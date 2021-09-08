import base64
import glob
import os
import pathlib
import re
import time
from datetime import datetime

import cv2 as cv
import imutils
import numpy as np
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from typing import List, Tuple

SIMILARITY = 0
VERTICAL = 1
HORIZONTAL = 2

CV_CCOEFF = cv.TM_CCOEFF_NORMED
CV_CCORR = cv.TM_CCORR_NORMED
CV_SQDIFF = cv.TM_SQDIFF_NORMED

ALL = ((0, 0), (1, 1))
UPPER = ((0, 0), (1, 0.3))
MIDDLE = ((0, 0.3), (1, 0.7))
LOWER = ((0, 0), (0.7, 1))
LEFT = ((0, 0), (0.5, 1))
RIGHT = ((0.5, 0), (1, 1))

Bounds = Tuple[Tuple[float, float], Tuple[float, float]]


class VisualMatch(object):

    def __init__(self, driver, center: Tuple, dimensions: Tuple, target: Tuple = (0, 0), similarity=0.7):
        self.driver = driver
        self.center = center
        self.dimensions = dimensions
        self.target = target
        self.similarity = similarity

    @property
    def position(self) -> Tuple[int, int]:
        return int(self.center[0] + self.target[0] * self.dimensions[0] / 2), \
               int(self.center[1] + self.target[1] * self.dimensions[1] / 2)

    @property
    def bounds(self) -> Bounds:
        start_x, start_y = int(self.center[0] - self.dimensions[0] / 2), int(self.center[1] - self.dimensions[1] / 2)
        end_x, end_y = int(start_x + self.dimensions[0]), int(start_y + self.dimensions[1])
        return (start_x, start_y), (end_x, end_y)

    def click(self):
        TouchAction(self.driver).press(x=self.position[0], y=self.position[1]).release().perform()


