
from playwright.sync_api import Page, expect
from qa.pages.landing import LandingPage
from qa.utilities.logging_utils import logger_utility
import os
import pytest


@pytest.mark.landing_page
def test_landing_page(page_instance: Page) -> None:
    landing_page = LandingPage(page_instance)
    # Profile
    expect(landing_page.profile).to_be_visible()
    logger_utility().info(f'Profile section is visible')
    profile_details = landing_page.get_profile_details()
    heading_one = profile_details[0]
    expect(heading_one).to_have_text('Chris Melski')
    logger_utility().info(f'Heading One: {heading_one.inner_text()} correctly displayed')
    title = profile_details[1]
    expect(title).to_contain_text('Test Manager / SDET')
    logger_utility().info(f'Title: {title.inner_text()} correctly displayed')

@pytest.mark.csv_download
def test_cv_download(page_instance: Page):

    # Trigger and capture the download
    with page_instance.expect_download() as download_info:
        page_instance.click("text=Download CV")

    download = download_info.value

    # Basic assertions
    assert download.suggested_filename.endswith(".pdf")

    # Save the file locally (optional but useful for validation)
    download.save_as("qa/downloads/cv.pdf")

    # Check file actually exists and has content
    assert os.path.exists("qa/downloads/cv.pdf")
    assert os.path.getsize("qa/downloads/cv.pdf") > 0


