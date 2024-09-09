from unittest.mock import patch

import cv2 as cv
import pytest

import gamedriver as gd
from tests.util import get_test_ss_path as ss, get_test_templ_path as templ


@pytest.fixture
def locate_campaign_begin():
    with patch("gamedriver._tap_img.locate") as locate:
        locate.return_value = gd.Box(left=320, top=1602, right=760, bottom=1729)
        yield locate


@pytest.fixture
def locate_campaign_begin_delayed():
    with patch("gamedriver._tap_img.locate") as locate:
        locate.side_effect = [
            None,
            None,
            gd.Box(left=320, top=1602, right=760, bottom=1729),
            None,
        ]
        yield locate


@pytest.fixture
def locate_not_found():
    with patch("gamedriver._tap_img.locate") as locate:
        locate.return_value = None
        yield locate


# TODO: Some of this goes into locate and should be split out. locate itself
# should be mocked here.


@pytest.fixture
def get_screen():
    screen1 = cv.imread(ss("campaign"))
    screen2 = cv.imread(ss("bounty-board"))
    assert screen1 is not None and screen2 is not None

    with patch("gamedriver._locate.get_screen") as get_screen:
        get_screen.side_effect = [screen1, screen1, screen2, screen1]
        yield get_screen


@pytest.fixture
def get_img_path():
    with patch("gamedriver._tap_img.get_img_path") as get_img_path:
        get_img_path.side_effect = templ
        yield get_img_path


# Use a fast refresh to keep tests running fast
@pytest.fixture
def fast_refresh_settings():
    with patch.dict("gamedriver.settings.settings", {"refresh_rate_ms": 1}) as settings:
        yield settings


def test_wait_until_img_visible(
    locate_campaign_begin_delayed, get_img_path, fast_refresh_settings
):
    assert gd.wait_until_img_visible("dispatch-brown")
    assert locate_campaign_begin_delayed.call_count == 3


def test_wait_until_img_visible_timeout(
    locate_campaign_begin_delayed, get_img_path, fast_refresh_settings
):
    # Refresh rate of 1ms. 2ms / 1ms = 2 calls to get_screen. No match
    assert not gd.wait_until_img_visible("dispatch-brown", timeout_s=0.002)
    assert locate_campaign_begin_delayed.call_count == 2


@pytest.fixture
def tap_box():
    with patch("gamedriver._tap_img.tap_box") as tap_box:
        yield tap_box


def test_tap_img(locate_campaign_begin, tap_box):
    assert gd.tap_img("begin")
    locate_campaign_begin.assert_called_once()
    tap_box.assert_called_once()


def test_tap_img_not_found(locate_not_found, tap_box):
    assert not gd.tap_img("dispatch-brown")
    locate_not_found.assert_called_once()
    tap_box.assert_not_called()


def test_tap_img_when_visible_after_wait(get_screen, get_img_path, tap_box):
    with patch("gamedriver._tap_img.wait") as wait:
        assert gd.tap_img_when_visible_after_wait("dispatch-brown")
        wait.assert_called_with(1)


# covered above
def test_tap_img_when_visible():
    pass


# TODO: Improve
# TODO: Use better screen examples (additional tests) - e.g. where 1 button
# disappears but the other is still there, instead of them both disappearing
def test_tap_img_while_other_visible(get_screen, get_img_path, tap_box):
    gd.tap_img_while_other_visible("begin", "fast-rewards", frequency_s=0.001)
    assert tap_box.called


# covered above
def test_tap_img_while_visible():
    pass
