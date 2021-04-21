import abc
import logging
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class BasePage(metaclass=abc.ABCMeta):

    def __init__(self, driver: WebDriver, url: str = None, desc: str = None) -> None:
        self._driver = driver
        self._url = url
        self._desc = desc
        self._locators = dict()
        return

    def element_exists(self, locator: dict) -> bool:
        try:
            self._find_element(locator=locator)
        except NoSuchElementException:
            return False
        else:
            return True

    @abc.abstractmethod
    def is_loaded(self) -> bool:
        pass

    def load_page(self) -> None:
        self._load_page()
        self.wait_until_loaded()
        return

    def wait_until_loaded(self, timeout=5.0, must_load=True) -> None:
        end_time = time.time() + timeout
        while time.time() < end_time:
            time.sleep(0.5)
            if self.is_loaded():
                return
        log_str = '{} did not load.'.format(self._desc)
        if must_load is True:
            logging.error(log_str)
            raise TimeoutError(log_str)
        else:
            logging.warning(log_str)
            return

    # Selenium method wrappers
    #   In the event the Selenium methods get renamed, you only need to change them here.
    #   All methods must be private.
    #   Only straight Selenium code goes here.
    #   All methods should be one-liners (i.e. no additional logic).

    def _click_element(self, locator: dict) -> None:
        self._find_element(locator).click()
        return

    def _element_is_displayed(self, locator: dict) -> bool:
        return self._find_element(locator).is_displayed()

    def _find_element(self, locator: dict) -> WebElement:
        return self._driver.find_element(by=locator['by'], value=locator['value'])

    def _find_elements(self, locator: dict) -> list[WebElement]:
        return self._driver.find_elements(by=locator['by'], value=locator['value'])

    def _load_page(self) -> None:
        self._driver.get(self._url)
        return

    def _send_keystrokes_to_element(self, locator: dict, input_str: str) -> None:
        self._find_element(locator).send_keys(input_str)
        return
