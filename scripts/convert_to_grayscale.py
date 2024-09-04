import os
import sys

import cv2 as cv


arg_count = len(sys.argv)
assert arg_count == 2, f"expected 1 argument but got {arg_count}"
fname = sys.argv[1]

img_bgr = cv.imread(fname)
assert img_bgr is not None, f"failed to load image {fname}"
img_gray = cv.cvtColor(img_bgr, cv.COLOR_BGR2GRAY)
fname_no_ext, ext = os.path.splitext(fname)
cv.imwrite(f"{fname_no_ext}-gray{ext}", img_gray)
