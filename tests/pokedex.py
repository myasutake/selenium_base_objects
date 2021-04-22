import logging.config

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

import misc.logging_config
import steps.pokedex

logging.config.dictConfig(misc.logging_config.config)


@pytest.fixture(scope='function')
def driver() -> WebDriver:
    d = webdriver.Chrome()
    steps.pokedex.load_page(driver=d)
    yield d

    d.quit()
    return


def test_default_sort_method(driver) -> None:
    steps.pokedex.verify_sort_method_selected(driver=driver, sort_method='Lowest Number (First)')
    steps.pokedex.verify_search_results_are_sorted_correctly(driver=driver)
    return
