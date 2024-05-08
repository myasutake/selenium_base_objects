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
from typing import Optional, TypedDict

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class Locator(TypedDict):
    """
    Locators used to find elements.

    The base classes defined below are using a slightly modified version of
    Selenium's built-in find_element() and find_elements() methods.

    Selenium's built-in methods require two arguments:
        'by': search type (e.g. by id, xpath, css selector, etc.)
        'value': value of the search type (e.g. the actual id, xpath, css selector, etc.)

    But Selenium also needs to know how the search is being executed:
        webdriver.find_element(by, value) -OR-
        webelement.find_element(by, value)

    So we really need a third argument to provide the scope of the search:
        'scope': 'driver' or 'element'
    """
    scope: str
    by: str
    value: str


class BaseMethods(metaclass=abc.ABCMeta):
    """Methods used by all Page Objects"""

    def __init__(self, driver: WebDriver, element: Optional[WebElement] = None) -> None:
        self._driver = driver
        self._element = element
        self._locators = dict()
        self._name = ''
        return

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @property
    def element(self) -> WebElement:
        return self._element

    def element_exists(self, locator: Locator) -> bool:
        try:
            self.find_element(locator=locator)
        except NoSuchElementException:
            return False
        else:
            return True

    def element_exists_and_is_displayed(self, locator: Locator) -> bool:
        # This seems obvious enough to not warrant its own method.
        #   However, calling _element_is_displayed() first could raise an unexpected exception.
        if not self.element_exists(locator=locator):
            return False
        return self.find_element(locator=locator).is_displayed()

    def find_element(self, locator: Locator) -> WebElement:
        """
        Finds a WebElement at the given locator.
        """
        self._verify_scope_param(scope=locator['scope'])
        locator['scope'] = locator['scope'].lower()

        if locator['scope'] == 'driver':
            return self.driver.find_element(by=locator['by'], value=locator['value'])
        elif locator['scope'] == 'element':
            return self.element.find_element(by=locator['by'], value=locator['value'])
        else:
            log_str = f"Unhandled exception in .find_element(). scope={locator['scope']}"
            logging.error(log_str)
            raise Exception(log_str)

    def find_elements(self, locator: Locator) -> list[WebElement]:
        """
        Finds multiple WebElements at the given locator.
        """
        self._verify_scope_param(scope=locator['scope'])
        locator['scope'] = locator['scope'].lower()

        if locator['scope'] == 'driver':
            return self.driver.find_elements(by=locator['by'], value=locator['value'])
        elif locator['scope'] == 'element':
            return self.element.find_elements(by=locator['by'], value=locator['value'])
        else:
            log_str = f"Unhandled exception in .find_elements(). scope={locator['scope']}"
            logging.error(log_str)
            raise Exception(log_str)

    def mouseover(self, element: WebElement) -> None:
        ActionChains(self.driver).move_to_element(element).perform()
        return

    @staticmethod
    def _verify_scope_param(scope: str) -> None:
        log_str = f"Invalid scope param value '{scope}'. Must be one of ['driver', 'element']."

        if not scope:
            logging.error(log_str)
            raise TypeError(log_str)

        scope = scope.lower()
        if scope not in ['driver', 'element']:
            logging.error(log_str)
            raise ValueError(log_str)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        return

    def __repr__(self) -> str:
        return f'{self.__class__}'

    def __str__(self) -> str:
        return self.name


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

        logging.debug(f'Navigating to {self}...')
        self.driver.get(url=self._url)
        self.wait_until_loaded()
        return


