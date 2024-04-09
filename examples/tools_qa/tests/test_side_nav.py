import logging.config

import pytest
from selenium.common.exceptions import InvalidElementStateException

import examples.tools_qa.page_objects.alerts_frame_windows.browser_windows
import examples.tools_qa.page_objects.alerts_frame_windows.frames
import examples.tools_qa.page_objects.alerts_frame_windows.modal_dialogs
import examples.tools_qa.page_objects.common
import examples.tools_qa.page_objects.elements.check_box
import examples.tools_qa.page_objects.elements.links
import examples.tools_qa.page_objects.elements.radio_button
import examples.tools_qa.page_objects.interactions.draggable
import examples.tools_qa.page_objects.interactions.droppable
import examples.tools_qa.page_objects.interactions.resizable
import misc.logging_config

logging.config.dictConfig(misc.logging_config.config)


@pytest.fixture(scope='function')
def navigate_to_page(launch_chrome) -> examples.tools_qa.page_objects.common.Page:
    driver = launch_chrome
    page = examples.tools_qa.page_objects.common.Page(driver)
    page.load_page()
    return page


@pytest.fixture(scope='function')
def navigate_to_page_and_verify_initial_nav_state(navigate_to_page) -> examples.tools_qa.page_objects.common.SideNav:
    expected_expanded_nav_groups = ['Elements']

    page = navigate_to_page
    nav = page.get_side_nav()
    if nav.expanded_groups != expected_expanded_nav_groups:
        log_str = "Unexpected initial nav state.\n"
        log_str += f"  Expected expected groups: {expected_expanded_nav_groups}\n"
        log_str += f"  Actual expected groups:   {nav.expanded_groups}"
        logging.error(log_str)
        raise InvalidElementStateException(log_str)

    return nav


class TestGroups:

    @staticmethod
    def test_clicking_an_expanded_group_closes_it(navigate_to_page_and_verify_initial_nav_state) -> None:
        nav = navigate_to_page_and_verify_initial_nav_state

        group_name = 'Elements'
        nav.click_group_header_button(group_name=group_name)
        assert nav.group_is_collapsed(group_name=group_name)
        return

    @staticmethod
    def test_clicking_a_closed_group_expands_it(navigate_to_page_and_verify_initial_nav_state) -> None:
        nav = navigate_to_page_and_verify_initial_nav_state

        group_name = 'Forms'
        nav.click_group_header_button(group_name=group_name)
        assert nav.group_is_expanded(group_name=group_name)
        return

    @staticmethod
    def test_clicking_multiple_times(navigate_to_page_and_verify_initial_nav_state) -> None:
        nav = navigate_to_page_and_verify_initial_nav_state

        group_name = 'Elements'
        number_of_loops = 10

        for _ in range(number_of_loops):
            nav.click_group_header_button(group_name=group_name)
            assert nav.group_is_collapsed(group_name=group_name)
            nav.click_group_header_button(group_name=group_name)
            assert nav.group_is_expanded(group_name=group_name)

        return

    @staticmethod
    def test_max_one_expanded_group(navigate_to_page_and_verify_initial_nav_state) -> None:
        nav = navigate_to_page_and_verify_initial_nav_state

        click_sequence = ['Forms',
                          'Alerts, Frame & Windows',
                          'Widgets',
                          'Interactions',
                          'Book Store Application',
                          'Elements',
                          'Widgets',
                          'Interactions',
                          'Forms',
                          'Alerts, Frame & Windows']
        for i_group_name in click_sequence:
            nav.click_group_header_button(group_name=i_group_name)
            assert len(nav.expanded_groups) == 1

        return

    @staticmethod
    def test_no_expanded_groups_is_possible(navigate_to_page_and_verify_initial_nav_state) -> None:
        nav = navigate_to_page_and_verify_initial_nav_state
        nav.click_group_header_button(group_name='Elements')
        assert len(nav.expanded_groups) == 0
        return


