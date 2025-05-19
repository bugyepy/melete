from __future__ import annotations
from typing import Dict

from data import ABILITIES, ABILITY_NAMES_JA


TEMPLATES = {
    'ecology': "{abilities}は{env}で繁栄する。",
    'cognition': "思考様式は{cog}に依拠する。",
    'society': "社会構造は{soc}を基盤とする。",
}


def render_species(bitset: int, env_vector: Dict[str, object]) -> str:
    """Render short description of species."""
    abilities_on = [ABILITY_NAMES_JA.get(name, name) for i, name in enumerate(ABILITIES) if bitset >> i & 1]
    env_desc = '、'.join(f"{k}={v}" for k, v in env_vector.items())
    ability_str = '、'.join(abilities_on) if abilities_on else '能力なし'
    paragraphs = [
        TEMPLATES['ecology'].format(abilities=ability_str, env=env_desc),
        TEMPLATES['cognition'].format(cog=ability_str),
        TEMPLATES['society'].format(soc=ability_str),
    ]
    return '\n\n'.join(paragraphs)
