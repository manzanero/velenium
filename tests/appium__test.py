import unittest

import velenium as ve
from appium import webdriver


class ActionsTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', dict(
            platformName='Android',
            deviceName='Android Emulator',
            app="test.apk",
        ))

    def tearDown(self):
        self.driver.quit()

    def test_find(self):
        ve.VisualElement(self.driver, 'tests/resources/appium.png').click()


if __name__ == '__main__':
    unittest.main()
