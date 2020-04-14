from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        self.browser.quit()
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Simon has heard of a new web app, where he can enter things into a Todo
        # list, he goes to check out this page

        self.browser.get('http://localhost:8000')

        # He notices the page title mentions to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')


        # He is invited to enter a to-do items straigt away

        # He types "Buy Hafermilch" into a textbox

        # When he hits ENTER, the page updates, and now the page lists
        # "1: Buy Hafermilch" as an item in a to-do list

        # There is still a textbox inviting him to add another item. He
        # enters "Call mum"

        # The page updates again, and now shows both items on his list

        # Simon wonders wheter the site will remember his list. Then he sees
        # that the has generated a unique URL for him -- there is some
        # explanatory text to that effect

        # He visits that URL - his to-do list is still here

        # Satisfied, he goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')

