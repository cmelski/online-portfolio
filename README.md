**Overview**

Static website for my online cv and portfolio.  Also includes a python playwright test automation framework. This framework includes an AI-assisted selector healing mechanism designed to improve test stability when UI changes break existing locators.

It follows a structured fallback approach:

- Primary selector 
- Alternative selectors
- AI-generated selector based on DOM context

When a valid selector is found, it is reused. If AI successfully heals a selector, it is automatically persisted for future runs.

**How it works**

1. Selector Resolution

Each element is defined in a selector store:

{
  "automation_projects": {
    "primary": "#projects-personal .card",
    "alternatives": [
      "#projects_personal .card",
      ".projects-personal .card"
    ]
  }
}

The framework attempts each selector until a valid match is found.

2. Validation

Selectors are validated by checking that at least one element is present:

locator.first.wait_for(timeout=1000)

This avoids false positives where a locator exists but matches no elements.

3. AI Healing

If all selectors fail:

- The current DOM is captured
- The broken selector is sent to the AI model
- A new selector is generated based on DOM structure

4. Selector Normalization

AI responses are cleaned before use:

selector = selector.replace("```", "").strip()

This ensures compatibility with Playwright.

5. Persistence

If the AI-generated selector is valid:

- It replaces the primary selector
- It is saved back to the selector store
- self.store[name]["primary"] = new_selector

This allows the framework to “learn” over time.

**Example Usage**

class LandingPage:

    def __init__(self, page):
        self.page = page
        self.healer = SelectorHealer(page)
        self.automation_projects = self.healer.find("automation_projects")

**Key Benefits**

- Reduces test maintenance caused by UI changes
- Supports both single elements and collections
- Automatically recovers from broken selectors
- Improves long-term stability through learned selectors

**Notes**

- Validation uses .first.wait_for() to avoid strict mode issues with multiple elements
- AI healing is only triggered when all known selectors fail