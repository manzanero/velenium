# velenium
Interact with an app using visual definitions of elements

## sample usage

```python
import unittest
from appium import webdriver
from velenium import VisualElement, HORIZONTAL_ORDER, SIMILARITY_ORDER, CV_SQDIFF


class VisualTestCase(unittest.TestCase):

    def test_visual(self):
        desired_caps = dict(
            ...
        )
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

        element = VisualElement(driver, 'path/to/pattern.png')

        # assert element is visible
        assert element.is_visible()

        # wait until visual element is visible, raises TimeoutException from selenium if timeout
        element.wait_until_visible()

        # wait until visual element is not visible, raises TimeoutException from selenium if timeout
        element.wait_until_not_visible()

        # click on element
        element.click()

        # refresh position of element and click
        element.reset_object().click()

        # click and wait no visibility of the element
        element.click().wait_until_not_visible()

        # find with different similarity threshold, by default is 90%
        VisualElement(driver, 'path/to/pattern.png', similarity=0.8).click()

        # click element at 3er position in vertical order (default behaviour)
        element[2].click()
        VisualElement(driver, 'path/to/pattern.png', order=2).click()

        # click element at 3er position in horizontal order
        VisualElement(driver, 'path/to/pattern.png', order=2, disposal=HORIZONTAL_ORDER).click()

        # click the very best match of element (similarity threshold applies)
        VisualElement(driver, 'path/to/pattern.png', disposal=SIMILARITY_ORDER).click()

        # use another cv2 method to get the match, by default uses CV_CCOEFF
        VisualElement(driver, 'path/to/pattern.png', method=CV_SQDIFF).wait_until_visible()

        # count matches
        elements = VisualElement(driver, 'path/to/pattern.png')
        print(len(elements))

        # iterate over matches
        for e in elements:
            e.click()
        
        # get debug images
        element.debug_object()


if __name__ == '__main__':
    unittest.main()
```