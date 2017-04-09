from selenium import webdriver
import unittest


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
		self.fail('Finish the test!')

		#She is invited to enter a to-do item straight away

		#She types "Buy paper hearts" into a text box

		#When she hits enter, the page updates, and now the page lists:
		# "1: Buy paper hearts" as an item in a to-do list

		#There is still a text boc inviting ger to add another item
		#She enters "Use paper hearts in scrapbook"

		#The page updates again, and now shows both items on her list

		#Lonni wonder whether the site will remember her lists
		#Then she sees the site has generated a unique URL for her
		#There is some explanatory text to that effect

		#She visits that URL - her to-do list is still there

		#Satisfied, she goes to sleep

if __name__ == '__main__':
	unittest.main()