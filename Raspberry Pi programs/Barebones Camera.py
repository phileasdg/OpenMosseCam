# TODO: Learn basic OpenCV

import cv2 as cv
import sys

img = cv.imread(r"C:\Users\phile\OneDrive\Bureau\openCVtest\Erotische_Aufnahme_c1880s.jpg")
if img is None:
    sys.exit("Could not read image")

cv.imshow("Display window", img)
k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite("starry_night.png", img)