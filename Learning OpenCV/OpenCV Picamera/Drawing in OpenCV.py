import numpy as np
import cv2 as cv
import os
import picamera
from picamera import PiCamera
import time
from datetime import datetime

# // Notes
# cv.rectangle(img, (point A x, y), (point B x, y), (B, G, R), thickness)
# img = cv.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# CAMERA INITIALISATION
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Camera settings
cam_width = 1280
cam_height = 480

# Final image capture settings
# scale_ratio = 1
scale_ratio = 0.5

# Camera resolution height must be dividable by 16, and width by 32
cam_width = int((cam_width+31)/32)*32
cam_height = int((cam_height+15)/16)*16
print ("Camera resolution: "+str(cam_width)+" x "+str(cam_height))

# Buffer for captured image settings
img_width = int (cam_width * scale_ratio)
img_height = int (cam_height * scale_ratio)
capture = np.zeros((img_height, img_width, 4), dtype=np.uint8)
print ("Scaled image resolution: "+str(img_width)+" x "+str(img_height))

# Initialize the camera
camera = PiCamera(stereo_mode='side-by-side',stereo_decimate=False)
camera.resolution=(cam_width, cam_height)
camera.framerate = 20
camera.hflip = True

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# GUI SETUP
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

cam_res_width = 640
cam_res_height = 480

# GUI reference variables:
marginX = int(cam_res_width / 32)
marginY = int(cam_res_height / 32)

# Colours and fonts:
WHITE = (255, 255, 255)
setting_value_font = cv.FONT_HERSHEY_PLAIN

# // UI BUILDING BLOCKS:
box1X, box1Y = int(cam_res_width - 6 * marginX), int(cam_res_height - 6 * marginY)

# Settings block (the settings rectangle):
x4thSettings = (box1X / 4)
y3rdSettings = (box1Y / 3)
# Settings cell:
# TODO: Button cell useful references to build icons
# Buttons Block:
y4thButtons = ((box1Y + 4 * marginY) / 4)

# Create a black image
main_img = np.zeros((cam_res_height, cam_res_width, 4), dtype=np.uint8)
main_img = cv.cvtColor(main_img, cv.COLOR_BGR2BGRA)

def draw_ui(current_display):

    # Draw UI rectangles:
    cv.rectangle(main_img, (2 * marginX + box1X, marginY), (5 * marginX + box1X, box1Y + 5 * marginY), (WHITE), 1)  # buttons
    cv.rectangle(main_img, (marginX, 2 * marginY + box1Y), (marginX + box1X, box1Y + 5 * marginY), (WHITE), 1)  # info
    if current_display != "viewFinder":
        cv.rectangle(main_img, (marginX, marginY), (marginX + box1X, marginY + box1Y), (WHITE), 1)  # top left
    else:
        # Capture frames from the camera
        for frame in camera.capture_continuous(capture, format="bgra", use_video_port=True,
                                               resize=(img_width, img_height)):
            cv.imshow("pair", frame)
            key = cv.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop and save last image
            if key == ord("q"):
                exit(0)
                break

    for i in range(3):
        cv.line(main_img, (2 * marginX + box1X, int(marginY + (i + 1) * y4thButtons)),
                (5 * marginX + box1X, int(marginY + (i + 1) * y4thButtons)), (WHITE), 1)

        if current_display == "settingsMenu":

            # Draw settings grid
            cv.line(main_img, (int(marginX + (i + 1) * x4thSettings), marginY),
                    (int(marginX + (i + 1) * x4thSettings), box1Y + marginY), (WHITE), 1)
            cv.line(main_img, (marginX, int(marginY + i * y3rdSettings)),
                    (box1X + marginX, int(marginY + i * y3rdSettings)), (WHITE), 1)

            # Draw settings Names:
            for k in sd.keys():
                print(k)
                print(int(sd[k][0][0][0]), int(sd[k][0][0][1]))
                cv.putText(main_img, k, (int(sd[k][0][0][0]), int(sd[k][0][0][1])), setting_value_font, 2, (WHITE), 2, cv.LINE_AA, False)

            # Draw settings names and icons TODO


                # cv.imshow("main img", main_img)
                # cv.waitKey(0)




                # Draw settings values TODO

                #     # draw settings names
                #     for k in sd.keys():
                #         textSurfaceObj = fontObj.render(k, True, WHITE)  # text, anti-aliasing, text colour, bg colour
                #         textRectObj = textSurfaceObj.get_rect()
                #         textRectObj.topleft = sd[k][0][0]
                #         DISPLAYSURF.blit(textSurfaceObj, textRectObj)
                #
                #     # draw settings values
                #     for setting in sl:
                #         fontObj = pygame.font.Font(None, 30)  # font, font size
                #         textSurfaceObj = fontObj.render(str(sd[setting][1][scvil[sl.index(setting)]]), True,
                #                                         WHITE)  # text, anti-aliasing, text colour, bg colour
                #         textRectObj = textSurfaceObj.get_rect()
                #         textRectObj.topleft = sd[setting][0][1]
                #         DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    # Draw button descriptions TODO
    # Draw current settings description TODO
    cv.putText(main_img, 'OpenCV', (marginX, box1Y + 5 * marginY), setting_value_font, 3, (WHITE), 2, cv.LINE_AA)



