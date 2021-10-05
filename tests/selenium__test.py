import unittest

from chromedriver_py import binary_path

import velenium as ve
from selenium import webdriver


class GooglePageObject:

    def __init__(self, driver):
        self.accept_legal_button = ve.VisualElement(driver, 'tests/resources/selenium.png')


class ActionsTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(binary_path)
        self.driver.get('https://www.google.com/')

    def test_find(self):
        GooglePageObject(self.driver).accept_legal_button.click()
        assert not GooglePageObject(self.driver).accept_legal_button.is_visible()

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
