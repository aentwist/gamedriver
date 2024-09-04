import os

import cv2 as cv
from matplotlib import pyplot as plt

import gamedriver as gd
from tests import TEST_DIR


def get_test_ss_path(rel_path: str) -> str:
    return os.path.join(TEST_DIR, "ss", f"{rel_path}.png")


def get_test_templ_path(rel_path: str) -> str:
    return os.path.join(TEST_DIR, "templ", f"{rel_path}.png")


def print_img_matches(img: str, matches: list[gd.Box]) -> None:
    img_bgr = cv.imread(img)
    assert img_bgr is not None, f"failed to load image {img}"

    img_rgb = cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)
    for b in matches:
        cv.rectangle(img_rgb, (b.left, b.top), (b.right, b.bottom), (255, 0, 0), 3)

    plt.imshow(img_rgb)
    plt.show()
