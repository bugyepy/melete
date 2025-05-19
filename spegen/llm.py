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
        "以下の条件を満たす未知の異星種族を日本語で出力してください。ただし、以下の条件は極端に抽象化されているため、前提としてのみ扱い、それを元に推測・推論して具体化してください。\n"
        f"環境: {env_desc}\n"
        f"能力: {ability_desc}\n"
        f"\n"
        "大まかな種族の概要を述べた後、"
        "環境・生態・思考・社会の各項目を記載してください。\n"
        "環境: その種族が生息する環境や生態系について説明してください。\n"
        "思考: その種族の思考や行動様式について説明してください。\n"
        "社会: その種族の社会構造や文化について説明してください。\n"
        "それぞれの項目は、見出しをつけて分けてください。\n"
        "見出しの後は改行し、内容は日本語で記載してください。\n"
        "以下はフォーマットです。\n"
        "概要: [種族名]は、[概要を記載。外見（m単位の全長や特徴的な部位等）や習性、生息域、交配等ありうるものは全て記載]\n"
        "環境: [環境]\n"
        "思考: [思考]\n"
        "社会: [社会]\n"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
