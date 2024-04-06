import logging.config

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

import misc.logging_config

logging.config.dictConfig(misc.logging_config.config)


@pytest.fixture(scope='session')
def launch_chrome() -> WebDriver:
    logging.debug('Launching Chrome...')
    driver = webdriver.Chrome()
    driver.set_window_size(width=1920, height=1080)
    yield driver
    logging.debug('Closing Chrome...')
    driver.quit()
    return
