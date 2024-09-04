import math

import cv2 as cv

from gamedriver._geometry import Box, tap_box
from gamedriver._locate import locate
from gamedriver._util import wait
from gamedriver.logger import logger
from gamedriver.settings import settings


def wait_until_img_visible(
    img: str,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold=None,
    timeout_s=30,
):
    """Waits until an image is visible

    Polls to check whether the image is visible every 0.1s.

    Args:
        image (str): image name
        region (tuple, optional): See `pyscreeze.locate`. Defaults to (0, 0, RESOLUTION[0], RESOLUTION[1]).
        timeout_s (int, optional): timeout in seconds. Defaults to 30.

    Returns:
        None | Box
    """
    polling_interval_s = settings["refresh_rate_ms"] / 1_000

    box = None
    for i in range(math.floor(timeout_s / polling_interval_s)):
        box = locate(
            img,
            bounding_box=bounding_box,
            convert_to_grayscale=convert_to_grayscale,
            is_grayscale=is_grayscale,
            method=method,
            threshold=threshold,
        )
        if box:
            logger.debug(f"{img} available after {i * polling_interval_s}s")
            break
        wait(polling_interval_s)
    else:
        logger.debug(f"{img} not available after {timeout_s}s")

    return box


def tap_img(
    img: str,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold=None,
):
    box = locate(
        img,
        bounding_box=bounding_box,
        convert_to_grayscale=convert_to_grayscale,
        is_grayscale=is_grayscale,
        method=method,
        threshold=threshold,
    )
    if not box:
        logger.debug(
            f"{img} not found{f' in bounding box {bounding_box}' if bounding_box else ''}"
        )
    else:
        tap_box(box)
    return bool(box)


# Makes us seem a little more human, if you're into that ;) (at the expense of speed)
def tap_img_when_visible_after_wait(
    img: str,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold=None,
    timeout_s=30,
    seconds=1,
):
    box = wait_until_img_visible(
        img,
        bounding_box=bounding_box,
        convert_to_grayscale=convert_to_grayscale,
        is_grayscale=is_grayscale,
        method=method,
        threshold=threshold,
        timeout_s=timeout_s,
    )
    if box:
        wait(seconds)
        tap_box(box)
    return bool(box)


def tap_img_when_visible(
    img: str,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold=None,
    timeout_s=30,
) -> bool:
    return tap_img_when_visible_after_wait(
        img,
        bounding_box=bounding_box,
        convert_to_grayscale=convert_to_grayscale,
        is_grayscale=is_grayscale,
        method=method,
        threshold=threshold,
        timeout_s=timeout_s,
        seconds=0,
    )


def tap_img_while_other_visible(
    img: str,
    other: str,
    *,
    bounding_box: Box = None,
    other_bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold=None,
    timeout_s=5,
    frequency_s=1,
):
    tap_count = math.floor(timeout_s / frequency_s)
    for _ in range(tap_count):
        if not locate(
            other,
            bounding_box=other_bounding_box,
            convert_to_grayscale=convert_to_grayscale,
            is_grayscale=is_grayscale,
            method=method,
            threshold=threshold,
        ):
            break
        tap_img(
            img,
            bounding_box=bounding_box,
            convert_to_grayscale=convert_to_grayscale,
            is_grayscale=is_grayscale,
            method=method,
            threshold=threshold,
        )
        wait(frequency_s)
    else:
        logger.error(
            f"Kept tapping image {img}, but image {other} was still visible "
            + f"after {tap_count} tries each {frequency_s} seconds apart"
        )
        return False

    return True


def tap_img_while_visible(
    img: str,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold=None,
    timeout_s=5,
    frequency_s=1,
):
    # Touching an image while it is visible is a special case of taping it
    # while an arbitrary image is visible
    return tap_img_while_other_visible(
        img,
        img,
        bounding_box=bounding_box,
        other_bounding_box=bounding_box,
        convert_to_grayscale=convert_to_grayscale,
        is_grayscale=is_grayscale,
        method=method,
        threshold=threshold,
        timeout_s=timeout_s,
        frequency_s=frequency_s,
    )
