import os
import time

import cv2 as cv

from gamedriver._error import ReadImageError
from gamedriver.settings import settings


def tap_xy(x: int, y: int) -> None:
    """Taps a point (x, y).

    Calls the user-provided :py:attr:`settings.Settings.tap_xy` function.

    Args:
        x (int)
        y (int)
    """
    settings["tap_xy"](x, y)


def swipe(x1: int, y1: int, x2: int, y2: int, duration_ms=100) -> None:
    """Swipes from point (x1, y1) to (x2, y2).

    Calls the user-provided :py:attr:`settings.Settings.swipe` function.

    Args:
        x1 (int)
        y1 (int)
        x2 (int)
        y2 (int)
        duration_ms (int, optional): Duration of the swipe in milliseconds.
            Defaults to 100.
    """
    settings["swipe"](x1, y1, x2, y2, duration_ms)


def wait(seconds=1.0) -> None:
    """Sleeps for a time, taking wait adjustments into account.

    Waits can be adjusted by :py:attr:`settings.Settings.wait_scale` and
    :py:attr:`settings.Settings.wait_offset`.

    Args:
        seconds (float, optional): Base time to sleep for. Defaults to 1.
    """
    time.sleep(settings["wait_scale"] * seconds + settings["wait_offset"])


def get_screen(*, grayscale=False) -> cv.typing.MatLike:
    """Gets the device screen.

    Calls the user-provided :py:attr:`settings.Settings.get_screen` function.
    Note that screens should be in the BGR color space.

    That function is augmented by specifying whether there should be a
    conversion to grayscale. This is for functions with `is_grayscale`
    parameters that if set expect argument images to be grayscale.

    Args:
        grayscale (bool, optional): Whether to return the screen in grayscale.
            Defaults to False.

    Returns:
        cv.typing.MatLike: Array representing the screen [height, width,
            channel]

    Examples:
        Save a screenshot::

            cv.imwrite("fname.png", cv.cvtColor(gd.get_screen(), cv.COLOR_BGR2RGB))

        Use grayscale template matching with an already-grayscale template,
        and a custom full path to the template::

            box = gd.match_template(
                gd.get_screen(grayscale=True),
                "my/path/buttons/confirm-gray.png",
                is_grayscale=True,
            )
    """
    screen = settings["get_screen"]()
    if grayscale:
        screen = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)
    return screen


def get_pixel(x: int, y: int) -> tuple[int, int, int]:
    """Gets a pixel from the device screen.

    The pixel should be in color. Note that it should be in the BGR color
    space.

    Args:
        x (int)
        y (int)

    Returns:
        tuple[int, int, int]: Pixel in the BGR color space

    Examples:
        ::

            # Check whether a pixel at (10, 20) is red enough
            px = gd.get_pixel(10, 20)
            is_red = px[0] < 25 and px[1] < 25 and px[2] > 225
    """
    return get_screen()[y, x]


def get_img_path(rel_path: str) -> str:
    """Gets the path to an image.

    The argument path is relative to the base directory
    :py:attr:`settings.Settings.img_path`. Argument images should be without a
    file extension, and will be given the extension
    :py:attr:`settings.Settings.img_ext`.

    Args:
        rel_path (str): Path to the image from the base directory, without a
            file extension

    Returns:
        str: Full path to the image

    Examples
        ::

            # If `img_path` is "/home/user/projects/project/project/img" and
            # `img_ext` is ".png"
            gd.get_img_path("buttons/confirm")
            # "/home/user/projects/project/project/img/buttons/confirm.png"
    """
    ext = settings["img_ext"]
    if not ext.startswith("."):
        ext = f".{ext}"
    return os.path.join(settings["img_path"], f"{rel_path}{ext}")


def open_img(path: str, *, is_grayscale=False) -> cv.typing.MatLike:
    """Opens an image.

    Args:
        path (str): Full path to the image
        is_grayscale (bool, optional): Whether the image is already grayscale.
            Defaults to False.

    Returns:
        cv.typing.MatLike: Image in the BGR color space

    Raises:
        :py:class:`gamedriver.ReadImageError`
    """
    image = cv.imread(path, cv.IMREAD_GRAYSCALE) if is_grayscale else cv.imread(path)
    if image is None:
        raise ReadImageError(path)
    return image
