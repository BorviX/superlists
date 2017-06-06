#Functional Tests
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 5

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
        #Lonni heard about a new online to-do app
        #She goes to check out it's homepage
        self.browser.get(self.live_server_url)

        #She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 
            'Enter a to-do item'
        )
        
        #She types "Buy paper hearts" into a text box
        inputbox.send_keys('Buy paper hearts')
        
        #When she hits enter, the page updates, and now the page lists:
        # "1: Buy paper hearts" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy paper hearts')

        #There is still a text box inviting her to add another item
        #She enters "Use paper hearts in scrapbook" and presses enter
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use paper hearts in scrapbook')
        inputbox.send_keys(Keys.ENTER)

        #The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('1: Buy paper hearts')
        self.wait_for_row_in_list_table('2: Use paper hearts in scrapbook')

        #Satisfied, she goes to sleep

    def test_multiple_users_can_start_list_at_different_urls(self):
        #Lonni starts a new todo list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy paper hearts')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy paper hearts')
        
        #She notices that her list has a unique URL
        lonni_list_url = self.browser.current_url
        self.assertRegex(lonni_list_url, '/lists/.+')
        
        #Now, a new user, Avichai, comes along to the site
        
        ## We use a new browser session to make sure that no information of Lonni's is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        #Avichai visits the home page. There is no sign of Lonni's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy paper hearts', page_text)
        self.assertNotIn('paper hearts in scrapbook', page_text)
        
        #Avichai starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Play with bimba')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Play with bimba')
        
        #Avichai gets his own unique URL
        avichai_list_url = self.browser.current_url
        self.assertRegex(avichai_list_url, '/lists/.+')
        self.assertNotEqual(avichai_list_url, lonni_list_url)
        
        #Again, there is no trace of Lonni's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy paper hearts', page_text)
        self.assertNotIn('paper hearts in scrapbook', page_text)
        
        #Satisfied they all go for a nap
        
    def test_layout_and_styling(self):
        # Lonni goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
        
        #Lonni starts a new list and sees that the input box
        #is still nicely centered
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
        
        
        