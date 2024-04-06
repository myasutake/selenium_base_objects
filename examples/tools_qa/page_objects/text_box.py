import logging
import time

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
    """
    Represents the SideNav found on every page.

    The idea is to be able to get/do everything you need with this class since it
    encompasses the entirety of the nav. No need to get each individual SideNavGroup
    or SideNavLinkButton, etc.
    """

    def __init__(self, element: WebElement) -> None:
        super().__init__(element=element)
        self._locators['group'] = {'scope': 'element', 'by': By.CSS_SELECTOR, 'value': 'div.element-group'}
        self._name = 'Side Nav'
        return

    # Properties

    @property
    def collapsed_groups(self) -> list[str]:
        groups = []
        for i in self._get_nav_groups():
            if i.is_collapsed():
                groups.append(i.name)
        return groups

    @property
    def expanded_groups(self) -> list[str]:
        groups = []
        for i in self._get_nav_groups():
            if i.is_expanded():
                groups.append(i.name)
        return groups

    def group_is_collapsed(self, group_name: str) -> bool:
        group = self._get_nav_group(group_name=group_name)
        return group.is_collapsed()

    def group_is_expanded(self, group_name: str) -> bool:
        group = self._get_nav_group(group_name=group_name)
        return group.is_expanded()

    # Actions

    def click_group_header_button(self, group_name: str) -> None:
        nav_group = self._get_nav_group(group_name=group_name)
        nav_group.click_header_button()
        return

    def expand_group(self, group_name: str) -> None:
        nav_group = self._get_nav_group(group_name=group_name)
        nav_group.expand()
        return

    def collapse_group(self, group_name: str) -> None:
        nav_group = self._get_nav_group(group_name=group_name)
        nav_group.collapse()
        return

    # Misc

    def _get_nav_group(self, group_name: str) -> 'SideNavGroup':
        for i in self._get_nav_groups():
            if i.name.lower() == group_name.lower():
                return i
        log_str = f"No group found with name '{group_name}'."
        logging.error(log_str)
        raise ValueError(log_str)

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
        self._locators['link_button'] = {'scope': 'element', 'by': By.CSS_SELECTOR, 'value': 'li.btn'}
        self._name = self.name
        return

    # Properties

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
        header_button = self._get_header_button()
        return header_button.name

    # Actions

    def click_header_button(self) -> None:
        header_button = self._get_header_button()
        header_button.click(scroll_into_view=True)
        return

    def close(self) -> None:
        if self.is_closed():
            log_str = f"{self} already closed. Doing nothing."
            logging.debug(log_str)
        else:
            self.click_header_button()
            self.wait_until_closed()
        return

    def open(self) -> None:
        if self.is_open():
            log_str = f"{self} already open. Doing nothing."
            logging.debug(log_str)
        else:
            self.click_header_button()
            self.wait_until_open()
        return

    def click(self, scroll_into_view: bool = False) -> None:
        """
        Overwriting inherited method. Recommend not using this method.

        Use one of the following instead:
        * click_header_button() - contains no logic
        * open() or expand() - contains minimal logic
        * close() or collapse() - contains minimal logic
        """
        log_str = f"This object {self.__class__} represents the entire group (header and links buttons).\n"
        log_str += "  Clicking this element could produce an unexpected result.\n"
        log_str += f"  Recommend clicking {self._get_header_button().__class__} instead.\n"
        log_str += f"    Clicking {self} anyway..."
        logging.warning(log_str)
        self.element.click()
        time.sleep(0.5)
        return

    # Misc

    def _get_header_button(self) -> 'SideNavGroupHeaderButton':
        element = self.find_element(locator=self._locators['header_button'])
        return SideNavGroupHeaderButton(element=element)

    def _get_link_buttons(self) -> list['SideNavLinkButton']:
        elements = self.find_elements(locator=self._locators['link_button'])
        buttons = []
        for i in elements:
            buttons.append(SideNavLinkButton(element=i))
        return buttons

    def __repr__(self) -> str:
        return f"{self.__class__} - '{self.name}'"

    def __str__(self) -> str:
        return f"Side Nav Group: '{self.name}'"


class SideNavGroupHeaderButton(page_objects.base.BaseElement):

    def __init__(self, element: WebElement) -> None:
        super().__init__(element=element)
        self._name = self.name
        return

    @property
    def name(self) -> str:
        # For some reason this has a trailing newline and space, e.g. 'Elements\n '
        #   I can't imagine why we would ever need to reference that, so let's just
        #   strip it.
        return self.element.text.strip()

    def __repr__(self) -> str:
        return f"{self.__class__} - '{self.name}'"

    def __str__(self) -> str:
        return f"Side Nav Group Header Button: '{self.name}'"


class SideNavLinkButton(page_objects.base.BaseElement):

    def __init__(self, element: WebElement) -> None:
        super().__init__(element=element)
        self._name = self.name
        return

    @property
    def name(self) -> str:
        return self.element.text

    def __repr__(self) -> str:
        return f"{self.__class__} - '{self.name}'"

    def __str__(self) -> str:
        return f"Side Nav Link Button: '{self.name}'"
