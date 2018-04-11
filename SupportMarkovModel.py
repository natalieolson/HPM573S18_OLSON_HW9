import InputData as Settings
import scr.FormatFunctions as F
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs
import scr.StatisticalClasses as Stat
import scr.EconEvalClasses as Econ


def print_outcomes(simOutput, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param simOutput: output of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and confidence interval text of patient survival time
    survival_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_survival_times().get_mean(),
        interval=simOutput.get_sumStat_survival_times().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # mean and confidence interval text of number of strokes
    time_to_stroke_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_time_to_stroke().get_mean(),
        interval=simOutput.get_sumStat_time_to_stroke().get_t_CI(alpha=Settings.ALPHA),
        deci=2)



    # print outcomes
    print(therapy_name)
    print("  Estimate of mean survival time and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          survival_mean_CI_text)
    print("  Estimate of mean time to AIDS and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          time_to_HIV_death_CI_text)
    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")


def draw_survival_curves_and_histograms(simOutputs_sans_anticoagulation, simOutputs_anticoagulation):
    """ draws the survival curves and the histograms of time until death
    :param simOutputs_sans_anticoagulation: output of a cohort simulated under mono therapy
    :param simOutputs_anticoagulation: output of a cohort simulated under combination therapy
    """

    # get survival curves of both treatments
    survival_curves = [
        simOutputs_sans_anticoagulation.get_survival_curve(),
        simOutputs_anticoagulation.get_survival_curve()
    ]

    # graph survival curve
    PathCls.graph_sample_paths(
        sample_paths=survival_curves,
        title='Survival curve',
        x_label='Simulation time step (year)',
        y_label='Number of alive patients',
        legends=['no anticoagulation', 'anticoagulation']
    )

    # histograms of survival times
    set_of_survival_times = [
        simOutputs_sans_anticoagulation.get_survival_times(),
        simOutputs_anticoagulation.get_survival_times()
    ]

    # graph histograms
    Figs.graph_histograms(
        data_sets=set_of_survival_times,
        title='Histogram of patient survival time',
        x_label='Survival time (year)',
        y_label='Counts',
        bin_width=1,
        legend=['no anticoagulation', 'anticoagulation'],
        transparency=0.6
    )


def print_comparative_outcomes(simOutputs_sans_anticoagulation, simOutputs_anticoagulation):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under combination therapy compared to mono therapy
    :param simOutputs_sans_anticoagulation: output of a cohort simulated under mono therapy
    :param simOutputs_anticoagulation: output of a cohort simulated under combination therapy
    """

    # increase in survival time under combination therapy with respect to NO anticoagulation
    increase_survival_time = Stat.DifferenceStatIndp(
        name='Increase in survival time',
        x=simOutputs_anticoagulation.get_survival_times(),
        y_ref=simOutputs_sans_anticoagulation.get_survival_times())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_survival_time.get_mean(),
        interval=increase_survival_time.get_t_CI(alpha=Settings.ALPHA),
        deci=2)
    print("Average increase in survival time "
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)
