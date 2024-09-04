from collections.abc import Callable
from typing import Optional, TypedDict

import cv2 as cv


class Settings(TypedDict):
    wait_scale: float
    wait_offset: float

    img_path: str
    img_ext: str

    get_screen: Callable[[], cv.typing.MatLike]
    refresh_rate_ms: int

    tap_xy: Callable[[int, int], None]
    # x1 y1 x2 y2 [duration_ms]
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
    for k, v in s.items():
        settings[k] = v
