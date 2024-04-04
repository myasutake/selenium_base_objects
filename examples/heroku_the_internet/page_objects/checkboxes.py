import logging

import page_objects.base
import page_objects.common

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class Page(page_objects.base.BasePage):

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self._url = 'https://the-internet.herokuapp.com/checkboxes'
        self._locators['checkboxes'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': '#checkboxes > input[type="checkbox"]'}
        self._name = 'Checkboxes Page'
        return

    # States

    def checkbox_1_is_checked(self) -> bool:
        checkbox = self.get_checkbox_1()
        return checkbox.checked

    def checkbox_2_is_checked(self) -> bool:
        checkbox = self.get_checkbox_2()
        return checkbox.checked

    # Actions

    def click_checkbox_1(self) -> None:
        checkbox = self.get_checkbox_1()
        checkbox.click()
        return

    def click_checkbox_2(self) -> None:
        checkbox = self.get_checkbox_2()
        checkbox.click()
        return

    # Misc

    def is_loaded(self) -> bool:
        checkbox_1 = self.get_checkbox_1()
        checkbox_2 = self.get_checkbox_2()
        if not checkbox_1.element.is_displayed():
            log_str = f'{self} not yet loaded; {checkbox_1} not displayed...'
            logging.debug(log_str)
            return False
        if not checkbox_2.element.is_displayed():
            log_str = f'{self} not yet loaded; {checkbox_2} not displayed...'
            logging.debug(log_str)
            return False
        log_str = f'{self} loaded.'
        logging.debug(log_str)
        return True

    def get_checkbox_1(self) -> page_objects.common.Checkbox:
        elements = self.find_elements(locator=self._locators['checkboxes'])
        return page_objects.common.Checkbox(element=elements[0])

    def get_checkbox_2(self) -> page_objects.common.Checkbox:
        elements = self.find_elements(locator=self._locators['checkboxes'])
        return page_objects.common.Checkbox(element=elements[1])
