from typing import Iterator

import cv2 as cv
import numpy as np

from gamedriver._geometry import Box


def _match_template(
    haystack: str | cv.typing.MatLike,
    needle: str | cv.typing.MatLike,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
):
    if is_grayscale:
        convert_to_grayscale = False

    IMAGE_DNE_ERR_MSG = "Failed to read %s image %s, are you sure it exists?"

    image = haystack
    if isinstance(haystack, str):
        image = (
            cv.imread(haystack, cv.IMREAD_GRAYSCALE)
            if is_grayscale
            else cv.imread(haystack)
        )
        assert image is not None, IMAGE_DNE_ERR_MSG % ("haystack", haystack)
    templ = needle
    if isinstance(needle, str):
        templ = (
            cv.imread(needle, cv.IMREAD_GRAYSCALE)
            if is_grayscale
            else cv.imread(needle)
        )
        assert templ is not None, IMAGE_DNE_ERR_MSG % ("needle", needle)

    bb = bounding_box
    if bb:
        image = image[bb.top : bb.bottom, bb.left : bb.right]

    # avoid semi-cryptic OpenCV error below if bad size
    if templ.shape[0] > image.shape[0] or templ.shape[1] > image.shape[1]:
        raise ValueError(
            "needle dimensions exceed the haystack image or bounding box dimensions"
        )

    if convert_to_grayscale:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        templ = cv.cvtColor(templ, cv.COLOR_BGR2GRAY)

    # Return both the Mat object and the dimensions of matches - we need the
    # dimensions outside and it is simplest to just return them from here
    # instead of moving logic around / passing things around. This issue is
    # caused by allowing the image args to be strings, then only opening them
    # in here.
    return cv.matchTemplate(image, templ, method), image.shape, templ.shape


def match_template(
    haystack: str | cv.typing.MatLike,
    needle: str | cv.typing.MatLike,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold=None,
) -> Box | None:
    res, _, templ_shape = _match_template(
        haystack,
        needle,
        bounding_box=bounding_box,
        convert_to_grayscale=convert_to_grayscale,
        is_grayscale=is_grayscale,
        method=method,
    )
    h, w = templ_shape[:2]
    min, max, min_loc, max_loc = cv.minMaxLoc(res)

    if bounding_box:
        bb = bounding_box
        min_loc = (bb[0] + min_loc[0], bb[1] + min_loc[1])
        max_loc = (bb[0] + max_loc[0], bb[1] + max_loc[1])

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    # (if not specified it defaults to TM_SQDIFF)
    if not method or method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        if not threshold:
            threshold = 0.05
        is_match = min < threshold
        top_left = min_loc
    else:
        if not threshold:
            threshold = 0.8
        is_match = max > threshold
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    if not is_match:
        return None
    return Box(top_left[0], top_left[1], bottom_right[0], bottom_right[1])


def match_template_all(
    haystack: str | cv.typing.MatLike,
    needle: str | cv.typing.MatLike,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold=None,
) -> Iterator[Box]:
    res, image_shape, templ_shape = _match_template(
        haystack,
        needle,
        bounding_box=bounding_box,
        convert_to_grayscale=convert_to_grayscale,
        is_grayscale=is_grayscale,
        method=method,
    )
    h, w = templ_shape[:2]

    if not method or method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        if not threshold:
            threshold = 0.05
        loc = np.where(res < threshold)
    else:
        if not threshold:
            threshold = 0.8
        loc = np.where(res > threshold)

    mask = np.zeros(image_shape[:2], np.uint8)
    for pt in zip(*loc[::-1]):
        if bounding_box:
            pt[0] += bounding_box[0]
            pt[1] += bounding_box[1]
        if not mask[pt[1] + int(round(h / 2)), pt[0] + int(round(w / 2))]:
            mask[pt[1] : pt[1] + h, pt[0] : pt[0] + w] = 1
            yield Box(pt[0], pt[1], pt[0] + w, pt[1] + h)
