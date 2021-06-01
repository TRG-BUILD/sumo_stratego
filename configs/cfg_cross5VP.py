import os

# paths

RUN_NAME = "four_phase_vf7"
RESULT_PATH = "output/four_phase"
DEBUG_NAME = os.path.join("debug/four_phase", RUN_NAME) 
MODELFILE = "stratego/four_phase_template.xml"
QUERY = "stratego/four_phase_query.q"
VERIFYTA_PATH = "verifyta"
#VERIFYTA_PATH = "$HOME/Documents/uppaal/stratego8_7/bin-Linux/verifyta"

TLS_ID = "C"

# How to translate the phases from controller to simulator
CTRL_TO_SIM_PHASE = {
    0: 0,
    1: 1,
    2: 2,
    3: 3
} 

# inserted once in the beginning of the simulation
CONSTANTS = {}

# template for the controller input state
CTRL_STATE = {
    "A": [0, 0, 0],
    "B": [0, 0, 0],
    "is_active": [0, 0, 0, 1],
    "x": 0.0
    }

CTRL_TO_SIM_FEATURES = {
    "A": [
        {0: "NC_4", 1: "NC_3", 2: "NC_2"}, 
        {0: "SC_4", 1: "SC_3", 2: "SC_2"}
    ],
    "B": [
        {0: "WC_4", 1: "WC_3", 2: "WC_2"},
        {0: "EC_4", 1: "EC_3", 2: "EC_2"}
    ]
}

SIM_TO_CTRL_FEATURES = {
    "NC_4": ("A", 0),
    "NC_3": ("A", 1),
    "NC_2": ("A", 2),
    "SC_4": ("A", 0),
    "SC_3": ("A", 1),
    "SC_2": ("A", 2),
    "WC_4": ("B", 0),
    "WC_3": ("B", 1),
    "WC_2": ("B", 2),
    "EC_4": ("B", 0),
    "EC_3": ("B", 1),
    "EC_2": ("B", 2)
}

OBSERVED_LANES = [k for k in SIM_TO_CTRL_FEATURES.keys()]
SIM_TO_CTRL_PHASE = {v: k for k, v in CTRL_TO_SIM_PHASE.items()}

# simulation parameters
KAPPA = 5
WARMUP = 1
