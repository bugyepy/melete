from __future__ import annotations
from typing import Dict

from data import ABILITIES


TEMPLATES = {
    'ecology': "{abilities} thrive under {env}.",
    'cognition': "Their thinking leverages {cog} abilities.",
    'society': "Society is structured around {soc}."
}


def render_species(bitset: int, env_vector: Dict[str, object]) -> str:
    """Render short description of species."""
    abilities_on = [name for i, name in enumerate(ABILITIES) if bitset >> i & 1]
    env_desc = ', '.join(f"{k}={v}" for k, v in env_vector.items())
    ability_str = ', '.join(abilities_on) if abilities_on else 'no abilities'
    paragraphs = [
        TEMPLATES['ecology'].format(abilities=ability_str, env=env_desc),
        TEMPLATES['cognition'].format(cog=ability_str),
        TEMPLATES['society'].format(soc=ability_str),
    ]
    return '\n\n'.join(paragraphs)
