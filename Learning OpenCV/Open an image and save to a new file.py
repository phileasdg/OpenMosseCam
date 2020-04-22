# Opens an image, displays it in a window and saves it to a new file when the user presses a key on the keyboard

import cv2 as cv
import sys

img = cv.imread(r"C:\Users\phile\OneDrive\Bureau\openCVtest\Erotische_Aufnahme_c1880s.jpg")
if img is None:
    sys.exit("Could not read image")

cv.imshow("Display window", img)
k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite("starry_night.png", img)
