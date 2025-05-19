from __future__ import annotations
import argparse
import json
from typing import Dict


from .core import mask_abilities, enumerate_valid_sets, score_set
from .template import render_species
from .schema import EnvVector


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SF Species Generator")
    parser.add_argument("--env", action="append", default=[], help="Env key=val")
    parser.add_argument("--top", type=int, default=5, help="Number of results")
    parser.add_argument("--markdown", action="store_true", help="Markdown output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    env: Dict[str, object] = {}
    for item in args.env:
        if '=' not in item:
            continue
        key, val = item.split('=', 1)
        if val.replace('.', '', 1).isdigit():
            val = float(val) if '.' in val else int(val)
        env[key] = val
    EnvVector(__root__=env)  # validation
    mask = mask_abilities(env)
    deps = {
        'X_ReactionControl': {'E_EnergyScaling'},
        'K_CumulativeInnovation': {'M_ExternalMemory'},
        'U_MassCoordination': {'T_TheoryOfMind', 'R_SymbolicCommunication'},
        'D_Domestication': {'M_Manipulation', 'T_TheoryOfMind'},
    }
    sets = enumerate_valid_sets(mask, deps)
    scored = [(s, score_set(s, env)) for s in sets]
    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[: args.top]
    results = []
    for bitset, score in top:
        text = render_species(bitset, env)
        results.append({"bitset": bitset, "score": score, "text": text})
    if args.markdown:
        for r in results:
            print(f"### Score: {r['score']:.2f}\n{r['text']}\n")
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
