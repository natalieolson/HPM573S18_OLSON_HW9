from enum import Enum
import InputData as Data
import scr.RandomVariantGenerators as Random


class HealthStats(Enum):
    """health states of patients with stroke"""
    WELL = 0
    STROKE = 1
    POST_STROKE = 2
    DEAD = 3

class Therapies(Enum):
    """ none vs. anticoagulation """
    NONE = 0
    ANTICOAGULATION = 1


class _Parameters:
    def __init__(self, therapy):
        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = Data.DELTA_T

        # initial health state
        self._initialHealthState = HealthStats.WELL

        #transmission probability matrix
        self._prob_matrix = []

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

class ParametersFixed(_Parameters):
    def __init__(self, therapy):


        # initialize the base class
        _Parameters.__init__(self, therapy)

        self._prob_matrix = calculate_prob_matrix()

class ParametersProbabilistic(_Parameters):
    def __init__(self, seed, therapy):

        # initializing the base class
        _Parameters.__init__(self, therapy)


def calculate_prob_matrix():
        prob_matrix = []
        for s in HealthStats:
            prob_matrix.append([0] * len(HealthStats))
            # for all health states
        for s in HealthStats:
            if s in [HealthStats.DEAD]:
                prob_matrix[s.value][s.value] = 1
        else:
            sum_counts = sum(Data.TRANS_MATRIX[s.value])
            for j in range(s.value):
                prob_matrix[s.value][j] = Data.TRANS_MATRIX[s.value][j] / sum_counts

        return prob_matrix
