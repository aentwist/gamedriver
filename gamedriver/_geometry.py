from typing import NamedTuple

from gamedriver._util import tap_xy


class Point(NamedTuple):
    x: int
    y: int


class Box(NamedTuple):
    left: int
    top: int
    right: int
    bottom: int


def get_center(box: Box) -> Point:
    x_mid = round((box.left + box.right) / 2)
    y_mid = round((box.top + box.bottom) / 2)
    return Point(x_mid, y_mid)


def tap_box(box: Box) -> None:
    center = get_center(box)
    tap_xy(center.x, center.y)
