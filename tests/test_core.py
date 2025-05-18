from sfgen.core import mask_abilities, enumerate_valid_sets
from sfgen.data import ABILITIES


def test_mask_blocks_impossible():
    env = {"E2_atmosphere": "vacuum"}
    mask = mask_abilities(env)
    idx = ABILITIES.index("F_ControlledFire")
    assert mask[idx] == 0


def test_dependencies_enforced():
    mask = [1] * len(ABILITIES)
    deps = {"F_ControlledFire": {"E_ExponentialEnergy"}}
    sets = enumerate_valid_sets(mask, deps)
    for bitset in sets:
        idx_f = ABILITIES.index("F_ControlledFire")
        idx_e = ABILITIES.index("E_ExponentialEnergy")
        if bitset >> idx_f & 1:
            assert bitset >> idx_e & 1


def test_deterministic_results():
    env = {"E2_atmosphere": "reducing"}
    mask = mask_abilities(env)
    deps = {}
    s1 = enumerate_valid_sets(mask, deps)
    s2 = enumerate_valid_sets(mask, deps)
    assert s1 == s2
