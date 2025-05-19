import random
import streamlit as st

from data import ABILITIES, ENV_PARAMETERS
from core import mask_abilities, enumerate_valid_sets
from template import render_species


DEPS = {
    'F_ControlledFire': {'E_ExponentialEnergy'},
    'K_CumulativeCulture': {'M_ExternalMemory'},
    'U_MassCooperation': {'T_TheoryOfMind', 'R_RecursiveLanguage'},
    'D_Domestication': {'H_PreciseGrasp', 'T_TheoryOfMind'},
}


def random_env():
    """Return random environment vector."""
    return {k: random.choice(v) for k, v in ENV_PARAMETERS.items()}


def bitstring(bitset: int) -> str:
    return ''.join('1' if bitset >> i & 1 else '0' for i in range(len(ABILITIES)))


def run() -> None:
    st.title("SF Species Generator")

    if 'env' not in st.session_state:
        st.session_state['env'] = random_env()

    if st.button("Randomize Environment"):
        st.session_state['env'] = random_env()

    env = st.session_state['env']
    st.write("### Environment Parameters")
    st.json(env)

    mask = mask_abilities(env)
    sets = enumerate_valid_sets(mask, DEPS)

    if not sets:
        st.warning("No valid ability sets for this environment.")
        return

    sample = random.sample(sets, min(10, len(sets)))

    st.write("### Random Species")
    for bitset in sample:
        st.markdown(f"**{bitstring(bitset)}**")
        st.write(render_species(bitset, env))
        with st.expander("Ability Breakdown"):
            table_data = [
                {"Ability": abil, "Present": "yes" if bitset >> idx & 1 else "no"}
                for idx, abil in enumerate(ABILITIES)
            ]
            st.table(table_data)
            presence = "、".join(
                f"{abil}は{'ある' if bitset >> idx & 1 else 'ない'}"
                for idx, abil in enumerate(ABILITIES)
            )
            st.write(presence)
        st.divider()


if __name__ == "__main__":
    run()
