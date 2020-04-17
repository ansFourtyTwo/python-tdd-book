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
        
    def test_can_start_a_list_and_retrieve_it_later(self):
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
        time.sleep(1)
        self.wait_for_row_in_list_table('1: Buy Hafermilch')
        
        # self.assertTrue(
        #     any(row.text == '1: Buy Hafermilch' for row in rows),
        #     f'New to-do item did not appear in the table.\n'
        #     f'Contents were:\n{table.text}'
        # )

        # There is still a textbox inviting him to add another item. He
        # enters "Call mum"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Call mum')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on his list
        self.wait_for_row_in_list_table('1: Buy Hafermilch')
        self.wait_for_row_in_list_table('2: Call mum')

        # Simon wonders wheter the site will remember his list. Then he sees
        # that the has generated a unique URL for him -- there is some
        # explanatory text to that effect

        # He visits that URL - his to-do list is still here

        # Satisfied, he goes back to sleep
        
        self.fail('Finish tests from above!!')


