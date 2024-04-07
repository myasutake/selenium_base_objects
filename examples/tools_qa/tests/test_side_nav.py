import logging.config

import pytest
from selenium.common.exceptions import InvalidElementStateException

import examples.tools_qa.page_objects.common
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


def test_clicking_an_expanded_group_closes_it(navigate_to_page_and_verify_initial_nav_state) -> None:
    nav = navigate_to_page_and_verify_initial_nav_state

    group_name = 'Elements'
    nav.click_group_header_button(group_name=group_name)
    assert nav.group_is_collapsed(group_name=group_name)
    return


def test_clicking_a_closed_group_expands_it(navigate_to_page_and_verify_initial_nav_state) -> None:
    nav = navigate_to_page_and_verify_initial_nav_state

    group_name = 'Forms'
    nav.click_group_header_button(group_name=group_name)
    assert nav.group_is_expanded(group_name=group_name)
    return


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


def test_no_expanded_groups_is_possible(navigate_to_page_and_verify_initial_nav_state) -> None:
    nav = navigate_to_page_and_verify_initial_nav_state
    nav.click_group_header_button(group_name='Elements')
    assert len(nav.expanded_groups) == 0
    return
