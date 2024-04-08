import page_objects.base
import examples.tools_qa.page_objects.common

from selenium.webdriver.remote.webdriver import WebDriver


class Page(examples.tools_qa.page_objects.common.Page):

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self._url = 'https://demoqa.com/broken'
        self._name = 'Elements/Broken-Links_Images Page'
        return

    def is_loaded(self) -> bool:
        title_element = self.find_element(locator=self._locators['title'])
        if not title_element.is_displayed():
            return False
        return title_element.text == 'Broken Links - Images'
