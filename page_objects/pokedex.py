from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.base import BasePage


class PokedexPage(BasePage):

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver=driver, url='https://www.pokemon.com/us/pokedex/', desc='Pokedex Page')
        self._locators['nav_main'] = {'by': By.CSS_SELECTOR, 'value': 'nav.main'}
        return

    def is_loaded(self) -> bool:
        locator = self._locators['nav_main']
        return self.element_exists(locator) and self._element_is_displayed(locator)
