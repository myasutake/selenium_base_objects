import logging

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

import steps.pokedex


def pytest_addoption(parser):
    parser.addoption('--config', action='store')
    return


@pytest.fixture
def params(request) -> str:
    return request.config.getoption('--config').lower()


@pytest.fixture(scope='function')
def driver(params) -> WebDriver:
    if params == 'chrome':
        d = webdriver.Chrome()
    elif params == 'firefox':
        d = webdriver.Firefox()
    else:
        log_str = f"Invalid 'config' param value '{params}' given."
        logging.error(log_str)
        raise ValueError(log_str)

    steps.pokedex.load_page(driver=d)
    yield d

    d.quit()
    return
