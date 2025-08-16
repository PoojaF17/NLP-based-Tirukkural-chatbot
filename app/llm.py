\
import os, json, textwrap
from typing import List, Dict
from dotenv import load_dotenv
from .prompts import SYSTEM_PROMPT, TEMPLATE_USER

load_dotenv()

def _format_context(kurals: List[Dict]) -> str:
    keep = []
    for k in kurals:
        keep.append({
            "kural_number": k["kural_number"],
            "tamil": k["tamil"],
            "translation": k["translation"],
            "explanation": k.get("explanation", ""),
            "chapter": k.get("chapter", ""),
            "section": k.get("section", ""),
        })
    return json.dumps(keep, ensure_ascii=False, indent=2)

def generate_with_openai(query: str, kurals: List[Dict]) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return ""  # Will trigger fallback

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        user_msg = TEMPLATE_USER.format(query=query, context_json=_format_context(kurals))

        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.7,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f""  # empty -> fallback

def generate_fallback(query: str, kurals: List[Dict]) -> str:
    # Simple, deterministic, no-external-call formatter
    if not kurals:
        return "மன்னிக்கவும்! பொருத்தமான குறள் எதுவும் கிடைக்கவில்லை. Couldn’t find a relevant Kural."

    k = kurals[0]
    others = kurals[1:3]
    lines = []

    lines.append(f"**Kural {k['kural_number']}**")
    lines.append(f"**Tamil**: {k['tamil']}")
    lines.append(f"**Translation**: {k['translation']}")
    if k.get("explanation"):
        lines.append(f"**Meaning**: {k['explanation']}")
    if others:
        more = ", ".join([f"#{o['kural_number']}" for o in others])
        lines.append(f"_Also see_: {more}")
    # A light-touch, generic modern application
    lines.append("**Modern take**: Think about how this applies directly to your situation. "
                 "Act with self-control and compassion where possible; the Kural often balances firmness with kindness.")
    return "\n\n".join(lines)

def generate_answer(query: str, kurals: List[Dict]) -> str:
    out = generate_with_openai(query, kurals)
    if out.strip():
        return out
    return generate_fallback(query, kurals)
