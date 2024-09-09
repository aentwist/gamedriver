import math
import time
import timeit

import cv2 as cv

from gamedriver._geometry import Box, tap_box
from gamedriver._locate import locate
from gamedriver._util import get_img_path, open_img, wait
from gamedriver.logger import logger
from gamedriver.settings import settings


def wait_until_img_visible(
    img: str | cv.typing.MatLike,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold: float = None,
    timeout_s=30,
) -> Box | None:
    """Waits until an image is visible.

    Polls to check whether the image is visible every
    :py:attr:`settings.Settings.refresh_rate_ms` milliseconds.

    See :py:func:`gamedriver.locate`.

    Args:
        timeout_s (int, optional): Timeout in seconds. Defaults to 30.

    Returns:
        Box | None: The match, or None if there is no match within `timeout_s`.
    """
    refresh_rate_s = settings["refresh_rate_ms"] / 1_000
    img_bgr = open_img(get_img_path(img)) if isinstance(img, str) else img

    box = None
    t_start = timeit.default_timer()
    t_end = t_start
    while t_end - t_start < timeout_s:
        # t_end is the end of last iteration, i.e. the start of this one
        box = locate(
            img_bgr,
            bounding_box=bounding_box,
            convert_to_grayscale=convert_to_grayscale,
            is_grayscale=is_grayscale,
            method=method,
            threshold=threshold,
        )
        if box:
            logger.debug(f"{img} available after {t_end - t_start}s")
            break

        # Amount of time used so far this loop iteration
        t_curr = timeit.default_timer() - t_end
        # Time left to use this loop iteration
        t_remain = refresh_rate_s - t_curr
        if t_remain > 0:
            time.sleep(t_remain)
        t_end = timeit.default_timer()
    else:
        logger.debug(f"{img} not available after {timeout_s}s")

    return box


def tap_img(
    img: str | cv.typing.MatLike,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold: float = None,
) -> Box | None:
    """Taps the center of an image if found.

    See :py:func:`gamedriver.locate`.
    """
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
    return box


# Makes us seem a little more human, if you're into that ;) (at the expense of speed)
def tap_img_when_visible_after_wait(
    img: str | cv.typing.MatLike,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold: float = None,
    timeout_s=30,
    seconds=1,
) -> Box | None:
    """Waits until an image is visible, waits for a time, then taps it.

    See :py:func:`gamedriver.locate` and
    :py:func:`gamedriver.wait_until_img_visible`.

    Args:
        seconds (int, optional): Time to wait after the image becomes visible
            before tapping it. Defaults to 1.
    """
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
    return box


def tap_img_when_visible(
    img: str | cv.typing.MatLike,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold: float = None,
    timeout_s=30,
) -> Box | None:
    """Waits until an image is visible, then taps the center of it.

    See :py:func:`gamedriver.locate` and
    :py:func:`gamedriver.wait_until_img_visible`.
    """
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
    img: str | cv.typing.MatLike,
    other: str | cv.typing.MatLike,
    *,
    bounding_box: Box = None,
    other_bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold: float = None,
    timeout_s=5,
    frequency_s=1,
) -> bool:
    """Taps an image while another is visible.

    See :py:func:`gamedriver.locate` and
    :py:func:`gamedriver.wait_until_img_visible`.

    Args:
        img (str | cv.typing.MatLike): Image to tap
        other (str | cv.typing.MatLike): Image to check the visibility of
        frequency_s (int, optional): How often the image to tap should be
            tapped, in seconds. Defaults to 1.

    Returns:
        bool: True if the image to check disappeared within the timeout and
            tapping was stopped, or False if the image to check remained after
            the timeout and tapping was continued until the end.
    """
    img_bgr = open_img(get_img_path(img)) if isinstance(img, str) else img
    other_bgr = open_img(get_img_path(other)) if isinstance(other, str) else other

    tap_count = math.floor(timeout_s / frequency_s)
    for _ in range(tap_count):
        if not locate(
            other_bgr,
            bounding_box=other_bounding_box,
            convert_to_grayscale=convert_to_grayscale,
            is_grayscale=is_grayscale,
            method=method,
            threshold=threshold,
        ):
            break
        tap_img(
            img_bgr,
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
    img: str | cv.typing.MatLike,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold: float = None,
    timeout_s=5,
    frequency_s=1,
) -> bool:
    """Taps an image while it is visible.

    See :py:func:`tap_img_while_other_visible`.

    Args:
        img (str | cv.typing.MatLike): Image to check the visibility of and tap
    """
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
