from __future__ import annotations
from typing import Dict, List, Set

from data import ABILITIES, COMP_MATRIX


def mask_abilities(env_vector: Dict[str, object]) -> List[int]:
    """Return ability mask (1=possible, 0=impossible)."""
    mask = [1] * len(ABILITIES)
    for param, value in env_vector.items():
        table = COMP_MATRIX.get(param, {})
        compat = table.get(str(value), {})
        for i, ability in enumerate(ABILITIES):
            rating = compat.get(ability, 1)
            if rating == -1:
                mask[i] = 0
    return mask


def _check_dependencies(bitset: int, deps: Dict[str, Set[str]]) -> bool:
    for abil, required in deps.items():
        idx = ABILITIES.index(abil)
        if bitset >> idx & 1:
            for r in required:
                ridx = ABILITIES.index(r)
                if not (bitset >> ridx & 1):
                    return False
    return True


def enumerate_valid_sets(mask: List[int],
                         deps: Dict[str, Set[str]],
                         max_results: int = 1000) -> List[int]:
    """Enumerate valid ability bitsets."""
    n = len(mask)
    active_indices = [i for i, m in enumerate(mask) if m == 1]
    results = []
    total = 1 << len(active_indices)
    for bits in range(total):
        bitset = 0
        for j, idx in enumerate(active_indices):
            if bits >> j & 1:
                bitset |= 1 << idx
        if _check_dependencies(bitset, deps):
            results.append(bitset)
            if len(results) >= max_results:
                break
    return results


def score_set(bitset: int, env_vector: Dict[str, object]) -> float:
    """Calculate utility score for a bitset."""
    scores = []
    count = 0
    for i, ability in enumerate(ABILITIES):
        if bitset >> i & 1:
            count += 1
            score = 1.0
            for param, value in env_vector.items():
                table = COMP_MATRIX.get(param, {})
                compat = table.get(str(value), {})
                rating = compat.get(ability, 1)
                if rating == -1:
                    rating = 0
                score *= rating if rating > 0 else 0
            scores.append(score)
    if not scores:
        return 0.0
    return float(sum(scores) / len(scores) * count)
