import unittest

from chromedriver_py import binary_path

import velenium as ve
from selenium import webdriver


class ActionsTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(binary_path)
        self.driver.get('https://www.google.com/')

    def tearDown(self):
        self.driver.quit()

    def test_find(self):
        ve.VisualElement(self.driver, 'tests/resources/selenium.png').click()


if __name__ == '__main__':
    unittest.main()
