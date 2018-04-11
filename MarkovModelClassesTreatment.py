import scr.SamplePathClasses as PathCls
import scr.StatisticalClasses as StatCls
import scr.RandomVariantGenerators as rndClasses
import ParameterClassesTreatment as P
import InputData as Data


class Patient:
    def __init__(self, id, parameters):
        self._id = id
        # random number generator for this patient
        self._rng = None
        # parameters
        self._param = parameters
        # state monitor
        self._stateMonitor = PatientStateMonitor(parameters)
        # simulation time step
        self._delta_t = parameters.get_delta_t()

    def simulate(self, sim_length):
        """ simulate the patient over the specified simulation length """

        # random number generator for this patient
        self._rng = rndClasses.RNG(self._id)

        k = 0  # current time step

        # while the patient is alive and simulation length is not yet reached
        while self._stateMonitor.get_if_alive() and k*self._delta_t < sim_length:

            # find the transition probabilities of the future states
            trans_probs = self._param.get_transition_prob(self._stateMonitor.get_current_state())
            # create an empirical distribution
            empirical_dist = rndClasses.Empirical(trans_probs)
            # sample from the empirical distribution to get a new state
            # (returns an integer from {0, 1, 2, ...})
            new_state_index = empirical_dist.sample(self._rng)

            # update health state
            self._stateMonitor.update(k, P.HealthStats(new_state_index))

            # increment time step
            k += 1

    def get_survival_time(self):
        """ returns the patient's survival time"""
        return self._stateMonitor.get_survival_time()

    def get_time_to_death(self):
        return self._stateMonitor.get_time_to_death()

    def get_num_strokes(self):
        """ returns the patient's number of strokes """
        return self._stateMonitor.get_num_strokes()


class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self, parameters):
        """
        :param parameters: patient parameters
        """
        self._currentState = parameters.get_initial_health_state() # current health state
        self._delta_t = parameters.get_delta_t()    # simulation time step
        self._survivalTime = 0          # survival time
        self._num_strokes = 0        # number of strokes
        self._ifstroke = False   # if the patient had a stroke
        self._dead = False


    def update(self, k, next_state):
        """
        :param k: current time step
        :param next_state: next state
        """

        # if the patient has died, do nothing
        if not self.get_if_alive():
            return

        # update survival time
        if next_state in [P.HealthStats.DEAD]:
            self._survivalTime = (k+0.5)*self._delta_t  # corrected for the half-cycle effect

        # update number of strokes
        if self._currentState != P.HealthStats.POST_STROKE and next_state == P.HealthStats.STROKE:
            self._ifstroke = True
        if self._currentState != P.HealthStats.WELL and next_state == P.HealthStats.STROKE:
            self._ifstroke = True

        # update current health state
        self._currentState = next_state

    def get_if_alive(self):
        result = True
        if self._currentState in [P.HealthStats.DEAD]:
            result = False
        return result

    def get_current_state(self):
        return self._currentState

    def get_survival_time(self):
        """ returns the patient survival time """
        # return survival time only if the patient has died
        if not self.get_if_alive():
            return self._survivalTime
        else:
            return None

    def get_num_strokes(self):
        """ returns the patient's number of strokes """
        # return time to AIDS  only if the patient has had a stroke
        if self._ifstroke:
            self._num_strokes +=1
            return self._num_strokes
        else:
            return None

    def get_time_to_death(self):
        if self._dead:
            return self._dead
        else:
            return None

class Cohort:
    def __init__(self, id, therapy):
        """ create a cohort of patients
        :param id: an integer to specify the seed of the random number generator
        """
        self._initial_pop_size = Data.POP_SIZE
        self._patients = []      # list of patients

        # populate the cohort
        for i in range(self._initial_pop_size):
            patient = Patient(id * self._initial_pop_size + i, P.ParametersFixed(therapy))
            self._patients.append(patient)

    def simulate(self):
        """ simulate the cohort of patients over the specified number of time-steps
        :returns outputs from simulating this cohort
        """

        # simulate all patients
        for patient in self._patients:
            patient.simulate(Data.SIM_LENGTH)

        # return the cohort outputs
        return CohortOutputs(self)

    def get_initial_pop_size(self):
        return self._initial_pop_size

    def get_patients(self):
        return self._patients


class CohortOutputs:
    def __init__(self, simulated_cohort):
        """ extracts outputs from a simulated cohort
        :param simulated_cohort: a cohort after being simulated
        """

        self._survivalTimes = []        # patients' survival times
        self._set_of_strokes = []        # patients' numbers of strokes
        self._time_to_death = []
        # survival curve
        self._survivalCurve = \
            PathCls.SamplePathBatchUpdate('Population size over time', id, simulated_cohort.get_initial_pop_size())

        # find patients' survival times
        for patient in simulated_cohort.get_patients():

            # get the patient survival time
            survival_time = patient.get_survival_time()
            if not (survival_time is None):
                self._survivalTimes.append(survival_time)           # store the survival time of this patient
                self._survivalCurve.record(survival_time, -1)       # update the survival curve

            # get the patient's number of strokes
            num_of_strokes = patient.get_num_strokes()
            if not (num_of_strokes is None):
                self._set_of_strokes.append(num_of_strokes)


        # summary statistics
        self._sumStat_survivalTime = StatCls.SummaryStat('Patient survival time', self._survivalTimes)
        self._sumState_TotalStrokes = StatCls.SummaryStat('number of strokes', self._set_of_strokes)


    def get_survival_times(self):
        return self._survivalTimes

    def get_set_of_strokes(self):
        return self._set_of_strokes

    def get_sumStat_survival_times(self):
        return self._sumStat_survivalTime

    def get_sumStat_num_of_strokes(self):
        return self._sumState_TotalStrokes

    def get_survival_curve(self):
        return self._survivalCurve