# settings list
sl = ["Mode", "Active Camera(s)", "Shutter", "ISO", "AWB", "Red gain", "Blue gain", "Effect", "Resolution", "Crop", "Format", "fps"]  # TODO: framerate and crop

sd = {
    # TODO: reformat and clean up when finished
    # "Reference": [["key blit xy (x, y)", "value blit xy (x, y)"], ["list of setting values"]], TODO!!!!!!!!!!!!!!!!!!
    "Mode": [[(marginX, marginY), (marginX, marginY+(y3rdSettings/2))], ["photo", "video"]],
    "Active Camera(s)": [[(marginX+x4thSettings, marginY),(marginX+x4thSettings, marginY+(y3rdSettings/2))], ["left camera", "right camera", "stereo", "3D overlap"]],
    "Shutter": [[(marginX+(2*x4thSettings), marginY), (marginX+(2*x4thSettings), marginY+(y3rdSettings/2))], [("auto", 0), ("1/8000", 125), ("1/6400", 156),
                ("1/5000", 200), ("1/4000", 250), ("1/3200", 312), ("1/2500", 400), ("1/2000", 500), ("1/1600", 625),
                ("1/1250", 800), ("1/1000", 1000), ("1/800", 1250), ("1/640", 1562), ("1/500", 2000), ("1/400", 2500),
                ("1/320", 3125), ("1/250", 4000), ("1/200", 5000), ("1/160", 6250), ("1/125", 8000), ("1/100", 10000),
                ("1/80", 12500), ("1/60", 16666), ("1/50", 20000), ("1/40", 25000), ("1/30", 33333), ("1/25", 40000),
                ("1/20", 50000), ("1/15", 66666), ("1/13", 76923), ("1/10", 100000), ("1/8", 125000), ("1/6", 166666),
                ("1/5", 200000), ("1/4", 250000), ("0.3", 300000), ("0.4", 400000), ("0.5", 500000), ("0.6", 600000),
                ("0.8", 800000), ("1", 1000000), ("1.3", 1300000), ("1.6", 1600000), ("2", 2000000), ("2.5", 2500000),
                ("3.2", 3200000), ("4", 4000000), ("5", 5000000), ("6", 6000000)]],
    "ISO": [[(marginX+(3*x4thSettings), marginY), (marginX+(3*x4thSettings), marginY+(y3rdSettings/2))], [0, 100, 160, 200, 250, 320, 400, 500, 640, 800]],
    "AWB": [[(marginX, marginY+y3rdSettings), (marginX, marginY+y3rdSettings+(y3rdSettings/2))], ["off", "greyworld", "auto", "sunlight", "cloudy", "shade", "tungsten",
                                       "fluorescent", "incandescent", "flash", "horizon"]],
    # TODO: the solution for blue gain and red gain above is pretty poor. To improve.
    "Red gain": [[(marginX+x4thSettings, marginY+y3rdSettings), (marginX+x4thSettings, marginY+y3rdSettings+(y3rdSettings/2))], [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
                 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1,
                 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2,
                 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0]],
    "Blue gain": [[(marginX+(2*x4thSettings), marginY+y3rdSettings), (marginX+(2*x4thSettings), marginY+y3rdSettings+(y3rdSettings/2))], [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
                  2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1,
                  4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2,
                  6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0]],
    "Effect": [[(marginX+(3*x4thSettings), marginY+y3rdSettings), (marginX+(3*x4thSettings), marginY+y3rdSettings+(y3rdSettings/2))], ["none", "negative", "solarize", "hatch", "gpen", "film", "colorswap",
                                          "washedout", "colorbalance", "cartoon"]],
    # effects availablee: 'none', 'negative', 'solarize', 'sketch', 'denoise', 'emboss', 'oilpaint', 'hatch', 'gpen',
    # 'pastel', 'watercolor', 'film', 'blur', 'saturation', 'colorswap', 'washedout', 'posterise', 'colorpoint',
    # 'colorbalance', 'cartoon', 'deinterlace1', 'deinterlace2'

    "Resolution": [[(marginX, marginY+(2*y3rdSettings)), (marginX, marginY+(2*y3rdSettings)+(y3rdSettings/2))], [(1980, 1080), (1080, 720)]],  # limited number of tuples, different
    "Crop": [[(marginX+x4thSettings, marginY+(2*y3rdSettings)), (marginX+x4thSettings, marginY+(2*y3rdSettings)+(y3rdSettings/2))], [(0, 0)]],  # TODO
    "Format": [[(marginX+(2*x4thSettings), marginY+(2*y3rdSettings)), (marginX+(2*x4thSettings), marginY+(2*y3rdSettings)+(y3rdSettings/2))], ["jpg", "png"]],
    "fps": [[(marginX+(3*x4thSettings), marginY+(2*y3rdSettings)), (marginX+(3*x4thSettings), marginY+(2*y3rdSettings)+(y3rdSettings/2))], [30]]  # TODO

}

display_modes = ["viewFinder", "settingsMenu", "gallery"]
current_display = display_modes[1]
draw_ui(current_display)

cv.imshow("image", main_img)
cv.waitKey(0)
