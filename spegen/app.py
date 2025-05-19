import random
import streamlit as st

from data import (
    ABILITIES,
    ENV_PARAMETERS,
    ABILITY_NAMES_JA,
    ENV_PARAMETER_NAMES_JA,
)
from core import mask_abilities, enumerate_valid_sets
from template import render_species, render_species_llm


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
    return ''.join(
        '1' if bitset >> i & 1 else '0' for i in range(len(ABILITIES))
    )


def run() -> None:
    st.title("Melete - Species Generator")
    use_llm = st.checkbox("LLM で説明を生成", value=False)

    if 'env' not in st.session_state:
        st.session_state['env'] = random_env()

    if st.button("環境をランダム生成"):
        st.session_state['env'] = random_env()

    env = st.session_state['env']
    st.write("### 環境パラメータ")
    env_ja = {ENV_PARAMETER_NAMES_JA.get(k, k): v for k, v in env.items()}
    st.json(env_ja)

    mask = mask_abilities(env)
    sets = enumerate_valid_sets(mask, DEPS)

    if not sets:
        st.warning("この環境では有効な能力セットがありません。")
        return

    sample = random.sample(sets, min(10, len(sets)))

    st.write("### ランダム種族")
    for bitset in sample:
        st.markdown(f"**{bitstring(bitset)}**")
        if use_llm:
            st.write(render_species_llm(bitset, env))
        else:
            st.write(render_species(bitset, env))
        with st.expander("能力一覧"):
            table_data = [
                {"能力": ABILITY_NAMES_JA.get(abil, abil),
                 "有無": "あり" if bitset >> idx & 1 else "なし"}
                for idx, abil in enumerate(ABILITIES)
            ]
            st.table(table_data)
            presence = "、".join(
                f"{ABILITY_NAMES_JA.get(abil, abil)}は"
                f"{'ある' if bitset >> idx & 1 else 'ない'}"
                for idx, abil in enumerate(ABILITIES)
            )
            st.write(presence)
        st.divider()


if __name__ == "__main__":
    run()
