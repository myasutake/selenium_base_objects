"""
Classes used for common HTML elements.
"""

import logging
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import page_objects.base


class Checkbox(page_objects.base.BaseElement):
    """
    <input type="checkbox">
    """

    def __init__(self, element: WebElement, desc: str = 'Checkbox') -> None:
        super().__init__(element=element, desc=desc)
        return

    @property
    def checked(self) -> bool:
        checked_attribute = self.element.get_attribute('checked')
        log_str = f'{self} value: {bool(checked_attribute)}.'
        logging.debug(log_str)
        return bool(checked_attribute)

    @checked.setter
    def checked(self, value: bool) -> None:
        if self.checked != value:
            self.click()
        else:
            log_str = f'{self} value already {value}; no need to click.'
            logging.debug(log_str)
        return

    def click(self) -> None:
        logging.info(f'Clicking {self}...')
        self.element.click()
        time.sleep(0.5)
        return

    # I would define a method that returns the label, but there's no standard DOM structure for that.


class Dropdown(page_objects.base.BaseElement):
    """
    <select>
    """

    def __init__(self, element: WebElement, desc: str = 'Dropdown') -> None:
        super().__init__(element=element, desc=desc)
        self._locators['options'] = {'by': By.CSS_SELECTOR, 'value': 'option'}
        return

    # Get/Set Options

    @property
    def options(self) -> list[str]:
        options_list = []
        for i in self._find_options_elements():
            options_list.append(i.text)

        log_str = f"Options for {self}:"
        for i in options_list:
            log_str += f'\n    {i}'
        logging.debug(log_str)

        return options_list

    @property
    def selected_option(self) -> str:
        for i_option_element in self._find_options_elements():
            if self._option_is_selected(element=i_option_element):
                log_str = f"'{i_option_element.text}' currently selected for {self}."
                logging.debug(log_str)
                return i_option_element.text
        log_str = f"{self} has no option selected. (How is this possible???)"
        logging.error(log_str)
        raise Exception(log_str)

    @selected_option.setter
    def selected_option(self, value: str) -> None:
        self._verify_no_duplicate_options()

        for i_option_element in self._find_options_elements():
            if i_option_element.text == value:
                if self._option_is_selected(element=i_option_element):
                    log_str = f"Option '{value}' is already selected."
                    logging.debug(log_str)
                if self._option_is_disabled(element=i_option_element):
                    log_str = f"Option '{value}' is disabled."
                    logging.warning(log_str)
                logging.info(f"Clicking '{value}'...")
                i_option_element.click()
                time.sleep(0.5)
                return

        log_str = f"Option '{value}' not found for {self}."
        logging.error(log_str)
        raise ValueError(log_str)

    # Misc

    def _contains_duplicate_options(self) -> bool:
        i = self.options
        if len(i) != len(set(i)):
            log_str = f'{self} contains duplicate options.'
            logging.warning(log_str)
            return True
        else:
            return False

    def _find_options_elements(self) -> list[WebElement]:
        return self.find_elements(locator=self._locators['options'], scope='element')

    def _find_option_element_with_text(self, text: str) -> WebElement:
        for i_element in self._find_options_elements():
            if i_element.text == text:
                return i_element
        log_str = f"Option '{text}' not found."
        logging.error(log_str)
        raise NoSuchElementException(log_str)

    @staticmethod
    def _option_is_disabled(element: WebElement) -> bool:
        if element.get_attribute('disabled') == 'true':
            return True
        else:
            return False

    @staticmethod
    def _option_is_selected(element: WebElement) -> bool:
        if element.get_attribute('selected') == 'true':
            return True
        else:
            return False

    def _verify_no_duplicate_options(self) -> None:
        if self._contains_duplicate_options():
            log_str = f'{self} contains duplicate options.'
            logging.error(log_str)
            raise ValueError(log_str)
        return
