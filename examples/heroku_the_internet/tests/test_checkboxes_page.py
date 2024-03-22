import logging.config

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from examples.heroku_the_internet.page_objects import checkboxes
import misc.logging_config

logging.config.dictConfig(misc.logging_config.config)


@pytest.fixture(scope='session')
def launch_chrome() -> WebDriver:
    logging.debug('Launching Chrome...')
    driver = webdriver.Chrome()
    yield driver
    logging.debug('Closing Chrome...')
    driver.quit()
    return


@pytest.fixture(scope='function')
def navigate_to_page(launch_chrome) -> checkboxes.Page:
    driver = launch_chrome
    page = checkboxes.Page(driver)
    logging.debug(f'Navigating to {page}...')
    page.load_page()
    return page


@pytest.fixture(scope='function')
def navigate_to_page_and_verify_initial_state(navigate_to_page) -> checkboxes.Page:
    page = navigate_to_page
    if page.checkbox_1_is_checked():
        log_msg = 'Checkbox 1 value:\n'
        log_msg += '  Expected: Not checked\n'
        log_msg += '  Actual:   Checked'
        logging.error(log_msg)
        raise ValueError(log_msg)
    if not page.checkbox_2_is_checked():
        log_msg = 'Checkbox 2 value:\n'
        log_msg += '  Expected: Checked\n'
        log_msg += '  Actual:   Not checked'
        logging.error(log_msg)
        raise ValueError(log_msg)
    return page


def test_clicking_unchecked_box_results_in_checked_box(navigate_to_page_and_verify_initial_state) -> None:
    page = navigate_to_page_and_verify_initial_state
    page.click_checkbox_1()
    assert page.checkbox_1_is_checked()
    return


def test_clicking_checked_box_results_in_unchecked_box(navigate_to_page_and_verify_initial_state) -> None:
    page = navigate_to_page_and_verify_initial_state
    page.click_checkbox_2()
    assert not page.checkbox_2_is_checked()
    return


def test_clicking_multiple_times(navigate_to_page_and_verify_initial_state) -> None:
    number_of_clicks = 10
    page = navigate_to_page_and_verify_initial_state
    for i in range(number_of_clicks):
        page.click_checkbox_1()
        if i % 2 == 1:
            assert not page.checkbox_1_is_checked()
        else:
            assert page.checkbox_1_is_checked()
    return
