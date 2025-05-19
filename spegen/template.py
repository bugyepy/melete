from __future__ import annotations

from typing import Dict, List

import openai

from data import ABILITIES, ABILITY_NAMES_JA, ENV_PARAMETER_NAMES_JA


ENV_COMMENTS: Dict[str, Dict[object, str]] = {
    "E1_gravity_g": {
        0.1: "低重力環境が想定される。",
        1: "地球並みの重力と考えられる。",
        3: "高重力環境が予測される。",
    },
    "E2_atmosphere": {
        "vacuum": "大気がほとんど存在しない。",
        "reducing": "還元性大気で化学的に活発。",
        "oxidizing": "酸素を含む酸化的な大気。",
        "high_pressure": "高圧の大気。",
    },
    "E3_surface_temp_C": {
        -180: "極低温環境。",
        0: "氷点近くの温度。",
        80: "高温環境。",
    },
    "E4_liquid_medium": {
        "water": "液体の水が存在する。",
        "ammonia": "液体アンモニアが存在する。",
        "methane": "液体メタンが存在する。",
        "none": "液体が存在しない。",
    },
    "E5_radiation_factor": {
        0.1: "放射線量が低い。",
        1: "放射線量は地球並み。",
        100: "放射線量が非常に高い。",
    },
    "E6_energy_gradient": {
        "stellar": "恒星由来のエネルギー源。",
        "chem_redux": "化学的な還元反応が主なエネルギー。",
        "tidal": "潮汐加熱が主なエネルギー源。",
    },
    "E7_metal_silicate": {
        "poor": "金属・ケイ素が乏しい。",
        "earthlike": "地球と同程度の金属・ケイ素量。",
        "rich": "金属・ケイ素が豊富。",
    },
    "E8_tectonics": {
        "dead": "地殻活動はほとんどない。",
        "plate": "プレートテクトニクスが存在する。",
        "continuous_plume": "継続的なプリューム活動。",
    },
}

ABILITY_COMMENTS: Dict[str, str] = {
    "M_Manipulation": "精密な操作で環境を改変できる。",
    "L_Locomotion": "長距離移動に優れている。",
    "H_Homeostasis": "体内環境を一定に保てる。",
    "X_ReactionControl": "高エネルギー反応を制御可能。",
    "E_EnergyScaling": "大規模なエネルギー利用ができる。",
    "M_ExternalMemory": "外部に情報を保存・共有できる。",
    "K_CumulativeInnovation": "技術を世代間で蓄積して発展させる。",
    "T_TheoryOfMind": "他者の思考を推測できる。",
    "R_SymbolicCommunication": "高度な記号による意思疎通。",
    "C_Metacognition": "自己の思考を客観視できる。",
    "P_LongTermPlanning": "長期的な計画を立て実行する。",
    "A_Allomothering": "血縁外で子育てを協力できる。",
    "U_MassCoordination": "多数が協力して行動できる。",
    "D_Domestication": "他種を制御し活用する。",
}

ECOLOGY_GROUP = {
    "M_Manipulation",
    "L_Locomotion",
    "H_Homeostasis",
    "X_ReactionControl",
    "E_EnergyScaling",
}

COGNITION_GROUP = {
    "M_ExternalMemory",
    "K_CumulativeInnovation",
    "T_TheoryOfMind",
    "R_SymbolicCommunication",
    "C_Metacognition",
}

SOCIETY_GROUP = {
    "P_LongTermPlanning",
    "A_Allomothering",
    "U_MassCoordination",
    "D_Domestication",
}


def _ability_codes() -> Dict[str, str]:
    """Return mapping from ability name to short code like 'H1'."""
    counts: Dict[str, int] = {}
    codes: Dict[str, str] = {}
    for name in ABILITIES:
        prefix = name.split("_")[0][0]
        counts[prefix] = counts.get(prefix, 0) + 1
        codes[name] = f"{prefix}{counts[prefix]}"
    return codes


ABILITY_CODES = _ability_codes()


def _env_codes() -> Dict[str, str]:
    """Return mapping from env parameter to code like 'E1'."""
    codes = {}
    for key in ENV_PARAMETER_NAMES_JA:
        codes[key] = key.split("_")[0]
    return codes


ENV_CODES = _env_codes()


def _abilities_text(bitset: int, group: set[str]) -> str:
    """Return annotated ability text for a group."""
    lines: List[str] = []
    for i, name in enumerate(ABILITIES):
        if bitset >> i & 1 and name in group:
            code = ABILITY_CODES.get(name, name)
            desc = ABILITY_COMMENTS.get(name, "")
            lines.append(f"{code}=\u300c{name}\u300d{desc}")
    return " ".join(lines) if lines else "特筆すべき能力はない。"


def render_species(bitset: int, env_vector: Dict[str, object]) -> str:
    """Render detailed description of a species with annotations."""
    env_parts = []
    for key, val in env_vector.items():
        code = ENV_CODES.get(key, key)
        comment = ENV_COMMENTS.get(key, {}).get(val, "")
        name = ENV_PARAMETER_NAMES_JA.get(key, key)
        env_parts.append(f"{code}={val} ({name}){comment}")
    env_text = " ".join(env_parts)

    ecology = _abilities_text(bitset, ECOLOGY_GROUP)
    cognition = _abilities_text(bitset, COGNITION_GROUP)
    society = _abilities_text(bitset, SOCIETY_GROUP)

    paragraphs = [
        "**生成された種族概要**",
        f"**環境 (Environment)**\n{env_text}",
        f"**生態 (Ecology)**\n{ecology}",
        f"**思考 (Cognition)**\n{cognition}",
        f"**社会 (Society)**\n{society}",
    ]
    return "\n\n".join(paragraphs)


def render_species_llm(bitset: int, env_vector: Dict[str, object]) -> str:
    """Generate species description using an LLM via OpenAI."""
    abilities = [
        name for i, name in enumerate(ABILITIES) if bitset >> i & 1
    ]
    env_desc = ", ".join(f"{k}={v}" for k, v in env_vector.items())
    abil_desc = ", ".join(abilities)
    prompt = (
        "環境パラメータ: "
        f"{env_desc}\n能力: {abil_desc}\n"
        "上記を踏まえ、環境・生態・思考・社会を短く説明し、"
        "各項目に注釈を付けてください。"
    )
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content.strip()
