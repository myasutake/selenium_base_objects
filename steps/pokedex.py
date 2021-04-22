import logging

from selenium.webdriver.remote.webdriver import WebDriver

import page_objects.pokedex


# Verifications


def verify_search_results_are_sorted_correctly(driver: WebDriver) -> None:
    page = page_objects.pokedex.PokedexPage(driver=driver)
    sort_dropdown = page.find_sort_dropdown()

    if sort_dropdown.selected_option == 'Lowest Number (First)':
        actual_results = page.all_search_results_numbers_as_ints()
        expected_results = actual_results.copy()
        expected_results.sort()
    elif sort_dropdown.selected_option == 'Highest Number (First)':
        actual_results = page.all_search_results_numbers_as_ints()
        expected_results = actual_results.copy()
        expected_results.sort(reverse=True)
    elif sort_dropdown.selected_option == 'A-Z':
        actual_results = page.all_search_results_names()
        expected_results = actual_results.copy()
        expected_results.sort()
    elif sort_dropdown.selected_option == 'Z-A':
        actual_results = page.all_search_results_names()
        expected_results = actual_results.copy()
        expected_results.sort(reverse=True)
    else:
        log_str = f"Unexpected sort method '{sort_dropdown.selected_option}' found."
        logging.error(log_str)
        raise ValueError(log_str)

    assert actual_results == expected_results
    logging.info(f"VERIFIED: Results correctly sorted for method '{sort_dropdown.selected_option}'.")
    return


def verify_sort_method_selected(driver: WebDriver, sort_method: str) -> None:
    page = page_objects.pokedex.PokedexPage(driver=driver)
    sort_dropdown = page.find_sort_dropdown()
    assert sort_dropdown.selected_option == sort_method
    logging.info(f"VERIFIED: Current sort method is '{sort_method}'.")
    return


# Misc


def load_page(driver: WebDriver) -> None:
    page = page_objects.pokedex.PokedexPage(driver=driver)
    page.load_page()
    if page.cookies_dialog_is_displayed():
        page.accept_cookies()
    return
