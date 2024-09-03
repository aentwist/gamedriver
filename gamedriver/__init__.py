from gamedriver._geometry import Box, get_center, Point, tap_box
from gamedriver._locate import locate, locate_all
from gamedriver._match_template import match_template, match_template_all
from gamedriver._tap_img import (
    tap_img,
    tap_img_when_visible,
    tap_img_when_visible_after_wait,
    tap_img_while_other_visible,
    tap_img_while_visible,
    wait_until_img_visible,
)
from gamedriver._util import get_img_path, get_pixel, get_screen, swipe, tap_xy, wait

from gamedriver.logger import _setup_logging


_setup_logging()
