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
        self._locators['search_result'] = {'by': By.CSS_SELECTOR, 'value': 'li.animating'}
        return

    def cookies_dialog_is_displayed(self) -> bool:
        return self.element_exists_and_is_displayed(locator=self._locators['accept_cookies_button'])

    def accept_cookies(self) -> None:
        self._click_element(locator=self._locators['accept_cookies_button'])
        return

    def find_search_results(self) -> list['SearchResult']:
        elements = self._find_elements(locator=self._locators['search_result'])
        return [SearchResult(element=i) for i in elements]

    def is_loaded(self) -> bool:
        return self.element_exists_and_is_displayed(locator=self._locators['nav_main'])


class SearchResult(BaseElement):

    def __init__(self, element: WebElement) -> None:
        super().__init__(element=element)
        self._locators['name'] = {'by': By.CSS_SELECTOR, 'value': 'h5'}
        self._locators['number'] = {'by': By.CSS_SELECTOR, 'value': 'p.id'}
        self._desc = f"Search Result - {self.number_as_str} {self.name}"
        return

    @property
    def name(self) -> str:
        return self._text_of_element_at(self._locators['name'])

    @property
    def number_as_str(self) -> str:
        return self._text_of_element_at(self._locators['number'])

    @property
    def number_as_int(self) -> int:
        return int(self.number_as_str.strip('#'))

    def is_loaded(self) -> bool:
        return self._is_displayed()
