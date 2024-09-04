from unittest.mock import Mock, patch

import cv2 as cv
import numpy as np

import gamedriver as gd
from gamedriver.settings import set_settings, settings
from tests.util import get_test_templ_path


@patch.dict("gamedriver._util.settings", {"tap_xy": Mock()})
def test_tap_xy():
    gd.tap_xy(0, 0)
    settings["tap_xy"].assert_called_once_with(0, 0)


@patch.dict("gamedriver._util.settings", {"swipe": Mock()})
def test_swipe():
    gd.swipe(0, 0, 100, 100, 200)
    settings["swipe"].assert_called_once_with(0, 0, 100, 100, 200)


@patch("gamedriver._util.time.sleep")
def test_wait(sleep: Mock):
    gd.wait(1)
    sleep.assert_called_once_with(1)


@patch("gamedriver._util.time.sleep")
@patch.dict("gamedriver._util.settings", {"wait_scale": 2})
def test_wait_scale(sleep: Mock):
    gd.wait(1)
    sleep.assert_called_once_with(2)


@patch("gamedriver._util.time.sleep")
@patch.dict("gamedriver._util.settings", {"wait_offset": 3})
def test_wait_offset(sleep: Mock):
    gd.wait(1)
    sleep.assert_called_once_with(4)


@patch.dict("gamedriver._util.settings", {"get_screen": Mock(return_value="my screen")})
def test_get_screen():
    screen = gd.get_screen()
    settings["get_screen"].assert_called_once_with()
    assert screen == "my screen"


def test_get_screen_grayscale():
    screen_bgr = cv.imread(get_test_templ_path("dispatch-blue"))
    screen_gray = cv.imread(
        get_test_templ_path("dispatch-blue-gray"), cv.IMREAD_GRAYSCALE
    )
    assert screen_bgr is not None and screen_gray is not None

    with patch.dict(
        "gamedriver._util.settings", {"get_screen": Mock(return_value=screen_bgr)}
    ):
        screen = gd.get_screen(grayscale=True)
    assert (screen == screen_gray).all()


@patch("gamedriver._util.get_screen")
def test_get_pixel(get_screen: Mock):
    PX = [255, 0, 0]
    screen = np.zeros((5, 5, 3))
    screen[3, 2, :] = PX
    get_screen.return_value = screen

    assert (gd.get_pixel(2, 3) == PX).all()


def test_get_img_path():
    IMG_PATH = "/path/to/img"
    EXT = ".jpg"
    set_settings({"img_path": IMG_PATH, "img_ext": EXT})

    assert gd.get_img_path("buttons/cancel") == f"{IMG_PATH}/buttons/cancel{EXT}"
