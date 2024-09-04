from unittest.mock import Mock, patch

import gamedriver as gd


def test_get_center():
    box = gd.Box(left=0, top=10, right=10, bottom=20)
    center = gd.get_center(box)
    assert isinstance(center, gd.Point)
    assert center == gd.Point(x=5, y=15)


@patch("gamedriver._geometry.tap_xy")
def test_tap_box(tap_xy: Mock):
    box = gd.Box(left=0, top=10, right=10, bottom=20)
    gd.tap_box(box)
    tap_xy.assert_called_once_with(5, 15)
