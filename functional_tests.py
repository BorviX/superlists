from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		
	def tearDown(self):
		self.browser.quit()
		
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

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Buy paper hearts' for row in rows), "New to-do item did not appear in table"
		)
		
		#There is still a text box inviting ger to add another item
		#She enters "Use paper hearts in scrapbook"
		self.fail('Finish the test!')

		#The page updates again, and now shows both items on her list

		#Lonni wonder whether the site will remember her lists
		#Then she sees the site has generated a unique URL for her
		#There is some explanatory text to that effect

		#She visits that URL - her to-do list is still there

		#Satisfied, she goes to sleep

if __name__ == '__main__':
	unittest.main()