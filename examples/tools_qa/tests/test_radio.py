import logging.config

import pytest

import examples.tools_qa.page_objects.elements.radio_button
import misc.logging_config

logging.config.dictConfig(misc.logging_config.config)


@pytest.fixture(scope='function')
def navigate_to_page(launch_chrome) -> examples.tools_qa.page_objects.elements.radio_button.Page:
    driver = launch_chrome
    page = examples.tools_qa.page_objects.elements.radio_button.Page(driver=driver)
    page.load_page()
    return page


class TestInit:

    @staticmethod
    def test_no_selection_on_init(navigate_to_page) -> None:
        radio_page = navigate_to_page
        assert radio_page.selected_radio_button is None
        return

    @staticmethod
    def test_no_results_text_on_init(navigate_to_page) -> None:
        radio_page = navigate_to_page
        assert radio_page.results_text is None
        return


class TestHappyPaths:

    @staticmethod
    def test_yes_result_text(navigate_to_page) -> None:
        radio_page = navigate_to_page

        radio_page.selected_radio_button = 'Yes'

        expected_result_text = 'You have selected Yes'
        actual_result_text = radio_page.results_text

        assert radio_page.selected_radio_button == 'Yes'
        assert actual_result_text == expected_result_text
        return

    @staticmethod
    def test_impressive_result_text(navigate_to_page) -> None:
        radio_page = navigate_to_page

        radio_page.selected_radio_button = 'Impressive'

        expected_result_text = 'You have selected Impressive'
        actual_result_text = radio_page.results_text

        assert radio_page.selected_radio_button == 'Impressive'
        assert actual_result_text == expected_result_text
        return


class TestDisabledButton:

    @staticmethod
    def test_clicking_no_doesnt_select_it(navigate_to_page) -> None:
        radio_page = navigate_to_page

        radio_page.selected_radio_button = 'No'

        assert radio_page.selected_radio_button is None
        return

    @staticmethod
    def test_clicking_no_results_in_no_text(navigate_to_page) -> None:
        radio_page = navigate_to_page

        radio_page.selected_radio_button = 'No'

        assert radio_page.results_text is None
        return

    @staticmethod
    def test_clicking_no_doesnt_update_after_other_selection(navigate_to_page) -> None:
        radio_page = navigate_to_page

        radio_page.selected_radio_button = 'Yes'
        radio_page.selected_radio_button = 'No'

        expected_result_text = 'You have selected Yes'
        actual_result_text = radio_page.results_text

        assert radio_page.selected_radio_button == 'Yes'
        assert actual_result_text == expected_result_text
