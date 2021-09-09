# velenium
Interact with an app using visual definitions of elements

## sample usage

```python
import unittest
from appium import webdriver
from velenium import VisualElement, LEFT_SIDE, RIGHT, VERTICAL, HORIZONTAL, CV_SQDIFF


class VisualTestCase(unittest.TestCase):

    def test_visual(self):
        desired_caps = dict(
            ...
        )
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

        # create a visual definition
        element = VisualElement(driver, 'path/to/pattern.png')

        # create a visual definition using multiple images using glob path
        element = VisualElement(driver, 'path/to/patterns/**/pattern_*.png')

        # assert element is visible
        self.assertTrue(element.is_visible())

        # wait until element is visible, raises TimeoutException from selenium if timeout
        element.wait_until_visible()

        # wait until element is not visible, raises TimeoutException from selenium if timeout
        element.wait_until_not_visible()

        # find only in de middle region
        VisualElement(driver, 'path/to/pattern.png', region=LEFT_SIDE).click()

        # custom region, upper right in the example
        VisualElement(driver, 'path/to/pattern.png', region=((0.5, 0), (1, 0.5))).click()
        
        # click on element on de right border
        VisualElement(driver, 'path/to/pattern.png', target=RIGHT).click()
        
        # custom region, center right in the example
        VisualElement(driver, 'path/to/pattern.png', target=(0.5, 0)).click()

        # refresh position of element and click
        element.reset_object().click()

        # click and wait no visibility of the element
        element.click().wait_until_not_visible()

        # find with different similarity threshold, by default is 80%
        VisualElement(driver, 'path/to/pattern.png', similarity=0.7).click()

        # click the 2nd best match of element
        VisualElement(driver, 'path/to/pattern.png', order=1).click()

        # click element at 2nd position in vertical order
        VisualElement(driver, 'path/to/pattern.png', order=1, disposal=VERTICAL).click()
        # or
        item = VisualElement(driver, 'path/to/pattern.png', disposal=VERTICAL)
        item.matches[1].click()

        # click element at 3er position in horizontal order
        VisualElement(driver, 'path/to/pattern.png', order=2, disposal=HORIZONTAL).click()
        # or
        item = VisualElement(driver, 'path/to/pattern.png', disposal=HORIZONTAL)
        item.matches[2].click()

        # use another cv2 method to get the match, by default uses CV_CCOEFF
        VisualElement(driver, 'path/to/pattern.png', method=CV_SQDIFF).wait_until_visible()

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