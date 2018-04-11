import ParameterClassesTreatment as P
import MarkovModelClasses as MarkovCls
import SupportMarkovModel as SupportMarkov


# simulating anticoagulation
# create a cohort
cohort_anticoagulation = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.ANTICOAGULATION)

# simulate the cohort

simOutputs = cohort_anticoagulation.simulate()

# draw survival curves and histograms
SupportMarkov.draw_survival_curves_and_histograms(simOutputs_anticoagulation, simOutputs_anticoagulation)

