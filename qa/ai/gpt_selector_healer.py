import os
from pathlib import Path

from openai import OpenAI
from qa.ai.prompt_templates import HEAL_SELECTOR_PROMPT
from dotenv import load_dotenv
test_env = Path("test.env")
load_dotenv(test_env)

# Safety check (recommended)
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not found in environment")

client = OpenAI()


client.api_key = os.environ.get("OPENAI_API_KEY")


def heal_selector(broken_selector, dom):
    prompt = HEAL_SELECTOR_PROMPT.format(
        broken_selector=broken_selector,
        dom=dom[:12000]
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