class VisualElement(object):

    def __init__(self, driver: WebDriver, path, target: Tuple = (0, 0), similarity: float = 0.7, order: int = 0,
                 disposal: int = SIMILARITY, method=CV_CCOEFF, region: Bounds = ALL, name: str = None):
        self.driver = driver
        self.path = str(path)
        self.target = target
        self.similarity = similarity
        self.order = order
        self.disposal = disposal
        self.name = name or re.sub(r'\W+', '_', pathlib.Path(path).stem)
        self.method = method
        self.region = region

        self._max_matches = 16
        self._debug = False
        self._searched = False
        self._matches: List[VisualMatch] = []

        for x in [region[0][0], region[0][1], region[1][0], region[1][1]]:
            if not 0 <= x <= 1:
                raise Exception(f"Visual region out of bounds: {region}")
        if region[0][0] > region[1][0] or region[0][1] > region[1][1]:
            raise Exception(f"Visual region error: {region}")

    @property
    def matches(self) -> List[VisualMatch]:
        return self._matches if self._searched else self._search_all_matches()._matches

    @property
    def match(self) -> VisualMatch:
        return self.matches[self.order]

    @property
    def count(self) -> int:
        return len(self.matches)

    def debug(self, enable=True):
        self._debug = enable
        return self

    def reset_object(self):
        self._searched = False
        self._matches.clear()
        return self

    def is_visible(self) -> bool:
        return bool(self.reset_object().matches)

    def wait_until_visible(self, timeout=10):
        start_time = datetime.now()
        while not self.is_visible():
            time_delta = datetime.now() - start_time
            if time_delta.total_seconds() >= timeout:
                raise TimeoutException(f'Cannot find "{self.name}" in {timeout} seconds')
            time.sleep(1)
        return self

    def wait_until_not_visible(self, timeout=10):
        start_time = datetime.now()
        while self.is_visible():
            time_delta = datetime.now() - start_time
            if time_delta.total_seconds() >= timeout:
                raise TimeoutException(f'Still present "{self.name}" in {timeout} seconds')
            time.sleep(1)
        return self

    def wait_until_clickable(self, timeout=10):
        return self.wait_until_visible(timeout)

    def click(self, timeout=10):
        self.wait_until_clickable(timeout).match.click()
        return self

    def _search_all_matches(self):
        self._matches.clear()
        for template_path in glob.glob(self.path):
            self._find_matches(template_path)

        if self.disposal == VERTICAL:
            self._matches.sort(key=lambda v: v.center[1])
        elif self.disposal == HORIZONTAL:
            self._matches.sort(key=lambda v: v.center[0])
        elif self.disposal == SIMILARITY:
            self._matches.sort(key=lambda v: v.similarity, reverse=True)  # more similar first

        self._searched = True
        return self

    @staticmethod
    def _get_bounds(loc, w, h, r):
        start_x, start_y = loc[0] * r, loc[1] * r
        end_x, end_y = (loc[0] + w) * r, (loc[1] + h) * r
        real_w, real_h = end_x - start_x, end_y - start_y
        return start_x, start_y, end_x, end_y, real_w, real_h

    def _find_matches(self, template_path):
        if not os.path.isfile(template_path):
            raise Exception(f"Template route doesn't exist: {template_path}")
        if self.disposal not in range(2):
            raise Exception(f"Disposal priority not valid: {self.disposal}")
        if self.order not in range(self._max_matches):
            raise Exception(f"Order above max occurrences: {self.order} > {self._max_matches}")

        debug_name = pathlib.Path(template_path).stem

        # load the template image, convert it to grayscale
        template = cv.imread(template_path)
        template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
        h, w = template.shape[:2]

        # load the image and initialize the bookkeeping variable to keep track of the matched region
        screenshot = self.driver.get_screenshot_as_base64()
        np_data = np.fromstring(base64.b64decode(screenshot), np.uint8)  # noqa - it accepts bytes
        image = cv.imdecode(np_data, cv.IMREAD_UNCHANGED)

        if self._debug:
            os.makedirs('temp/velenium', exist_ok=True)
            cv.imwrite(f'temp/velenium/{int(time.time() * 1000)}__{debug_name}__screenshot.png', image)

        # cover outside region in black
        total_h, total_w = image.shape[:2]
        cv.rectangle(image, (0, 0), (total_w, int(total_h * self.region[0][1])), (0, 0, 0), -1)
        cv.rectangle(image, (0, int(total_h * self.region[1][1])), (total_w, total_h), (0, 0, 0), -1)
        cv.rectangle(image, (0, 0), (int(total_w * self.region[0][0]), total_h), (0, 0, 0), -1)
        cv.rectangle(image, (int(total_w * self.region[1][0]), 0), (total_w, total_h), (0, 0, 0), -1)

        # remove colors for performance
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        occurrence = None

        if self._debug:
            cv.imwrite(f'temp/velenium/{int(time.time() * 1000)}__{debug_name}__start.png', gray)

        # loop over the scales of the image
        for scale in np.linspace(0.2, 1.0, 20)[::-1]:

            # resize the image according to the scale, and keep track of the ratio of the resizing
            resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
            r = gray.shape[1] / float(resized.shape[1])

            # if the resized image is smaller than the template, then break from the loop
            if resized.shape[0] < h or resized.shape[1] < w:
                break

            # apply template matching to find the template in the image
            result = cv.matchTemplate(resized, template, self.method)

            # get best match and its coordinates, discard if not enough similarity
            _, max_val, _, max_loc = cv.minMaxLoc(result)
            if max_val <= self.similarity:
                continue

            # if we have found a new maximum correlation value, then update the bookkeeping variable
            if occurrence is None or max_val > occurrence[0]:
                occurrence = (max_val, max_loc, r, resized)

            # draw a bounding box around the detected region
            if self._debug:
                clone = np.dstack([resized, resized, resized])
                cv.rectangle(clone, (max_loc[0], max_loc[1]), (max_loc[0] + w, max_loc[1] + h), (0, 0, 255), 2)
                cv.imwrite(f'temp/velenium/{int(time.time() * 1000)}__{debug_name}__{int(max_val * 100)}%.png', clone)

        if not occurrence:
            return

        # unpack the bookkeeping variable and compute the coordinates of the bounding box based on the resized ratio
        max_val, max_loc, r, resized = occurrence
        start_x, start_y, end_x, end_y, real_w, real_h = self._get_bounds(max_loc, w, h, r)
        self._matches.append(VisualMatch(self.driver, (start_x + real_w / 2, start_y + real_h / 2),
                                         (real_w, real_h), self.target, max_val))

        # from that resized image get more matches
        for i in range(self._max_matches):

            # cover the previous best match in black to discard duplicates
            cv.rectangle(resized, (max_loc[0], max_loc[1]), (max_loc[0] + w, max_loc[1] + h), (0, 0, 0), -1)

            if self._debug:
                cv.imwrite(f'temp/velenium/{int(time.time() * 1000)}__{debug_name}__covered_{i}.png', resized)

            # repeat template matching to find the template in the image
            result = cv.matchTemplate(resized, template, self.method)
            _, max_val, _, max_loc = cv.minMaxLoc(result)
            if max_val <= self.similarity:
                break

            start_x, start_y, end_x, end_y, real_w, real_h = self._get_bounds(max_loc, w, h, r)
            self._matches.append(VisualMatch(self.driver, (start_x + real_w / 2, start_y + real_h / 2),
                                             (real_w, real_h), self.target, max_val))

        if self._debug:
            clone = np.dstack([gray, gray, gray])
            for match in self._matches:
                cv.rectangle(clone, (match.bounds[0][0], match.bounds[0][1]), (match.bounds[1][0], match.bounds[1][1]),
                             (0, 0, 255), 2)
                cv.circle(clone, (match.position[0], match.position[1]), 4, (0, 255, 0), -1)
            cv.imwrite(f'temp/velenium/{int(time.time() * 1000)}__{debug_name}__result.png', clone)
