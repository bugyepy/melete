from __future__ import annotations
import os
from typing import Dict, List

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_species_description(env: Dict[str, object],
                                 abilities: List[str]) -> str:
    """Generate species description via OpenAI API."""
    env_desc = ", ".join(f"{k}={v}" for k, v in env.items())
    ability_desc = ", ".join(abilities)
    prompt = (
        "Provide a short overview of a fictional species followed by\n"
        "evaluations under the headings Environment, Ecology, Cognition "
        "and Society.\n"
        f"Environment parameters: {env_desc}.\n"
        f"Abilities: {ability_desc}."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
