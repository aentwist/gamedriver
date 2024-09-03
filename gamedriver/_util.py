import os
import time

import cv2 as cv

from gamedriver.settings import settings


def tap_xy(x: int, y: int) -> None:
    settings["tap_xy"](x, y)


def swipe(x1: int, y1: int, x2: int, y2: int, duration_ms: int = None) -> None:
    settings["swipe"](x1, y1, x2, y2, duration_ms)


def wait(seconds=1.0) -> None:
    """Sleeps for a time, taking into account the wait scale and wait offset

    Args:
        seconds (float, optional): seconds to sleep for. Defaults to 1.
    """
    time.sleep(settings["wait_scale"] * seconds + settings["wait_offset"])


def get_screen(*, grayscale: bool = None) -> cv.typing.MatLike:
    settings["get_screen"](grayscale)


def get_pixel(x: int, y: int) -> tuple[int, int, int]:
    return get_screen()[y, x]


def get_img_path(rel_path: str) -> str:
    ext = settings["img_ext"]
    if not ext.startswith("."):
        ext = f".{ext}"
    return os.path.join(settings["img_path"], f"{rel_path}{ext}")
