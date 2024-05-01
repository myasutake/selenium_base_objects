import logging.config

import pytest

import examples.tools_qa.page_objects.elements.text_box
import misc.logging_config

logging.config.dictConfig(misc.logging_config.config)


@pytest.fixture(scope='function')
def navigate_to_page(launch_chrome) -> examples.tools_qa.page_objects.elements.text_box.Page:
    driver = launch_chrome
    page = examples.tools_qa.page_objects.elements.text_box.Page(driver=driver)
    page.load_page()
    return page


def test_no_submitted_data_displayed_on_init(navigate_to_page) -> None:
    text_box_page = navigate_to_page
    assert not text_box_page.submitted_name_field_is_visible()
    assert not text_box_page.submitted_email_field_is_visible()
    assert not text_box_page.submitted_current_address_field_is_visible()
    assert not text_box_page.submitted_permanent_address_field_is_visible()
    return


class TestHappyPaths:

    name_input = 'Alpha Bravo'
    expected_submitted_name = f'Name:Alpha Bravo'

    email_input = 'charlie@deltaecho.com'
    expected_submitted_email = f'Email:charlie@deltaecho.com'

    current_address_input = '123 Foxtrot\nGolf, HO 12345'
    expected_submitted_current_address = 'Current Address:123 Foxtrot Golf, HO 12345'  # Returns single space instead of newline, for some reason.

    permanent_address_input = '123 India\nJuliet, KI 12345'
    expected_submitted_permanent_address = 'Permanent Address:123 India Juliet, KI 12345'  # Returns single space instead of newline, for some reason.

    @classmethod
    def test_full_name(cls, navigate_to_page) -> None:
        text_box_page = navigate_to_page

        text_box_page.full_name_input = cls.name_input
        text_box_page.click_submit_button()

        assert text_box_page.submitted_name == cls.expected_submitted_name
        assert not text_box_page.submitted_email_field_is_visible()
        assert not text_box_page.submitted_current_address_field_is_visible()
        assert not text_box_page.submitted_permanent_address_field_is_visible()
        return

    @classmethod
    def test_email(cls, navigate_to_page) -> None:
        text_box_page = navigate_to_page

        text_box_page.email_input = cls.email_input
        text_box_page.click_submit_button()

        assert not text_box_page.submitted_name_field_is_visible()
        assert text_box_page.submitted_email == cls.expected_submitted_email
        assert not text_box_page.submitted_current_address_field_is_visible()
        assert not text_box_page.submitted_permanent_address_field_is_visible()
        return

    @classmethod
    @pytest.mark.xfail(reason='Name and email have spaces after the colon. Addr does not. Probably a bug.')
    def test_current_address(cls, navigate_to_page) -> None:
        text_box_page = navigate_to_page

        text_box_page.current_address_textarea = cls.current_address_input
        text_box_page.click_submit_button()

        assert not text_box_page.submitted_name_field_is_visible()
        assert not text_box_page.submitted_email_field_is_visible()
        assert text_box_page.submitted_current_address == cls.expected_submitted_current_address
        assert not text_box_page.submitted_permanent_address_field_is_visible()
        return

    @classmethod
    @pytest.mark.xfail(reason="Name and email have spaces after the colon. Addr does not. Probably a bug. 'Permanent' also misspelled.")
    def test_permanent_address(cls, navigate_to_page) -> None:
        text_box_page = navigate_to_page

        text_box_page.permanent_address_textarea = cls.permanent_address_input
        text_box_page.click_submit_button()

        assert not text_box_page.submitted_name_field_is_visible()
        assert not text_box_page.submitted_email_field_is_visible()
        assert not text_box_page.submitted_current_address_field_is_visible()
        assert text_box_page.submitted_permanent_address == cls.expected_submitted_permanent_address
        return
