"""
Base classes used for all page objects.

Your page objects must subclass one of the following:
    BasePage
    BaseElement
    BaseLoadingElement
"""

import abc
import logging
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class BaseMethods(metaclass=abc.ABCMeta):
    """Methods used by all Page Objects"""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self._locators = dict()
        return

    def element_exists(self, locator: dict, scope: str = None) -> bool:
        try:
            self.find_element(locator=locator, scope=scope)
        except NoSuchElementException:
            return False
        else:
            return True

    def element_exists_and_is_displayed(self, locator: dict, scope: str = None) -> bool:
        # This seems obvious enough to not warrant its own method.
        #   However, calling _element_is_displayed() first could raise an unexpected exception.
        if not self.element_exists(locator=locator, scope=scope):
            return False
        return self.find_element(locator=locator, scope=scope).is_displayed()

    def find_element(self, locator: dict, scope: str = None) -> WebElement:
        """
        Finds a WebElement at the given locator.

        :param locator: Locator of the WebElement.
        :param scope: Determines scope of search. Can be 'driver' or 'element'.
            if 'driver': self.driver.find_element() is executed.
            if 'element': self.element.find_element() is executed.
        :return: WebElement.
        """
        self._verify_scope_param(scope=scope)
        if scope:
            scope = scope.lower()

        if (scope == 'driver') or (not scope and isinstance(self, BasePage)):
            return self.driver.find_element(by=locator['by'], value=locator['value'])
        elif (scope == 'element') or (not scope and isinstance(self, BaseElement)):
            return self.element.find_element(by=locator['by'], value=locator['value'])
        else:
            log_str = f"Unhandled exception in .find_element(). scope={scope}, type(self)={type(self)}"
            logging.error(log_str)
            raise Exception(log_str)

    def find_elements(self, locator: dict, scope: str = None) -> list[WebElement]:
        """
        Finds multiple WebElements at the given locator.

        :param locator: Locator of the WebElements.
        :param scope: Determines scope of search. Can be 'driver' or 'element'.
            if 'driver': self.driver.find_elements() is executed.
            if 'element': self.element.find_elements() is executed.
        :return: list of WebElements.
        """
        self._verify_scope_param(scope=scope)
        if scope:
            scope = scope.lower()

        if (scope == 'driver') or (not scope and isinstance(self, BasePage)):
            return self.driver.find_elements(by=locator['by'], value=locator['value'])
        elif (scope == 'element') or (not scope and isinstance(self, BaseElement)):
            return self.element.find_elements(by=locator['by'], value=locator['value'])
        else:
            log_str = f"Unhandled exception in .find_elements(). scope={scope}, type(self)={type(self)}"
            logging.error(log_str)
            raise Exception(log_str)

    def mouseover(self, element: WebElement) -> None:
        ActionChains(self.driver).move_to_element(element).perform()
        return

    @staticmethod
    def _verify_scope_param(scope: str) -> None:
        if scope:
            scope = scope.lower()
            if scope not in ['driver', 'element']:
                log_str = f"Invalid scope param value '{scope}'. Must be one of ['driver', 'element', None]."
                logging.error(log_str)
                raise ValueError(log_str)


class BaseLoadingMethods(BaseMethods, metaclass=abc.ABCMeta):
    """Methods used by Page Objects which have a loading state."""

    @abc.abstractmethod
    def is_loaded(self) -> bool:
        """Criteria to determine when the element is deemed loaded"""
        pass

    def wait_until_loaded(self, timeout: float = 5.0, must_load: bool = True) -> None:
        end_time = time.time() + timeout
        while time.time() < end_time:
            time.sleep(0.5)
            if self.is_loaded():
                return
        if must_load is True:
            log_str = f"'{self}' did not load."
            logging.error(log_str)
            raise TimeoutError(log_str)


class BasePage(BaseLoadingMethods, metaclass=abc.ABCMeta):

    def __init__(self, driver: WebDriver, url: str = None) -> None:
        super().__init__(driver=driver)
        self._url = url
        return

    def load_page(self) -> None:
        if not self._url:
            log_str = 'No URL was specified when this object was created.'
            logging.error(log_str)
            raise ValueError(log_str)

        self.driver.get(url=self._url)
        self.wait_until_loaded()
        return


class BaseElement(BaseMethods):

    def __init__(self, element: WebElement) -> None:
        super().__init__(driver=element.parent)
        self.element = element
        return


class BaseLoadingElement(BaseLoadingMethods, BaseElement, metaclass=abc.ABCMeta):
    pass
