"""
Classes used for common HTML elements.
"""

import abc
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import page_objects.base


class CanDisable(page_objects.base.BaseElement, metaclass=abc.ABCMeta):

    def __init__(self, element: WebElement) -> None:
        super().__init__(element=element)
        return

    def is_disabled(self) -> bool:
        if self.element.get_attribute('disabled') == 'true':
            return True
        else:
            return False


class Checkbox(page_objects.base.BaseElement):
    """
    <input type="checkbox">
    """

    def __init__(self, element: WebElement) -> None:
        super().__init__(element=element)
        self._name = 'Checkbox'
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

    # I would define a method that returns the label, but there's no standard DOM structure for that.


class Dropdown(CanDisable):
    """
    <select>
    """

    def __init__(self, element: WebElement) -> None:
        super().__init__(element=element)
        self._locators['options'] = {'scope': 'element', 'by': By.CSS_SELECTOR, 'value': 'option'}
        self._name = 'Dropdown'
        return

    # Get/Set Options

    @property
    def options(self) -> list[str]:
        options_list = []
        for i in self._get_options():
            options_list.append(i.text)

        log_str = f"Options for {self}:"
        for i in options_list:
            log_str += f'\n    {i}'
        logging.debug(log_str)

        return options_list

    @property
    def selected_option(self) -> str:
        for i_option in self._get_options():
            if i_option.is_selected():
                log_str = f"'{i_option.text}' currently selected for {self}."
                logging.debug(log_str)
                return i_option.text

        log_str = f"{self} has no option selected. (How is this possible???)"
        logging.error(log_str)
        raise Exception(log_str)

    @selected_option.setter
    def selected_option(self, value: str) -> None:
        self._verify_no_duplicate_options()

        for i_option in self._get_options():
            if i_option.text == value:
                i_option.click()
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

    def _get_options(self) -> list['Option']:
        elements_list = self.find_elements(locator=self._locators['options'])
        options_list = []
        for i in elements_list:
            options_list.append(Option(element=i))
        return options_list

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


class InputText(CanDisable):
    """
    <input type="text">
    """

    def __init__(self, element: WebElement) -> None:
        super().__init__(element=element)
        self._name = 'Input Text Field'
        return

    @property
    def value(self) -> str:
        return self.element.get_attribute('value')

    @value.setter
    def value(self, input_: str) -> None:
        self.element.send_keys(input_)
        return


class Option(CanDisable):
    """
    <option>
    """

    def __init__(self, element: WebElement) -> None:
        super().__init__(element=element)
        self._name = f"Option: '{self.text}'"
        return

    def is_selected(self) -> bool:
        if self.element.get_attribute('selected') == 'true':
            return True
        else:
            return False

    @property
    def text(self) -> str:
        return self.element.text

    def click(self, scroll_into_view: bool = False) -> None:
        if self.is_selected():
            log_str = f"Option '{self}' is already selected."
            logging.debug(log_str)
        if self.is_disabled():
            log_str = f"Option '{self}' is disabled."
            logging.warning(log_str)
        if scroll_into_view:
            logging.debug(f"Scrolling {self} into view...")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element)
        logging.info(f"Clicking '{self}'...")
        self.element.click()
        return
