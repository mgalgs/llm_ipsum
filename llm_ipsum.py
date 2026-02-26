#!/usr/bin/env -S uv --quiet run --script
# /// script
# requires-python = "==3.13"
# dependencies = [
#     "openai",
# ]
# ///

"""
Spiritual successor to lorem ipsum. Uses LLMs to generate placeholder text.
"""

import argparse
import random
import sys
import os

from openai import OpenAI


BASE_SYSTEM_PROMPT = """\
You are a placeholder text generator. Your task is to generate a string of placeholder text that is {num_words} words long.

Requirements:
- Output exactly {num_words} English words.
- Favor novelty over familiarity (even if slightly bizarre/non-sensical).
- Avoid overused "LLM-poetry" vocabulary (do not use any of these words): whisper, whispers, whispering, dreamy, dream, dreams, cloud, clouds, velvet, crimson.
- Avoid corporate/process/computer phrasing (do not mention systems, parameters, documentation, data transfer; do not write requests like "please confirm").
- Prefer concrete objects, textures, and surprising pairings; write a statement, not an instruction.
"""

SHORT_PHRASE_SYSTEM_PROMPT_APPEND = """\

Additional requirements (short phrase):
- For short phrases, avoid punctuation entirely.
"""

TITLE_SYSTEM_PROMPT_APPEND = """\

Additional requirements (title text):
- Output should be usable as a title/heading: do not end the text with punctuation.
- Prefer noun phrases over complete sentences.
"""

PROMPT_TEMPLATE = """\
Instruction: Output exactly {num_words} words of placeholder text{style_hint}. Draw vocabulary from: {domain}. Output *nothing* else.
"""

VOCAB_DOMAINS = [
    "kitchen utensils", "deep ocean creatures", "desert geology",
    "antique furniture", "tropical insects", "winter clothing",
    "brass instruments", "root vegetables", "abandoned factories",
    "circus equipment", "volcanic rock", "old bookshops",
    "fishing tackle", "bread baking", "railway stations",
    "carpentry tools", "tide pools", "alpine meadows",
    "pottery glazes", "copper plumbing", "beekeeping",
    "clock repair", "leather tanning", "paper mills",
    "harbor docks", "seed catalogues", "blacksmithing",
    "weaving looms", "cave formations", "market stalls",
]


def gen_system_prompt(num_words: int, title: bool) -> str:
    prompt = BASE_SYSTEM_PROMPT.format(num_words=num_words)
    if title:
        prompt += TITLE_SYSTEM_PROMPT_APPEND
    elif num_words < 10:
        prompt += SHORT_PHRASE_SYSTEM_PROMPT_APPEND
    return prompt


def llm_call(
    api_base_url,
    api_key,
    prompt,
    model,
    max_tokens,
    num_words,
    title,
    timeout,
) -> dict[str, str] | None:
    """Call the LLM API to generate text."""
    client = OpenAI(
        base_url=api_base_url,
        api_key=api_key,
        timeout=timeout,
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": gen_system_prompt(num_words=num_words, title=title),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=1.25,
            top_p=0.98,
            max_tokens=max_tokens,
            extra_headers={
                "HTTP-Referer": "https://mgalgs.io",
                "X-Title": "llm_ipsum",
            },
        )

        return {
            "content": response.choices[0].message.content.strip(),
        }
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None


def gen_prompt(num_words: int, topic: str, title: bool) -> str:
    style_hint = " suitable as a title" if title else ""
    domain = topic if topic != "generic" else random.choice(VOCAB_DOMAINS)
    return PROMPT_TEMPLATE.format(
        num_words=num_words,
        domain=domain,
        style_hint=style_hint,
    )


def guess_base_api_creds_from_env() -> tuple[str, str] | None:
    base_url = os.getenv("OPENAI_BASE_URL")
    api_key = os.getenv("OPENAI_API_KEY")

    if not (base_url and api_key):
        base_url = os.getenv("OPENROUTER_BASE_URL")
        api_key = os.getenv("OPENROUTER_API_KEY")

    if not (base_url and api_key):
        return None

    return (base_url, api_key)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate placeholder text with LLMs")
    parser.add_argument(
        "length", type=int, default=10, help="The length (in words) of text to generate"
    )
    parser.add_argument(
        "--model",
        default="google/gemini-2.5-flash-lite",
        help="The model to use for generating text",
    )
    parser.add_argument(
        "--topic", default="generic", help="The topic or theme for the generated text"
    )
    parser.add_argument(
        "--title",
        action="store_true",
        help="Generate title text (no trailing punctuation; prefer noun phrases)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=7,
        help="Timeout in seconds for the API call (default: 7)",
    )

    args = parser.parse_args()

    prompt: str = gen_prompt(args.length, args.topic, title=args.title)
    # Reasoning models (e.g. minimax-m2.5) use reasoning tokens that count
    # against max_tokens, so we need a generous budget beyond the actual
    # output length to avoid empty content.
    token_estimate: int = args.length * 5 + 500
    api_creds = guess_base_api_creds_from_env()
    if not api_creds:
        print(
            "Error: No API credentials found. Please set OPENAI_BASE_URL/OPENAI_API_KEY or OPENROUTER_BASE_URL/OPENROUTER_API_KEY.",
            file=sys.stderr,
        )
        return 1

    output: dict[str, str] | None = llm_call(
        api_base_url=api_creds[0],
        api_key=api_creds[1],
        prompt=prompt,
        model=args.model,
        max_tokens=token_estimate,
        num_words=args.length,
        title=args.title,
        timeout=args.timeout,
    )

    if output:
        print(output["content"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
