import logging
import time

from page_objects.base import BasePage


def verify_page_is_displayed(expected_page: BasePage) -> None:
    try:
        expected_page.wait_until_loaded()
    except TimeoutError:
        log_str = f'TEST FAILED: {expected_page} is not displayed.'
        logging.error(log_str)
        raise AssertionError(log_str)

    logging.info(f'VERIFIED: {expected_page} is displayed.')
    return


def wait_for_one_of_multiple_pages_to_load(possible_pages: list[BasePage], timeout: int = 5) -> BasePage:
    """
    Call this function when one of multiple pages could appear next. Returns page loaded.
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        time.sleep(0.5)
        for i_page in possible_pages:
            if i_page.is_loaded():
                logging.debug(f'{i_page} loaded.')
                return i_page
    log_str = f'None of the specified pages loaded: {possible_pages}'
    logging.error(log_str)
    raise TimeoutError(log_str)