class BaseElement(BaseMethods):

    def __init__(self, element: WebElement) -> None:
        super().__init__(driver=element.parent, element=element)
        return

    @property
    def element_to_click(self) -> WebElement:
        """
        Most of the time, you want BaseElement.click() to click itself.

        Sometimes, you might want to click something else. In such a case, have
        your subclass override this method.
        """
        return self.element

    def click(self, scroll_into_view: bool = False, scroll_align_top: bool = True, scroll_vertical_offset: int = 0) -> None:
        """
        Clicks the element.

        If the element is covered up by another element, it may result in an
        ElementClickIntercepted exception. Try calling this method with
        scroll_into_view = True.

        scroll_align_top will scroll until the element to click is either at the
        top or bottom of the window. scroll_vertical_offset will then scroll
        the specified amount of pixels before clicking the element.
        """
        if scroll_into_view:
            if scroll_align_top:
                top_or_bottom = 'top'
            else:
                top_or_bottom = 'bottom'
            logging.debug(f"Scrolling {self} into view, aligning to {top_or_bottom}...")
            self.driver.execute_script(f"arguments[0].scrollIntoView({str(scroll_align_top).lower()});",
                                       self.element_to_click)

            if scroll_vertical_offset != 0:
                if scroll_vertical_offset < 0:
                    up_or_down = 'up'
                else:
                    up_or_down = 'down'
                logging.debug(f"Scrolling {up_or_down} {abs(scroll_vertical_offset)} pixels...")
                self.driver.execute_script(f"scrollBy(0, {scroll_vertical_offset})")

            # Delay before clicking
            #   Sometimes the scroll needs time to finish, despite what it seems.
            time.sleep(0.5)

        logging.info(f"Clicking {self}...")
        self.element_to_click.click()
        time.sleep(0.5)
        return

    def highlight(self, duration=3):
        """
        Highlights the element. Used for debugging purposes. Make sure your locators are good!
        """
        # Store original style so it can be reset later
        original_style = self.element.get_attribute("style")

        end_time = time.time() + duration
        while time.time() < end_time:
            # Style element with dashed red border
            self.driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])",
                                       self.element,
                                       "style",
                                       "border: 2px solid red; border-style: dashed;")
            time.sleep(0.2)
            # Revert
            self.driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])",
                                       self.element,
                                       "style",
                                       original_style)
            time.sleep(0.2)


class BaseLoadingElement(BaseLoadingMethods, BaseElement, metaclass=abc.ABCMeta):
    pass


class BaseOpenCloseElement(BaseElement, metaclass=abc.ABCMeta):
    """
    Used for an element that has an opened/closed state.

    Also works for expanded/collapsed.
    """

    @abc.abstractmethod
    def is_closed(self) -> bool:
        """Criteria to determine if the element is deemed closed."""
        pass

    @abc.abstractmethod
    def is_open(self) -> bool:
        """Criteria to determine if the element is deemed open."""
        pass

    # These two methods do not need to be defined - a user may not have the option
    #   to open/close an element; it may be open/closed based on some other input.
    #   But because a user option usually exists, I'm including the methods'
    #   prototypes here.
    #
    def close(self) -> None:
        # user action to close the element (e.g. click on the menu icon)
        # wait_until_closed()
        raise NotImplementedError

    def open(self) -> None:
        # user action to open the element (e.g. click on the menu icon)
        # wait_until_opened()
        raise NotImplementedError

    def wait_until_closed(self, timeout: float = 5.0, must_close: bool = True) -> None:
        end_time = time.time() + timeout
        while time.time() < end_time:
            time.sleep(0.5)
            if self.is_closed():
                return
        if must_close is True:
            log_str = f"'{self}' did not close."
            logging.error(log_str)
            raise TimeoutError(log_str)

    def wait_until_open(self, timeout: float = 5.0, must_open: bool = True) -> None:
        end_time = time.time() + timeout
        while time.time() < end_time:
            time.sleep(0.5)
            if self.is_open():
                return
        if must_open is True:
            log_str = f"'{self}' did not open."
            logging.error(log_str)
            raise TimeoutError(log_str)

    # The following methods are just wrappers. They can read easier for elements that
    #   open/close differently, e.g. an accordion-type element that expands/collapses.from

    def collapse(self) -> None:
        self.close()
        return

    def expand(self) -> None:
        self.open()
        return

    def is_collapsed(self) -> bool:
        return self.is_closed()

    def is_expanded(self) -> bool:
        return self.is_open()

    def wait_until_collapsed(self, timeout: float = 5.0, must_collapse: bool = True) -> None:
        self.wait_until_closed(timeout=timeout, must_close=must_collapse)
        return

    def wait_until_expanded(self, timeout: float = 5.0, must_expand: bool = True) -> None:
        self.wait_until_open(timeout=timeout, must_open=must_expand)
        return
