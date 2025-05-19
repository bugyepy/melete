import os
import yaml

# Ability list
ABILITIES = [
    "M_Manipulation",
    "L_Locomotion",
    "H_Homeostasis",
    "X_ReactionControl",
    "E_EnergyScaling",
    "M_ExternalMemory",
    "K_CumulativeInnovation",
    "T_TheoryOfMind",
    "R_SymbolicCommunication",
    "C_Metacognition",
    "P_LongTermPlanning",
    "A_Allomothering",
    "U_MassCoordination",
    "D_Domestication",
]

# Japanese ability descriptions
ABILITY_NAMES_JA = {
    "M_Manipulation": "外界へ微細かつ精密に力を加えて対象を操作できる能力",
    "L_Locomotion": "長距離を持続的に移動できる高効率の運動能力",
    "H_Homeostasis": "外部環境の変化に対し内部状態を能動的に安定化させる生理機構",
    "X_ReactionControl": "高エネルギー反応を制御し物質やエネルギーを変換・抽出する能力",
    "E_EnergyScaling": "エネルギー利用量を桁違いに拡大可能な社会・技術基盤を構築する能力",
    "M_ExternalMemory": "情報を身体外部に記録・共有し持続的に参照できる記憶インフラ",
    "K_CumulativeInnovation": "知識・技術を世代横断的に累積し継続的に改良・再構築する文化的仕組み",
    "T_TheoryOfMind": "他主体の感情・意図・信念を推定し行動を適応させる認知能力",
    "R_SymbolicCommunication": "再帰構造を持つ記号体系で無限に新規の意味を創出・伝達する能力",
    "C_Metacognition": "自己の知覚・思考過程を客観視し戦略的に修正できる能力",
    "P_LongTermPlanning": "長期的未来を見据え計画を立案・実行する能力",
    "A_Allomothering": "血縁を越えた個体間で子育てを協力的に行う繁殖戦略",
    "U_MassCoordination": "広域・多数の個体が血縁を超えて共通目標のために協働する社会システム",
    "D_Domestication": "異種の生物・システムを選択・改変・維持し自文明の目的に取り込む能力",
}

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
