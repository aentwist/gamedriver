from typing import Iterator

import cv2 as cv

from gamedriver._geometry import Box
from gamedriver._match_template import match_template, match_template_all
from gamedriver._util import get_img_path, get_screen


def locate(
    img: str,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold: float = None,
) -> Box | None:
    """Locates an image on the screen.

    Performs a template match where the haystack image is the device screen and
    the needle image is specified by the relative path instead of the full path.

    See :py:func:`gamedriver.match_template`.

    See also :py:func:`gamedriver.get_screen` and
    :py:func:`gamedriver.get_img_path`.

    Args:
        img (str): Relative path to the needle image, with no file extension

    Returns:
        Box | None

    Examples:
        ::

            box = gd.locate("buttons/confirm")
    """
    screen = (
        get_screen(grayscale=is_grayscale) if is_grayscale is not None else get_screen()
    )
    return match_template(
        screen,
        get_img_path(img),
        bounding_box=bounding_box,
        convert_to_grayscale=convert_to_grayscale,
        is_grayscale=is_grayscale,
        method=method,
        threshold=threshold,
    )


def locate_all(
    img: str,
    *,
    bounding_box: Box = None,
    convert_to_grayscale=True,
    is_grayscale=False,
    method=cv.TM_SQDIFF_NORMED,
    threshold: float = None,
) -> Iterator[Box]:
    """Locates all images on the screen.

    See :py:func:`locate`.

    See also :py:func:`gamedriver.match_template_all`.

    Yields:
        Iterator[Box]
    """
    screen = (
        get_screen(grayscale=is_grayscale) if is_grayscale is not None else get_screen()
    )
    return match_template_all(
        screen,
        get_img_path(img),
        bounding_box=bounding_box,
        convert_to_grayscale=convert_to_grayscale,
        is_grayscale=is_grayscale,
        method=method,
        threshold=threshold,
    )
