import page_objects.base
import page_objects.common

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class Page(page_objects.base.BasePage):

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self._url = 'https://demoqa.com/text-box'
        self._locators['side_nav'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': 'div.left-pannel'}  # 'pannel' is not a typo
        self._locators['title'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': 'h1.text-center'}
        self._name = 'Elements/Text Box Page'
        return

    def get_side_nav(self) -> 'SideNav':
        element = self.find_element(locator=self._locators['side_nav'])
        return SideNav(element)

    def is_loaded(self) -> bool:
        title_element = self.find_element(locator=self._locators['title'])
        return title_element.is_displayed()


class SideNav(page_objects.base.BaseElement):

    def __init__(self, element: WebElement) -> None:
        super().__init__(element=element)
