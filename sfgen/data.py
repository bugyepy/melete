import os
import yaml

# Ability list
ABILITIES = [
    "H_PreciseGrasp", "L_Locomotion", "S_SweatCooling", "F_ControlledFire",
    "E_ExponentialEnergy", "M_ExternalMemory", "K_CumulativeCulture",
    "T_TheoryOfMind", "R_RecursiveLanguage", "C_Metacognition",
    "P_LongTermPlanning", "A_Allomothering", "U_MassCooperation",
    "D_Domestication"
]

# Environment parameter possible values
ENV_PARAMETERS = {
    "E1_gravity_g": [0.1, 1, 3],
    "E2_atmosphere": ["vacuum", "reducing", "oxidizing", "high_pressure"],
    "E3_surface_temp_C": [-180, 0, 80],
    "E4_liquid_medium": ["water", "ammonia", "methane", "none"],
    "E5_radiation_factor": [0.1, 1, 100],
    "E6_energy_gradient": ["stellar", "chem_redux", "tidal"],
    "E7_metal_silicate": ["poor", "earthlike", "rich"],
    "E8_tectonics": ["dead", "plate", "continuous_plume"],
}

# Load compatibility matrix from YAML
_COMP_PATH = os.path.join(os.path.dirname(__file__), "compatibility.yaml")
if os.path.exists(_COMP_PATH):
    with open(_COMP_PATH, "r", encoding="utf-8") as f:
        COMP_MATRIX = yaml.safe_load(f)
else:
    COMP_MATRIX = {}
