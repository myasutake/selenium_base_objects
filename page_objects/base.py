import abc
import logging
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class Base(metaclass=abc.ABCMeta):

    def __init__(self, desc: str = None) -> None:
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
    def _find_element(self, locator: dict) -> WebElement:
        pass

    @abc.abstractmethod
    def is_loaded(self) -> bool:
        pass

    def wait_until_loaded(self, timeout=5.0, must_load=True) -> None:
        end_time = time.time() + timeout
        while time.time() < end_time:
            time.sleep(0.5)
            if self.is_loaded():
                return
        log_str = f"'{self._desc}' did not load."
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
    #   Exception: logging.

    def _text_of_element_at(self, locator: dict) -> str:
        return self._find_element(locator).text


class BasePage(Base, metaclass=abc.ABCMeta):

    def __init__(self, driver: WebDriver, url: str = None, desc: str = None) -> None:
        super().__init__(desc=desc)
        self._driver = driver
        self._url = url
        return

    def element_exists_and_is_displayed(self, locator: dict) -> bool:
        # This seems obvious enough to not warrant its own method.
        #   However, calling _element_is_displayed() first could raise an unexpected exception.
        if not self.element_exists(locator=locator):
            return False
        return self._element_is_displayed(locator=locator)

    def load_page(self) -> None:
        self._load_page()
        self.wait_until_loaded()
        return

    # Selenium method wrappers
    #   Same rules as Base class apply.

    def _click_element(self, locator: dict) -> None:
        logging.info(f'Clicking element at {locator}.')
        self._find_element(locator).click()
        return

    def _element_is_displayed(self, locator: dict) -> bool:
        return self._find_element(locator).is_displayed()

    def _find_element(self, locator: dict) -> WebElement:
        return self._driver.find_element(by=locator['by'], value=locator['value'])

    def _find_elements(self, locator: dict) -> list[WebElement]:
        return self._driver.find_elements(by=locator['by'], value=locator['value'])

    def _load_page(self) -> None:
        logging.info(f"Loading '{self._desc}'.")
        self._driver.get(self._url)
        return

    def _send_keystrokes_to_element(self, locator: dict, input_str: str) -> None:
        logging.info(f'Sending keystrokes "{input_str}" to element at {locator}.')
        self._find_element(locator).send_keys(input_str)
        return


class BaseElement(Base, metaclass=abc.ABCMeta):

    def __init__(self, element: WebElement, desc: str = None) -> None:
        super().__init__(desc=desc)
        self._element = element
        return

    # Selenium method wrappers
    #   Same rules as Base class apply.

    def _click(self) -> None:
        logging.info(f"Clicking '{self._desc}'.")
        self._element.click()
        return

    def _is_displayed(self) -> bool:
        return self._element.is_displayed()

    def _find_element(self, locator: dict) -> WebElement:
        return self._element.find_element(by=locator['by'], value=locator['value'])

    def _find_elements(self, locator: dict) -> list[WebElement]:
        return self._element.find_elements(by=locator['by'], value=locator['value'])

    def _send_keystrokes(self, input_str: str) -> None:
        logging.info(f'Sending keystrokes "{input_str}" to "{self._desc}".')
        self._element.send_keys(input_str)
        return

    def _text(self) -> str:
        return self._element.text
