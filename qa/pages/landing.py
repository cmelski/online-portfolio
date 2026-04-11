from qa.utilities.logging_utils import logger_utility
from playwright.sync_api import Page, expect
from qa.selector_repo.selector_healer import SelectorHealer


class LandingPage:

    def __init__(self, page):
        self.page = page
        self.healer = SelectorHealer(page)
        self.profile = self.healer.find('profile')
        self.automation_projects = self.healer.find('automation_projects')

    def get_profile_details(self):

        image = self.profile.locator('img')
        heading = self.profile.locator('h1')
        title = self.profile.locator('p')

        expect(image).to_be_visible()
        logger_utility().info(f'Profile image is visible')
        return heading, title


