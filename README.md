# velenium
Interact with an app using visual definitions of elements

## sample usage

```python
import unittest

from appium import webdriver
from appium.options.common import AppiumOptions

import velenium as ve


class VisualTestCase(unittest.TestCase):
    
    def setUp(self):
        # given a driver
        options = AppiumOptions()
        options.load_capabilities({'automationName': 'UIAutomator2', 'platformName': 'Android', ...})

        # Create remote appium driver
        self.driver = webdriver.Remote(command_executor='http://localhost:4723/wd/hub', options=options)
        # or for local desktop automation
        self.driver = ve.VisualDriver()

    def tearDown(self):
        self.driver.quit()

    def test_visual(self):
        # create a visual definition
        element = ve.VisualElement(self.driver, 'path/to/pattern.png')

        # create a visual definition using multiple images using glob path
        element = ve.VisualElement(self.driver, 'path/to/patterns/**/pattern_*.png')

        # assert element is visible
        self.assertTrue(element.is_visible())

        # wait until element is visible, raises TimeoutException from selenium if timeout
        element.wait_until_visible()

        # wait until element is not visible, raises TimeoutException from selenium if timeout
        element.wait_until_not_visible()

        # find only in de middle region
        ve.VisualElement(self.driver, 'path/to/pattern.png', region=ve.LEFT_SIDE).click()

        # custom region, upper right in the example
        ve.VisualElement(self.driver, 'path/to/pattern.png', region=((0.5, 0), (1, 0.5))).click()

        # click on element on de right border
        ve.VisualElement(self.driver, 'path/to/pattern.png', target=ve.RIGHT).click()

        # custom region, center right in the example
        ve.VisualElement(self.driver, 'path/to/pattern.png', target=(0.5, 0)).click()

        # refresh position of element and click
        element.reset_object().click()

        # click and wait no visibility of the element
        element.click().wait_until_not_visible()

        # find with different similarity threshold, by default is 80%
        ve.VisualElement(self.driver, 'path/to/pattern.png', similarity=0.7).click()

        # click the 2nd best match of element
        ve.VisualElement(self.driver, 'path/to/pattern.png', order=1).click()

        # click element at 2nd position in vertical order
        ve.VisualElement(self.driver, 'path/to/pattern.png', order=1, disposal=ve.VERTICAL).click()
        # or
        item = ve.VisualElement(self.driver, 'path/to/pattern.png', disposal=ve.VERTICAL)
        item.matches[1].click()

        # click element at 3er position in horizontal order
        ve.VisualElement(self.driver, 'path/to/pattern.png', order=2, disposal=ve.HORIZONTAL).click()
        # or
        item = ve.VisualElement(self.driver, 'path/to/pattern.png', disposal=ve.HORIZONTAL)
        item.matches[2].click()

        # use another cv2 method to get the match, by default uses CV_CCOEFF
        ve.VisualElement(self.driver, 'path/to/pattern.png', method=ve.CV_SQDIFF).wait_until_visible()

        # count matches
        print(len(element.matches))
        # or
        print(element.count)

        # iterate over matches
        for e in element.matches:
            e.click()

        # enable debug images in "temp/" folder
        element.debug()

        # disable debug images
        element.debug(False)


if __name__ == '__main__':
    unittest.main()
```