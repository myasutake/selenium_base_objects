import logging

import page_objects.base
import page_objects.common

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class Page(page_objects.base.BasePage):

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self._url = 'https://the-internet.herokuapp.com/dropdown'
        self._locators['dropdown'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': '#dropdown'}
        self._desc = 'Dropdown Page'
        return

    def current_selection(self) -> str:
        dd = self._get_dropdown()
        return dd.selected_option

    def set_selection(self, option: str) -> None:
        dd = self._get_dropdown()
        dd.selected_option = option
        return

    # Misc

    def is_loaded(self) -> bool:
        dd = self._get_dropdown()
        if not dd.element.is_displayed():
            log_str = f'{self} not yet loaded; {dd} not displayed...'
            logging.debug(log_str)
            return False
        log_str = f'{self} loaded.'
        logging.debug(log_str)
        return True

    def _get_dropdown(self) -> page_objects.common.Dropdown:
        element = self.find_element(locator=self._locators['dropdown'])
        return page_objects.common.Dropdown(element=element, desc='Dropdown')
