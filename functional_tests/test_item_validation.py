from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):
        
    def test_cannot_add_empty_list_items(self):
        # Simon goes to the home page and accidentially tries to submit
        # an empty list item, He hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.ENTER)
        
        # The browser intercepts the request, and does not load the 
        # list page
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:invalid'
        ))
        
        # He starts typing some text for the new item and the error 
        # disappears
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:valid'
        ))
        
        # And he can submit the entered items successfully
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        
        # Perversly, she now decides to submit a second blank list item
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.ENTER)
        
        # Again the browser intercepts
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:invalid'
        ))
        
        # And he can correct it by filling some text in
        inputbox.send_keys('Make tea')
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:valid'
        ))
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
