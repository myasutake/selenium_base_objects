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
        self._locators['group'] = {'scope': 'element', 'by': By.CSS_SELECTOR, 'value': 'div.element-group'}
        self._name = 'Side Nav'
        return

    def _get_nav_groups(self) -> list['SideNavGroup']:
        groups = []
        for i in self.find_elements(locator=self._locators['group']):
            groups.append(SideNavGroup(element=i))
        return groups


class SideNavGroup(page_objects.base.BaseOpenCloseElement):

    def __init__(self, element: WebElement) -> None:
        super().__init__(element=element)
        self._locators['header_button'] = {'scope': 'element', 'by': By.CSS_SELECTOR, 'value': 'span.group-header'}
        self._locators['link_list'] = {'scope': 'element', 'by': By.CSS_SELECTOR, 'value': 'div.element-list'}
        self._name = self.name
        return

    def is_closed(self) -> bool:
        link_list = self.find_element(locator=self._locators['link_list'])
        classes = link_list.get_attribute('class')
        return 'show' not in classes

    def is_open(self) -> bool:
        link_list = self.find_element(locator=self._locators['link_list'])
        classes = link_list.get_attribute('class')
        return 'show' in classes

    @property
    def name(self) -> str:
        header_element = self.find_element(locator=self._locators['header_button'])
        return header_element.text

    def __repr__(self) -> str:
        return f"{self.__class__} - '{self.name}'"

    def __str__(self) -> str:
        return f"Side Nav Group: '{self.name}'"
