import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

import steps.pokedex


@pytest.fixture(scope='function')
def driver() -> WebDriver:
    d = webdriver.Chrome()
    steps.pokedex.load_page(driver=d)
    yield d

    d.quit()
    return
