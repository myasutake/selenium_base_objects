"""
Classes used for common HTML elements.
"""

import time

from selenium.webdriver.remote.webelement import WebElement

import page_objects.base


class Checkbox(page_objects.base.BaseElement):

    def __init__(self, element: WebElement, desc: str = 'Checkbox') -> None:
        super().__init__(element=element, desc=desc)
        return

    @property
    def checked(self) -> bool:
        checked_attribute = self.element.get_attribute('checked')
        return bool(checked_attribute)

    @checked.setter
    def checked(self, value: bool) -> None:
        if self.checked != value:
            self.click()
        return

    def click(self) -> None:
        self.element.click()
        time.sleep(0.5)
        return

    # I would define a method that returns the label, but there's no standard DOM structure for that.
