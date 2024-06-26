from typing import Optional

import page_objects.base
import page_objects.common
import examples.tools_qa.page_objects.common

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class Page(examples.tools_qa.page_objects.common.Page):

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self._url = 'https://demoqa.com/text-box'
        self._name = 'Elements/Text-Box Page'
        self._locators['full_name_input'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': '#userName'}
        self._locators['email_input'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': '#userEmail'}
        self._locators['current_address_textarea'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': 'textarea#currentAddress'}
        self._locators['permanent_address_textarea'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': 'textarea#permanentAddress'}
        self._locators['submit_button'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': '#submit'}
        self._locators['submitted_name'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': '#name'}
        self._locators['submitted_email'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': '#email'}
        self._locators['submitted_current_address'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': 'p#currentAddress'}
        self._locators['submitted_permanent_address'] = {'scope': 'driver', 'by': By.CSS_SELECTOR, 'value': 'p#permanentAddress'}
        return

    # Properties

    #   Inputs

    @property
    def current_address_textarea(self) -> str:
        return self._get_current_address_textarea().value

    @current_address_textarea.setter
    def current_address_textarea(self, value: str) -> None:
        self._get_current_address_textarea().value = value
        return

    @property
    def email_input(self) -> str:
        return self._get_email_input().value

    @email_input.setter
    def email_input(self, value: str) -> None:
        self._get_email_input().value = value
        return

    @property
    def full_name_input(self) -> str:
        return self._get_full_name_input().value

    @full_name_input.setter
    def full_name_input(self, value: str) -> None:
        self._get_full_name_input().value = value
        return

    @property
    def permanent_address_textarea(self) -> str:
        return self._get_permanent_address_textarea().value

    @permanent_address_textarea.setter
    def permanent_address_textarea(self, value: str) -> None:
        self._get_permanent_address_textarea().value = value
        return

    #  Submitted Values

    @property
    def submitted_name(self) -> Optional[str]:
        if not self.submitted_name_field_is_visible():
            return None
        else:
            return self.find_element(locator=self._locators['submitted_name']).text

    @property
    def submitted_email(self) -> Optional[str]:
        if not self.submitted_email_field_is_visible():
            return None
        else:
            return self.find_element(locator=self._locators['submitted_email']).text

    @property
    def submitted_current_address(self) -> Optional[str]:
        if not self.submitted_current_address_field_is_visible():
            return None
        else:
            return self.find_element(locator=self._locators['submitted_current_address']).text

    @property
    def submitted_permanent_address(self) -> Optional[str]:
        if not self.submitted_permanent_address_field_is_visible():
            return None
        else:
            return self.find_element(locator=self._locators['submitted_permanent_address']).text

    def submitted_name_field_is_visible(self) -> bool:
        return self.element_exists_and_is_displayed(locator=self._locators['submitted_name'])

    def submitted_email_field_is_visible(self) -> bool:
        return self.element_exists_and_is_displayed(locator=self._locators['submitted_email'])

    def submitted_current_address_field_is_visible(self) -> bool:
        return self.element_exists_and_is_displayed(locator=self._locators['submitted_current_address'])

    def submitted_permanent_address_field_is_visible(self) -> bool:
        return self.element_exists_and_is_displayed(locator=self._locators['submitted_permanent_address'])

    # Actions

    def click_submit_button(self) -> None:
        self._get_submit_button().click(scroll_into_view=True)
        return

    # Misc

    def _get_current_address_textarea(self) -> page_objects.common.TextField:
        element = self.find_element(locator=self._locators['current_address_textarea'])
        textarea = page_objects.common.TextField(element=element)
        textarea.name = 'Text Area - Current Address'
        return textarea

    def _get_email_input(self) -> page_objects.common.TextField:
        element = self.find_element(locator=self._locators['email_input'])
        input_email = page_objects.common.TextField(element=element)
        input_email.name = 'Input Email'
        return input_email

    def _get_full_name_input(self) -> page_objects.common.TextField:
        element = self.find_element(locator=self._locators['full_name_input'])
        input_text = page_objects.common.TextField(element=element)
        input_text.name = 'Input Text - Full Name'
        return input_text

    def _get_permanent_address_textarea(self) -> page_objects.common.TextField:
        element = self.find_element(locator=self._locators['permanent_address_textarea'])
        textarea = page_objects.common.TextField(element=element)
        textarea.name = 'Text Area - Permanent Address'
        return textarea

    def _get_submit_button(self) -> page_objects.base.BaseElement:
        element = self.find_element(locator=self._locators['submit_button'])
        button = page_objects.base.BaseElement(element=element)
        button.name = 'Submit Button'
        return button

    def is_loaded(self) -> bool:
        title_element = self.find_element(locator=self._locators['title'])
        if not title_element.is_displayed():
            return False
        return title_element.text == 'Text Box'
