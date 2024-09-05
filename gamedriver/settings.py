from collections.abc import Callable
from typing import Optional, TypedDict

import cv2 as cv


class Settings(TypedDict):
    """GameDriver configuration."""

    #: How much to multiply :py:func:`gamedriver.wait` s by. Defaults to 1.
    wait_scale: float
    #: How much to add to :py:func:`gamedriver.wait` s. Defaults to 0.
    wait_offset: float

    #: Path to the template image directory. Recommend using an absolute path.
    #: Defaults to "".
    img_path: str
    #: File extension for template images. Defaults to ".png".
    img_ext: str

    #: Returns the screen [height, width, channel] in the BGR color space.
    #: Required for template matching that uses the device screen.
    get_screen: Callable[[], cv.typing.MatLike]
    #: How often the screen is checked in explicit wait operations. For example
    #: when using :py:func:`gamedriver.wait_until_img_visible`. Defaults to
    #: 1000 (1s).
    refresh_rate_ms: int

    #: Taps an (`x`, `y`) coordinate. Required for all tap-based interactions.
    tap_xy: Callable[[int, int], None]
    #: Swipes from (`x1`, `y1`) to (`x2`, `y2`) in `duration_ms` milliseconds.
    #: Required for all swipe interactions.
    swipe: Callable[[int, int, int, int, Optional[int]], None]


def _raise_default_setting_err(prop: str) -> None:
    raise ValueError(f"{prop} setting not set")


default_settings: Settings = {
    "wait_scale": 1,
    "wait_offset": 0,
    "img_path": "",
    "img_ext": ".png",
    "get_screen": lambda: _raise_default_setting_err("get_screen"),
    "refresh_rate_ms": 1_000,
    "tap_xy": lambda *args: _raise_default_setting_err("tap_xy"),
    "swipe": lambda *args: _raise_default_setting_err("swipe"),
}


settings: Settings = default_settings


def set_settings(s: Settings) -> None:
    """Sets multiple settings.

    A convenient way to set multiple settings at once. Only settings set in
    this way will be affected - existing settings that are not set remain
    unaffected.

    Args:
        s (Settings): Partial settings dictionary with the settings to be set
    """
    for k, v in s.items():
        settings[k] = v
