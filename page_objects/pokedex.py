from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.base import BasePage


class PokedexPage(BasePage):

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver=driver, url='https://www.pokemon.com/us/pokedex/', desc='Pokedex Page')
        self._locators['nav_main'] = {'by': By.CSS_SELECTOR, 'value': 'nav.main'}
        self._locators['accept_cookies_button'] = {'by': By.ID, 'value': 'onetrust-accept-btn-handler'}
        return

    def cookies_dialog_is_displayed(self) -> bool:
        return self.element_exists_and_is_displayed(locator=self._locators['accept_cookies_button'])

    def accept_cookies(self) -> None:
        self._click_element(locator=self._locators['accept_cookies_button'])
        return

    def is_loaded(self) -> bool:
        return self.element_exists_and_is_displayed(locator=self._locators['nav_main'])
