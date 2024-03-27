import logging.config

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from examples.heroku_the_internet.page_objects import dropdown
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
def navigate_to_page(launch_chrome) -> dropdown.Page:
    driver = launch_chrome
    page = dropdown.Page(driver)
    page.load_page()
    return page


def test_selecting_enabled_options(navigate_to_page) -> None:
    page = navigate_to_page
    options = ['Option 1', 'Option 2']
    for i in options:
        page.set_selection(option=i)
        actual_result = page.current_selection()
        expected_result = i

        err_msg = "Unexpected dropdown selection found:\n"
        err_msg += f"    Actual:   '{actual_result}'\n"
        err_msg += f"    Expected: '{expected_result}'"

        assert actual_result == expected_result, err_msg
    return


def test_selecting_disabled_options(navigate_to_page) -> None:
    page = navigate_to_page

    option_sequence = ['Option 1', 'Please select an option', 'Option 2', 'Please select an option']
    expected_results_sequence = ['Option 1', 'Option 1', 'Option 2', 'Option 2']

    for i_option, i_expected in zip(option_sequence, expected_results_sequence):
        page.set_selection(option=i_option)

        actual_result = page.current_selection()
        expected_result = i_expected

        err_msg = "Unexpected dropdown selection found:\n"
        err_msg += f"    Actual:   '{actual_result}'\n"
        err_msg += f"    Expected: '{expected_result}'"

        assert actual_result == expected_result, err_msg
    return
