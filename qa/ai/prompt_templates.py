HEAL_SELECTOR_PROMPT = """
You are a senior test automation engineer.

The Playwright selector "{broken_selector}" failed.

HTML snapshot:
{dom}

Return the selector as raw CSS, not JSON escaped.
Example: [id="user-name"]
Do not use backslashes.
No explanations.
"""
