from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):
        
    def test_cannot_add_empty_list_items(self):
        # Simon goes to the home page and accidentially tries to submit
        # an empty list item, He hits Enter on the empty input box
        
        # The home page refreshes, and there is an error message saying
        # the list items cannot be blank
        
        # She tries again with some text for the item, which now works
        
        # Perversly, she now decides to submit a second blank list item
        
        # He receives a similar warning on the list page
        
        # And he can correct it by filling some text in
        self.fail('Write me')
