import page_objects.base
import page_objects.common
import examples.tools_qa.page_objects.common

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class Page(examples.tools_qa.page_objects.common.Page):

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self._url = 'https://demoqa.com/radio-button'
        self._name = 'Elements/Radio-Button Page'
        self._locators['radio_divs'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': 'div.custom-radio'}
        self._locators['radio_buttons'] = {'scope': 'element', 'by': By.CSS_SELECTOR, 'value': 'input'}
        self._locators['radio_labels'] = {'scope': 'element', 'by': By.CSS_SELECTOR, 'value': 'label'}
        return

    # Radio

    @property
    def selected_radio_button(self) -> str:
        return self._get_radio_button_group().selected_radio_button

    @selected_radio_button.setter
    def selected_radio_button(self, label: str) -> None:
        self._get_radio_button_group().selected_radio_button = label
        return

    # Misc

    def _get_radio_button_group(self) -> page_objects.common.RadioGroup:
        return page_objects.common.RadioGroup(radio_list=self._get_radio_buttons())

    def _get_radio_buttons(self) -> list['Radio']:
        radio_buttons = []
        radio_div_elements = self.find_elements(locator=self._locators['radio_divs'])
        radio_divs = [page_objects.base.BaseElement(element=i) for i in radio_div_elements]
        for i_radio_div in radio_divs:
            i_radio_button_element = i_radio_div.find_element(locator=self._locators['radio_buttons'])
            i_radio_label_element = i_radio_div.find_element(locator=self._locators['radio_labels'])
            i_radio = Radio(input_element=i_radio_button_element, text_element=i_radio_label_element)
            radio_buttons.append(i_radio)
        return radio_buttons

    def is_loaded(self) -> bool:
        title_element = self.find_element(locator=self._locators['title'])
        if not title_element.is_displayed():
            return False
        return title_element.text == 'Radio Button'


class Radio(page_objects.common.Radio):

    def __init__(self, input_element: WebElement, text_element: WebElement) -> None:
        super().__init__(input_element=input_element, text_element=text_element)
        return

    @property
    def element_to_click(self) -> WebElement:
        # Clicking the input element gets intercepted for some stupid reason.
        #   Clicking the label seems to work.
        return self._text_element
