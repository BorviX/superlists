from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		
	def tearDown(self):
		self.browser.quit()
	
	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])
	
	
	def test_can_start_a_list_and_retrieve_it_later(self):

		#Lonni heard about a new online to-do app
		#She goes to check out it's homepage
		self.browser.get('http://localhost:8000')

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
		time.sleep(1)
		self.check_for_row_in_list_table('1: Buy paper hearts')

		#There is still a text box inviting her to add another item
		#She enters "Use paper hearts in scrapbook" and presses enter
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use paper hearts in scrapbook')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		#The page updates again, and now shows both items on her list
		self.check_for_row_in_list_table('1: Buy paper hearts')
		self.check_for_row_in_list_table('2: Use paper hearts in scrapbook')
		
		#Lonni wonder whether the site will remember her lists
		#Then she sees the site has generated a unique URL for her
		#There is some explanatory text to that effect
		self.fail('Finish the test!')
		#She visits that URL - her to-do list is still there

		#Satisfied, she goes to sleep

if __name__ == '__main__':
	unittest.main()