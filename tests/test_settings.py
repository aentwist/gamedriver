from unittest.mock import Mock, patch

import pytest

from gamedriver.settings import default_settings, set_settings, settings


def test_default_settings():
    assert settings is default_settings


def test_default_settings_get_screen():
    with pytest.raises(ValueError):
        settings["get_screen"]()


def test_default_settings_tap_xy():
    with pytest.raises(ValueError):
        settings["tap_xy"](0, 0)


def test_default_settings_swipe():
    with pytest.raises(ValueError):
        settings["swipe"](0, 0, 0, 0)


@patch.dict("gamedriver.settings.settings")
def test_set_settings():
    IMG_PATH = "/home/me/projects/project/project/img"
    REFRESH_RATE_MS = 3_000
    m = Mock()

    set_settings(
        {"img_path": IMG_PATH, "refresh_rate_ms": REFRESH_RATE_MS, "tap_xy": m}
    )
    assert settings["img_path"] == IMG_PATH
    assert settings["img_ext"] == ".png", "settings not set remain unchanged"
    assert settings["refresh_rate_ms"] == REFRESH_RATE_MS
    assert settings["tap_xy"] is m, "functions are set"
