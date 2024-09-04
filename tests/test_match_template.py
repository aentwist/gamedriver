import cv2 as cv
import pytest

import gamedriver as gd
from tests.util import get_test_ss_path as ss, get_test_templ_path as templ


def test_match_template():
    box = gd.match_template(ss("campaign"), templ("begin"))
    assert box, "matches"
    loc = gd.Box(left=320, top=1602, right=760, bottom=1729)
    assert box == loc, "match has the correct location"


def test_match_template_false_positive():
    box = gd.match_template(ss("campaign"), templ("campaign-unselected"))
    assert not box


def test_match_template_matches_inside_bounding_box():
    box = gd.match_template(
        ss("campaign"),
        templ("begin"),
        bounding_box=gd.Box(left=320, top=1000, right=760, bottom=1920),
    )
    assert box


def test_match_template_doesnt_match_outside_bounding_box():
    box = gd.match_template(
        ss("campaign"),
        templ("begin"),
        bounding_box=gd.Box(left=320, top=0, right=760, bottom=1000),
    )
    assert not box


def test_match_template_restrictive_bounding_box():
    box = gd.match_template(
        ss("campaign"),
        templ("begin"),
        bounding_box=gd.Box(left=300, top=1605, right=800, bottom=1800),
    )
    assert box, "matches"
    assert box.top == 1605, "match location is restricted based on the bounding box"


def test_match_template_bounding_box_too_small():
    with pytest.raises(ValueError):
        gd.match_template(
            ss("campaign"),
            templ("begin"),
            bounding_box=gd.Box(left=300, top=1600, right=400, bottom=1800),
        )


def test_match_template_is_grayscale():
    box = gd.match_template(
        ss("bounty-board-gray"), templ("dispatch-blue-gray"), is_grayscale=True
    )
    assert box


def test_match_template_method():
    box = gd.match_template(ss("campaign"), templ("begin"), method=cv.TM_CCOEFF_NORMED)
    assert box


def test_match_template_all():
    boxes = list(gd.match_template_all(ss("bounty-board"), templ("dispatch-brown")))
    assert len(boxes) == 5


def test_match_template_all_convert_to_grayscale():
    # A similar button but with a different color should also match
    boxes = list(gd.match_template_all(ss("bounty-board"), templ("dispatch-blue")))
    assert len(boxes) == 2

    # Now the incorrect button match should be eliminated
    boxes = list(
        gd.match_template_all(
            ss("bounty-board"), templ("dispatch-blue"), convert_to_grayscale=False
        )
    )
    assert len(boxes) == 1


def test_match_template_all_threshold_sqdiff():
    tight = list(
        gd.match_template_all(
            ss("bounty-board"), templ("dispatch-blue"), threshold=0.01
        )
    )
    loose = list(
        gd.match_template_all(
            ss("bounty-board"), templ("dispatch-blue"), threshold=0.07
        )
    )
    assert len(tight) < len(loose)


def test_match_template_all_threshold_ccoeff():
    tight = list(
        gd.match_template_all(
            ss("bounty-board"),
            templ("dispatch-blue"),
            method=cv.TM_CCOEFF_NORMED,
            threshold=0.9,
        )
    )
    loose = list(
        gd.match_template_all(
            ss("bounty-board"),
            templ("dispatch-blue"),
            method=cv.TM_CCOEFF_NORMED,
            threshold=0.3,
        )
    )
    assert len(tight) < len(loose)
