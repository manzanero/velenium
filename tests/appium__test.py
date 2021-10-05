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

    def test_find(self):
        element = ve.VisualElement(self.driver, 'tests/resources/appium.png',
                                   target=ve.MIDDLE_LEFT,
                                   similarity=0.7,
                                   order=1,
                                   disposal=ve.VERTICAL,
                                   region=ve.UP_SIDE)
        element.debug()
        element.click()

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