class TestLinks:

    # I just picked three groups, three links from each group. Testing all is overkill, for demo purposes.

    # Setups

    @staticmethod
    @pytest.fixture(scope='function')
    def open_elements_group(navigate_to_page_and_verify_initial_nav_state) -> examples.tools_qa.page_objects.common.SideNav:
        nav = navigate_to_page_and_verify_initial_nav_state
        nav.expand_group(group_name='Elements')
        return nav

    @staticmethod
    @pytest.fixture(scope='function')
    def open_alerts_frame_windows_group(navigate_to_page_and_verify_initial_nav_state) -> examples.tools_qa.page_objects.common.SideNav:
        nav = navigate_to_page_and_verify_initial_nav_state
        nav.expand_group(group_name='Alerts, Frame & Windows')
        return nav

    @staticmethod
    @pytest.fixture(scope='function')
    def open_interactions_group(navigate_to_page_and_verify_initial_nav_state) -> examples.tools_qa.page_objects.common.SideNav:
        nav = navigate_to_page_and_verify_initial_nav_state
        nav.expand_group(group_name='Interactions')
        return nav

    # Elements

    @staticmethod
    def test_elements_check_box_link(open_elements_group) -> None:
        nav = open_elements_group
        driver = nav.driver
        check_box_page = examples.tools_qa.page_objects.elements.check_box.Page(driver=driver)

        nav.click_link_button(link_name='Check Box')
        check_box_page.wait_until_loaded()
        assert check_box_page.is_loaded()
        return

    @staticmethod
    def test_elements_radio_button_link(open_elements_group) -> None:
        nav = open_elements_group
        driver = nav.driver
        radio_button_page = examples.tools_qa.page_objects.elements.radio_button.Page(driver=driver)

        nav.click_link_button(link_name='Radio Button')
        radio_button_page.wait_until_loaded()
        assert radio_button_page.is_loaded()
        return

    @staticmethod
    def test_elements_links_link(open_elements_group) -> None:
        nav = open_elements_group
        driver = nav.driver
        links_page = examples.tools_qa.page_objects.elements.links.Page(driver=driver)

        nav.click_link_button(link_name='Links')
        links_page.wait_until_loaded()
        assert links_page.is_loaded()
        return

    # Alerts

    @staticmethod
    def test_alerts_browser_windows_link(open_alerts_frame_windows_group) -> None:
        nav = open_alerts_frame_windows_group
        driver = nav.driver
        browser_windows_page = examples.tools_qa.page_objects.alerts_frame_windows.browser_windows.Page(driver=driver)

        nav.click_link_button(link_name='Browser Windows')
        browser_windows_page.wait_until_loaded()
        assert browser_windows_page.is_loaded()
        return

    @staticmethod
    def test_alerts_frames_link(open_alerts_frame_windows_group) -> None:
        nav = open_alerts_frame_windows_group
        driver = nav.driver
        frames_page = examples.tools_qa.page_objects.alerts_frame_windows.frames.Page(driver=driver)

        nav.click_link_button(link_name='Frames')
        frames_page.wait_until_loaded()
        assert frames_page.is_loaded()
        return

    @staticmethod
    def test_alerts_modal_dialogs_link(open_alerts_frame_windows_group) -> None:
        nav = open_alerts_frame_windows_group
        driver = nav.driver
        modal_dialogs_page = examples.tools_qa.page_objects.alerts_frame_windows.modal_dialogs.Page(driver=driver)

        nav.click_link_button(link_name='Modal Dialogs')
        modal_dialogs_page.wait_until_loaded()
        assert modal_dialogs_page.is_loaded()
        return

    # Interactions

    @staticmethod
    def test_interactions_resizable_link(open_interactions_group) -> None:
        nav = open_interactions_group
        driver = nav.driver
        resizable_page = examples.tools_qa.page_objects.interactions.resizable.Page(driver=driver)

        nav.click_link_button(link_name='Resizable')
        resizable_page.wait_until_loaded()
        assert resizable_page.is_loaded()
        return

    @staticmethod
    def test_interactions_droppable_link(open_interactions_group) -> None:
        nav = open_interactions_group
        driver = nav.driver
        droppable_page = examples.tools_qa.page_objects.interactions.droppable.Page(driver=driver)

        nav.click_link_button(link_name='Droppable')
        droppable_page.wait_until_loaded()
        assert droppable_page.is_loaded()
        return

    @staticmethod
    def test_interactions_draggable_link(open_interactions_group) -> None:
        nav = open_interactions_group
        driver = nav.driver
        draggable_page = examples.tools_qa.page_objects.interactions.draggable.Page(driver=driver)

        nav.click_link_button(link_name='Dragabble')
        draggable_page.wait_until_loaded()
        assert draggable_page.is_loaded()
        return
