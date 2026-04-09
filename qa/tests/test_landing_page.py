from playwright.sync_api import Page, expect
from qa.pages.landing import LandingPage
from qa.utilities.logging_utils import logger_utility
import os
import pytest


@pytest.mark.profile
def test_profile_info(page_instance: Page) -> None:
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
    logger_utility().info(f'Download CV function works as expected')


@pytest.mark.sidebar_nav
@pytest.mark.parametrize('navigation', ['intro', 'experience', 'projects-work',
                                        'projects-personal', 'skills'],
                         ids=['intro', 'professional_exp', 'delivery_exp', 'test_auto_projects',
                              'skills'])
def test_sidebar_navigation(page_instance, navigation):
    section = page_instance.locator(f"#{navigation}")

    with page_instance.expect_navigation():
        page_instance.click(f"a[href='#{navigation}']")

    # URL check
    assert f"#{navigation}" in page_instance.url
    logger_utility().info(f'Sidebar navigation: {navigation} works as expected')

    # Ensure Playwright scrolls it into view
    section.scroll_into_view_if_needed()
    expect(section).to_be_visible()


@pytest.mark.personal_site_links
@pytest.mark.parametrize('personal_sites', ['linkedin', 'github'],
                         ids=['linkedin', 'github'])
def test_personal_site_links(page_instance: Page, personal_sites):
    with page_instance.expect_popup() as popup_info:
        page_instance.locator(f".sidebar-social .fab.fa-{personal_sites}").click()

    new_page = popup_info.value
    new_page.wait_for_load_state("domcontentloaded")

    # URL validation (flexible)
    assert f"{personal_sites}.com" in new_page.url
    logger_utility().info(f'{personal_sites} link works as expected')


@pytest.mark.mailto
def test_mailto_link(page_instance: Page):
    link = page_instance.locator("a[href^='mailto:']")

    href = link.get_attribute("href")

    assert href is not None
    assert href.startswith("mailto:")
    assert "c_melski@yahoo.com" in href
    logger_utility().info(f'Mailto link is correct')
