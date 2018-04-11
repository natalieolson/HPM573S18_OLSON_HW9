# simulation settings
POP_SIZE = 2000    # cohort population size
SIM_LENGTH = 50   # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DELTA_T = 1      # time step length


# transition matrix
TRANS_MATRIX = [
    [0.75,  0.15,      0.0,    0.1],   # Well
    [0,     0.0,       1.0,    0.0],   # Stroke
    [0,     0.25,      0.55,   0.2],   # Post-Stroke
    [0,     0,         0 ,     1.0]] #dead

ANTICOAGULATION_MATRIX = [
    [0.75,  0.15,    0.0,    0.1],   # Well
    [0,     0.0,     1.0,    0.0],   # Stroke
    [0,     0.1625,  0.6275, 0.21],   # Post-Stroke
    [0,     0,       0,      1] #dead
    ]

