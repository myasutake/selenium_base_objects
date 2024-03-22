import logging
import time

import page_objects.base

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class Page(page_objects.base.BasePage):

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self._url = 'https://the-internet.herokuapp.com/checkboxes'
        self._locators['checkboxes'] = {'by': By.CSS_SELECTOR, 'value': '#checkboxes > input[type="checkbox"]'}
        return

    # States

    def checkbox_1_is_checked(self) -> bool:
        element = self.get_checkbox_1_element()
        checked_attribute = element.get_attribute('checked')
        return bool(checked_attribute)

    def checkbox_2_is_checked(self) -> bool:
        element = self.get_checkbox_2_element()
        checked_attribute = element.get_attribute('checked')
        return bool(checked_attribute)

    # Actions

    def click_checkbox_1(self) -> None:
        element = self.get_checkbox_1_element()
        logging.info('Clicking Checkbox 1...')
        element.click()
        time.sleep(0.5)
        return

    def click_checkbox_2(self) -> None:
        element = self.get_checkbox_2_element()
        logging.info('Clicking Checkbox 2...')
        element.click()
        time.sleep(0.5)
        return

    # Misc

    def is_loaded(self) -> bool:
        checkbox_1_element = self.get_checkbox_1_element()
        checkbox_2_element = self.get_checkbox_2_element()
        if not checkbox_1_element.is_displayed():
            return False
        return checkbox_2_element.is_displayed()

    def get_checkbox_1_element(self) -> WebElement:
        elements = self.find_elements(locator=self._locators['checkboxes'], scope='driver')
        return elements[0]

    def get_checkbox_2_element(self) -> WebElement:
        elements = self.find_elements(locator=self._locators['checkboxes'], scope='driver')
        return elements[1]

    def __str__(self) -> str:
        return 'Checkboxes Page'
