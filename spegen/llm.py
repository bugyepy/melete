"""OpenAI-based species description generator."""

from __future__ import annotations

import argparse
from typing import Dict

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = openai.api_key or os.getenv("OPENAI_API_KEY")

from .data import ENV_PARAMETER_NAMES_JA
from .schema import EnvVector


def build_env_text(env: Dict[str, object]) -> str:
    """Return environment description in Japanese."""
    parts = []
    for key, val in env.items():
        name = ENV_PARAMETER_NAMES_JA.get(key, key)
        parts.append(f"{name}={val}")
    return "、".join(parts)


def generate_species(env: Dict[str, object], abilities: str) -> str:
    """Generate a species description using the OpenAI API."""
    env_text = build_env_text(env)
    prompt = (
        "以下の環境に適応したSFの種族案を日本語で一つ提案してください。\n"
        f"環境: {env_text}\n"
        f"能力: {abilities}\n"
        "大まかな種族の概要を述べた後、"
        "環境・生態・思考・社会の各項目を箇条書きで評価してください。"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message["content"].strip()


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="LLM Species Generator")
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        help="Env key=val",
    )
    parser.add_argument("--abilities", default="", help="Ability summary text")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    env: Dict[str, object] = {}
    for item in args.env:
        if "=" not in item:
            continue
        key, val = item.split("=", 1)
        if val.replace(".", "", 1).isdigit():
            val = float(val) if "." in val else int(val)
        env[key] = val
    EnvVector(__root__=env)
    text = generate_species(env, args.abilities)
    print(text)


if __name__ == "__main__":
    main()
