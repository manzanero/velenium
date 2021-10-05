import unittest

import velenium as ve


class ActionsTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = ve.VisualDriver()

    def test_find(self):
        ve.VisualElement(self.driver, 'tests/resources/desktop.png').wait_until_visible(20).click()

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
