import json
from playwright.sync_api import TimeoutError
from qa.utilities.dom_capture import capture_dom
from qa.ai.gpt_selector_healer import heal_selector
from qa.utilities.logging_utils import logger_utility


class SelectorHealer:
    def __init__(self, page):
        self.page = page
        with open("qa/selector_repo/selector_store.json") as f:
            self.store = json.load(f)

    def clean_selector(self, selector: str) -> str:

        selector = selector.strip()
        selector = selector.replace("plaintext", "")
        selector = selector.replace("```", "")
        selector = selector.replace("`", "")
        selector = selector.replace('\\"', '"')
        selector = selector.replace('\"', '"')
        return selector.strip().strip("`").strip('"').strip("'")

    def find(self, name: str):
        selectors = self.store[name]
        candidates = [selectors["primary"]] + selectors["alternatives"]

        # 1️⃣ Try stored selector_repo
        for selector in candidates:
            loc = self.page.locator(selector)
            try:
                loc.first.wait_for(timeout=1000)  # key for when there are more than 1 element returned
                print(f"[FOUND] {selector}")
                return loc
            except TimeoutError:
                logger_utility().info(f'Selector Candidate {selector} did not work')


        # 2️⃣ AI Healing
        broken = selectors["primary"]
        print("BROKEN:", broken)
        logger_utility().info(f'Primary selector BROKEN: {broken}')
        dom = capture_dom(self.page)
        new_selector = heal_selector(broken, dom)
        new_selector = self.clean_selector(new_selector)
        print("AI SUGGESTED:", new_selector)
        logger_utility().info(f'AI Suggested: {new_selector}')
        print(f"[AI HEAL] {new_selector}")
        logger_utility().info(f'AI HEAL: {new_selector}')

        # 3️⃣ Validate AI selector
        try:
            loc = self.page.locator(new_selector)
            loc.first.wait_for(timeout=1000)

            # 4️⃣ Persist learned selector
            self.store[name]["primary"] = self.clean_selector(new_selector)
            with open("qa/selector_repo/selector_store.json", "w") as f:
                json.dump(self.store, f, indent=2)

            print("[AI HEAL] Selector saved")
            logger_utility().info('[AI HEAL] Selector saved')
            return loc

        except TimeoutError:
            raise Exception("AI failed to heal selector")
