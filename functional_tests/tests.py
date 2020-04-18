from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        self.browser.quit()
        
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
        
    def test_can_start_a_list_for_one_user(self):
        # Simon has heard of a new web app, where he can enter things into a Todo
        # list, he goes to check out this page
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do items straigt away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
                         
        # He types "Buy Hafermilch" into a textbox
        inputbox.send_keys('Buy Hafermilch')

        # When he hits ENTER, the page updates, and now the page lists
        # "1: Buy Hafermilch" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy Hafermilch')

        # There is still a textbox inviting him to add another item. He
        # enters "Call mum"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Call mum')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on his list
        self.wait_for_row_in_list_table('1: Buy Hafermilch')
        self.wait_for_row_in_list_table('2: Call mum')

        # Satisfied, he goes back to sleep
        
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Simon starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy Hafermilch')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy Hafermilch')
        
        # He notices that his list has a unique URL
        simon_list_url = self.browser.current_url
        self.assertRegex(simon_list_url, '/list/.+')
        
        # Now a new user, Francis, comes along to the site.
        
        ## We use a new browser session to make sure that no information
        ## of Simon's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        # Francis visits the home page. There is no sign of Simon's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Hafermilch', page_text)
        self.assertNotIn('Call mum', page_text)
        
        # Francis starts a new list by entering a new item. He is less
        # interesting than Simon
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Go to church')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('Go to church')
        
        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertReqex(francis_list_url, '/list/.+')
        assertNotEqual(simon_list_url, francis_list_url)
        
        # Again, there is no trace of Simon's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Hafermilch', page_text)
        self.assertNotIn('Call mum', page_text)
        
        # Satisfied, they both go back to sleep
        


