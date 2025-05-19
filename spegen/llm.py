from __future__ import annotations
import os
from typing import Dict, List

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_species_description(env: Dict[str, object],
                                 abilities: List[str]) -> str:
    """Generate species description via OpenAI API."""
    env_desc = ", ".join(f"{k}={v}" for k, v in env.items())
    ability_desc = ", ".join(abilities)
    prompt = (
        "以下の条件を満たす未知の異星種族を日本語で出力してください。\n"
        f"環境: {env_desc}\n"
        f"能力: {ability_desc}\n"
        "大まかな種族の概要を述べた後、"
        "環境・生態・思考・社会の各項目を記載してください。"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
