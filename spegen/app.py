import os
import random
import streamlit as st

from data import (
    ABILITIES,
    ENV_PARAMETERS,
    ABILITY_NAMES_JA,
    ENV_PARAMETER_NAMES_JA,
)
from core import mask_abilities, enumerate_valid_sets
from template import render_species
from llm import generate_species_description


DEPS = {
    'X_ReactionControl': {'E_EnergyScaling'},
    'K_CumulativeInnovation': {'M_ExternalMemory'},
    'U_MassCoordination': {'T_TheoryOfMind', 'R_SymbolicCommunication'},
    'D_Domestication': {'M_Manipulation', 'T_TheoryOfMind'},
}


def random_env():
    """Return random environment vector."""
    return {k: random.choice(v) for k, v in ENV_PARAMETERS.items()}


def bitstring(bitset: int) -> str:
    """Return binary representation for a bitset."""
    return ''.join(
        '1' if bitset >> i & 1 else '0'
        for i in range(len(ABILITIES))
    )


def run() -> None:
    """Run the Streamlit species generator app."""
    st.title("Melete - Species Generator")

    if "env" not in st.session_state:
        st.session_state["env"] = random_env()
    if "samples" not in st.session_state:
        st.session_state["samples"] = []
    if "descriptions" not in st.session_state:
        st.session_state["descriptions"] = {}

    if st.button("環境をランダム生成"):
        st.session_state["env"] = random_env()
        st.session_state["samples"] = []
        st.session_state["descriptions"] = {}

    env = st.session_state["env"]
    st.write("### 環境パラメータ")
    env_ja = {ENV_PARAMETER_NAMES_JA.get(k, k): v for k, v in env.items()}
    st.json(env_ja)

    mask = mask_abilities(env)
    if not st.session_state["samples"]:
        sets = enumerate_valid_sets(mask, DEPS)
        if not sets:
            st.warning("この環境では有効な能力セットがありません。")
            return
        st.session_state["samples"] = random.sample(sets, min(3, len(sets)))

    sample = st.session_state["samples"]


    auto_llm = bool(os.getenv("OPENAI_API_KEY"))
    for bitset in sample:
        if auto_llm:
            if bitset not in st.session_state["descriptions"]:
                abil_list = [
                    ABILITY_NAMES_JA.get(name, name)
                    for idx, name in enumerate(ABILITIES)
                    if bitset >> idx & 1
                ]
                desc = generate_species_description(env, abil_list)
                st.session_state["descriptions"][bitset] = desc
            st.write(st.session_state["descriptions"][bitset])

        with st.expander("詳細"):
            st.markdown(f"**{bitstring(bitset)}**")
            st.write(render_species(bitset, env))

            table_data = [
                {
                    "能力": ABILITY_NAMES_JA.get(abil, abil),
                    "有無": "あり" if bitset >> idx & 1 else "なし",
                }
                for idx, abil in enumerate(ABILITIES)
            ]
            st.table(table_data)
            presence = "、".join(
                f"{ABILITY_NAMES_JA.get(abil, abil)}"
                f"は{'ある' if bitset >> idx & 1 else 'ない'}"
                for idx, abil in enumerate(ABILITIES)
            )
            st.write(presence)
        st.divider()

if __name__ == "__main__":
    run()
