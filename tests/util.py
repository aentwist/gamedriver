import os

from tests import TEST_DIR


def get_test_img_path(rel_path: str) -> str:
    return os.path.join(TEST_DIR, f"{rel_path}.png")
