import unittest

import velenium as ve


class ActionsTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = ve.VisualDriver()

    def tearDown(self):
        self.driver.quit()

    def test_find(self):
        ve.VisualElement(self.driver, 'tests/resources/desktop.png').click()


if __name__ == '__main__':
    unittest.main()
