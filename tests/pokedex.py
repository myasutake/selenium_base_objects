import logging.config

import misc.logging_config
import steps.pokedex

logging.config.dictConfig(misc.logging_config.config)


def test_default_sort_method(driver) -> None:
    steps.pokedex.verify_sort_method_selected(driver=driver, sort_method='Lowest Number (First)')
    steps.pokedex.verify_search_results_are_sorted_correctly(driver=driver)
    return
