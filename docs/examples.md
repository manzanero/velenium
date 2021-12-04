# Examples

A few examples

## Desktop driver

```python
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
```

## Selenium driver

```python
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
```

## Appium driver

```python
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
```
