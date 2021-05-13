import logging
import time

from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from page_objects.base import BaseElement
from page_objects.base import BasePage


class PokedexPage(BasePage):

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver=driver, url='https://www.pokemon.com/us/pokedex/', desc='Pokedex Page')
        self._locators['nav_main'] = {'by': By.CSS_SELECTOR, 'value': 'nav.main'}
        self._locators['accept_cookies_button'] = {'by': By.ID, 'value': 'onetrust-accept-btn-handler'}
        self._locators['sort_dropdown'] = {'by': By.CSS_SELECTOR, 'value': 'section.overflow-visible > div > div > div.custom-select-menu'}
        self._locators['search_result'] = {'by': By.CSS_SELECTOR, 'value': 'li.animating'}
        return

    # Basic Filters

    def find_sort_dropdown(self) -> 'SortDropdown':
        return SortDropdown(element=self.find_element(locator=self._locators['sort_dropdown']))

    # Search Results

    def all_search_results_names(self) -> list[str]:
        results = self.find_search_results()
        return [i.name for i in results]

    def all_search_results_numbers_as_ints(self) -> list[int]:
        results = self.find_search_results()
        return [i.number_as_int for i in results]

    def find_search_results(self) -> list['SearchResult']:
        elements = self.find_elements(locator=self._locators['search_result'])
        return [SearchResult(element=i) for i in elements]

    # Cookie dialog

    def cookies_dialog_is_displayed(self) -> bool:
        return self.element_exists_and_is_displayed(locator=self._locators['accept_cookies_button'])

    def accept_cookies(self) -> None:
        self.find_element(locator=self._locators['accept_cookies_button']).click()
        return

    # Misc

    def is_loaded(self) -> bool:
        return self.element_exists_and_is_displayed(locator=self._locators['nav_main'])


class SortDropdown(BaseElement):

    def __init__(self, element):
        super().__init__(element=element, desc='Sort Dropdown')
        self._locators['current_option'] = {'by': By.CSS_SELECTOR, 'value': 'label'}
        self._locators['option'] = {'by': By.CSS_SELECTOR, 'value': 'li'}
        return

    # Displaying Options

    def click_dropdown(self) -> None:
        self._element.click()
        time.sleep(0.1)
        return

    def display_options(self) -> None:
        if self.options_are_displayed():
            logging.debug('Options are already displayed. No action needed.')
            return
        self.click_dropdown()
        return

    def options_are_displayed(self) -> bool:
        current_option_element = self.find_element(locator=self._locators['current_option'])
        class_attributes = current_option_element.get_attribute(name='class')
        return 'opened' in class_attributes

    def _verify_options_are_displayed(self) -> None:
        if not self.options_are_displayed():
            log_str = "Options are not displayed."
            logging.error(log_str)
            raise ElementNotVisibleException(log_str)
        return

    # Setting/Getting Options

    def click_option(self, option: str) -> None:
        self._verify_options_are_displayed()
        self._find_option_element(option=option).click()
        return

    def _find_option_element(self, option: str) -> WebElement:
        self._verify_options_are_displayed()

        elements = self.find_elements(self._locators['option'])
        for i in elements:
            if option.lower() == i.text.lower():
                return i

        log_str = f"Invalid option '{option}' specified."
        logging.error(log_str)
        raise ValueError(log_str)

    @property
    def selected_option(self) -> str:
        element = self.find_element(locator=self._locators['current_option'])
        return element.text

    @selected_option.setter
    def selected_option(self, option: str) -> None:
        self.display_options()
        self.click_option(option=option)
        return


class SearchResult(BaseElement):

    def __init__(self, element: WebElement) -> None:
        super().__init__(element=element)
        self._locators['name'] = {'by': By.CSS_SELECTOR, 'value': 'h5'}
        self._locators['number'] = {'by': By.CSS_SELECTOR, 'value': 'p.id'}
        self._desc = f"Search Result - {self.number_as_str} {self.name}"
        return

    @property
    def name(self) -> str:
        element = self.find_element(locator=self._locators['name'])
        return element.text

    @property
    def number_as_str(self) -> str:
        element = self.find_element(locator=self._locators['number'])
        return element.text

    @property
    def number_as_int(self) -> int:
        return int(self.number_as_str.strip('#'))
