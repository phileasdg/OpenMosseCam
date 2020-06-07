import RPi.GPIO as GPIO
from time import sleep
import pygame
import sys
from pygame.locals import *
import cv2
import numpy as np
import time
import picamera
import picamera.array
import os

# -------------------------------------------------------------------------------------------------------------------- #
# PROGRAM GLOBAL VARIABLE DECLARATIONS
# -------------------------------------------------------------------------------------------------------------------- #

# Saving and displaying pictures and video
save_directory = "/home/pi/Desktop/OpenMosseCam/DCIM"
savedFilePathList = []  # saved file path list
sfpli = 0  # saved file path list index

# Program state
currentDisplay = "viewFinder"
video_recording = False
vid_capture_user_init = False  # becomes true when user first presses capture on video mode
infoOverlay = True
csi = 0  # current setting index, defaults to Mode
requireReInit = False  # whether PiCamera objects should be re-initialise

# Camera program GUI assets
setting_header_dir = r"/home/pi/Desktop/OpenMosseCam/Raspberry Pi programs/app_icons/Ready for program/setting_cell_icons_transparent"
button_icon_dir = r"/home/pi/Desktop/OpenMosseCam/Raspberry Pi programs/app_icons/Ready for program/button_icons_transparent"

# Global camera setting values
Mode = active_cameras = Shutter = ISO = AWB = Red_gain = Blue_gain = Effect = Resolution = Crop = Format = fps = None
camResX = camResY = None  # PiCamera resolution values
c_num = None  # PiCamera camera number
s_mode = None  # PiCamera stereo mode

# -------------------------------------------------------------------------------------------------------------------- #
# PiCamera setup
# -------------------------------------------------------------------------------------------------------------------- #

camera = None
# camera = picamera.PiCamera(camera_num=c_num, stereo_mode=s_mode, stereo_decimate=False, led_pin=3)
# camera_num options = [0, 1]
# stereo mode options = ['none', 'side-by-side', top-bottom]

# Important: Camera resolution height must be dividable by 16, and width by 32 TODO: check if this is still true

# -------------------------------------------------------------------------------------------------------------------- #
# OpenCV setup
# -------------------------------------------------------------------------------------------------------------------- #

# Video stream
video = picamera.array.PiRGBArray(camera)
globalFrame = None

# videoCapture object
video_out = None

# -------------------------------------------------------------------------------------------------------------------- #
# GPIO SETUP
# -------------------------------------------------------------------------------------------------------------------- #

buttons = {1: 17, 2: 22, 3: 23, 4: 27}
GPIO.setmode(GPIO.BCM)
for value in buttons.values():
    GPIO.setup(value, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTIONS DECLARATIONS
# -------------------------------------------------------------------------------------------------------------------- #

# Buttons
def capture():
    global globalFrame, video_recording, video_out, camResX, camResY
    # run function
    if sd["Mode"][1][scvil[0]] == "Photo":
        imgFileName = "image " + str(time.ctime()) + "." + sd["Format"][1][scvil[10]]
        cv2.imwrite(os.path.join(save_directory, imgFileName), globalFrame)
    elif sd["Mode"][1][scvil[0]] == "Video":

        video_recording = not video_recording

        if video_recording:
            # videoCapture object
            imgFileName = "video " + str(time.ctime()) + "." + sd["Format"][1][scvil[10]]
            fourcc = cv2.VideoWriter_fourcc(*'MPEG')
            video_out = cv2.VideoWriter(os.path.join(save_directory, imgFileName), fourcc, 2, (camResX, camResY))

        print("video recording status: ", video_recording)
def toggle_info():
    global infoOverlay
    infoOverlay = not infoOverlay
def settings_menu():
    global currentDisplay

    currentDisplay = "settingsMenu"

    # update gui display
    DISPLAYSURF.fill(BLACK)

    # settings GUI top left corner list (x n x4thSettings, y n y3rdSettings)
    sguil = [[0, 0], [1, 0], [2, 0], [3, 0], [0, 1], [1, 1], [2, 1], [3, 1], [0, 2], [1, 2], [2, 2], [3, 2]]

    # highlight the selected setting (draw green box behind the selected setting)
    pygame.draw.rect(DISPLAYSURF, GREEN,
                     (marginX + (sguil[csi][0] * x4thSettings), marginY + (sguil[csi][1]* y3rdSettings),
                      x4thSettings, y3rdSettings), 5)  # settings rect

    # draw setting titles to GUI from images
    setting_titles_paths = []
    for path in os.listdir(setting_header_dir):
        setting_titles_paths.append(os.path.join(setting_header_dir, path))

    for k in sd.keys():
        img = pygame.image.load(os.path.join(setting_header_dir, (k + ".PNG")))
        DISPLAYSURF.blit(img, sd[k][0][0])

    # alternative option for drawing setting titles to GUI using texts objects
    # for k in sd.keys():
    #     fontObj = pygame.font.Font(None, 30)  # font, font size
    #     textSurfaceObj = fontObj.render(k, True, WHITE)  # text, anti-aliasing, text colour, bg colour
    #     textRectObj = textSurfaceObj.get_rect()
    #     textRectObj.topleft = sd[k][0][0]
    #     DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    # draw settings values
    for setting in sl:
        fontObj = pygame.font.Font(None, 30)  # font, font size
        textSurfaceObj = fontObj.render(str(sd[setting][1][scvil[sl.index(setting)]]), True, WHITE)
        # ^^ text, anti-aliasing, text colour, bg colour
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = sd[setting][0][1]
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    # draw settings box
    pygame.draw.rect(DISPLAYSURF, WHITE, (marginX, marginY, GUIx, GUIy), 1)  # settings rect

    # Draw grid lines
    for i in range(3):
        pygame.draw.line(DISPLAYSURF, WHITE, (int(marginX + (i + 1) * x4thSettings), marginY),
                         (int(marginX + (i + 1) * x4thSettings), GUIy + marginY), 1)  # x4ths
        pygame.draw.line(DISPLAYSURF, WHITE, (marginX, int(marginY + i * y3rdSettings)),
                         (GUIx + marginX, int(marginY + i * y3rdSettings)), 1)  # y3rds
        # point 2 is always GUIsize + margin because we are matching with a rect declared using xy of A followed by
        # width and height rather than xy of point D
    draw_base_ui_overlay()
def gallery():
    global currentDisplay, savedFilePathList, sfpli

    # run function
    currentDisplay = "gallery"

    # list files in save directory
    for path in os.listdir(save_directory):
        if path.endswith(("jpg", "png")):
            savedFilePathList.append(os.path.join(save_directory, path))

    # update gui display
    DISPLAYSURF.fill(BLACK)
    if len(savedFilePathList) == 0:
        fontObj = pygame.font.Font(None, 50)  # font, font size
        textSurfaceObj = fontObj.render("Image and video folder empty", True, WHITE)
        # ^^ text, anti-aliasing, text colour, bg colour
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (marginX + int(GUIx / 2), marginY + int(GUIy / 2))
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    else:
        # load image to pygame
        img = pygame.image.load(savedFilePathList[sfpli])

        # resize image to fit display box
        imgWidth = img.get_width()
        imgHeight = img.get_height()
        if max(imgWidth, imgHeight) is imgWidth:
            refDivider = imgWidth / GUIx
        else:
            refDivider = imgHeight / GUIy
        imgWidth /= refDivider
        imgHeight /= refDivider

        img = pygame.transform.scale(img, (int(imgWidth), int(imgHeight)))
        # blit image to pygame
        DISPLAYSURF.blit(img, (marginX + int((GUIx-imgWidth)/2), marginY + int((GUIy-imgHeight)/2)))

    # draw settings box
    pygame.draw.rect(DISPLAYSURF, WHITE, (marginX, marginY, GUIx, GUIy), 1)  # settings rect

    draw_base_ui_overlay()

def return_to_viewfinder():
    global requireReInit

    global currentDisplay
    currentDisplay = "viewFinder"

    # update camera settings
    if requireReInit:
        re_init_camera_object()
    update_camera_settings()
def next_up():
    global savedFilePathList, sfpli, requireReInit
    # run function and update GUI display
    if currentDisplay == "settingsMenu":
        if 0 <= scvil[csi] < len(sd[sl[csi]][1]) - 1:  # note the "-1", it is important.
            # current setting value from index in list of values in dictionary += 1
            scvil[csi] += 1
        # sets setting index value to 0
        else:
            scvil[csi] = 0
        settings_menu()

        # re-init camera if there is a user request to do so
        if csi == 1:
            requireReInit = True

    elif currentDisplay == "gallery":
        if 0 <= sfpli < len(savedFilePathList) - 1:
            sfpli += 1
        else:
            sfpli = 0
        gallery()
def next_down():
    global savedFilePathList, sfpli, requireReInit
    # run function and update GUI display
    if currentDisplay == "settingsMenu":
        if 0 < scvil[csi] <= len(sd[sl[csi]][1]):
            # current setting value from index in list of values in dictionary -= 1
            scvil[csi] -= 1
        # sets setting index value to the highest index in the list
        else:
            scvil[csi] = len(sd[sl[csi]][1]) - 1
        settings_menu()

        # re-init camera if there is a user request to do so

        if csi == 1:
            requireReInit = True

    elif currentDisplay == "gallery":
        if 0 < sfpli <= len(savedFilePathList):
            sfpli -= 1
        else:
            sfpli = len(savedFilePathList) - 1
        gallery()
def change_setting():
    # run function
    global csi
    if 0 <= csi < (len(sl)-1):  # between 0 and highest index in sl (settings list)
        csi += 1
    else:
        csi = 0

    # update gui display
    settings_menu()
def delete():
    pass

# Program execution
def listen_for_button_press():
    global infoOverlay

    for k, v in buttons.items():
        if GPIO.input(v) == False:  # for any GPIO input equal to a value from the button dictionary

            # Toggle infoOverlay if user presses a button other than button 2
            if v in [17, 23, 27]:
                infoOverlay = True

            df[currentDisplay]["Button" + str(k)][0]()  # run function associated with button

            sleep(0.25)
def re_init_camera_object():
    global resX, resY, s_mode, c_num, frameblitX, frameblitY, camera, video, camResX, camResY

    # update the video frame blit coordinates
    frameblitX, frameblitY = acmpl[scvil[1]][2]

    # update the picamera object camera number and stereo mode
    c_num = acmpl[scvil[1]][0]
    s_mode = acmpl[scvil[1]][1]
    if camera is not None:
        camera.close()
    camera = picamera.PiCamera(camera_num=c_num, stereo_mode=s_mode, stereo_decimate=False, led_pin=3)

    # update camera resolution
    # define and apply resolutions to fit active camera settings
    camResX, camResY = sd["Resolution"][1][scvil[8]]
    camResX *= acmpl[scvil[1]][3][0]
    camResY *= acmpl[scvil[1]][3][1]
    camera.resolution = (camResX, camResY)

    # re-declare video stream
    video = picamera.array.PiRGBArray(camera)

    # update image rescale to fit pitft LCD
    resX, resY = camera.resolution
    if max(resX, resY) is resX:
        refDivider = resX / dX
    else:
        refDivider = resY / dY
    resX /= refDivider
    resY /= refDivider
def update_camera_settings():
    global camera, Shutter, ISO, AWB, Red_gain, Blue_gain, Effect, Resolution, fps
    global camResX, camResY
    global video_out

    # Check setting values
    Shutter = sd["Shutter"][1][scvil[2]][1]
    ISO = sd["ISO"][1][scvil[3]]
    AWB = sd["AWB"][1][scvil[4]]
    Red_gain = sd["Red gain"][1][scvil[5]]
    Blue_gain = sd["Blue gain"][1][scvil[6]]
    Effect = sd["Effect"][1][scvil[7]]
    Resolution = sd["Resolution"][1][scvil[8]]
    fps = sd["fps"][1][scvil[11]]

    # update camera resolution
    # define and apply resolutions to fit active camera settings
    camResX, camResY = sd["Resolution"][1][scvil[8]]
    camResX *= acmpl[scvil[1]][3][0]
    camResY *= acmpl[scvil[1]][3][1]
    camera.resolution = (camResX, camResY)

    # Update camera settings
    camera.shutter_speed = Shutter
    camera.iso = ISO
    camera.awb_mode = AWB  # TODO: figure out why it doesn't show white balance change on video feed
    camera.awb_gains = (Red_gain, Blue_gain)  # TODO: figure out why it doesn't apply the gains
    camera.framerate = fps

# User interfaces (GUI, CLI)
def draw_base_ui_overlay():
    global bodyFontObj

    # draw button icons
    button_icons_paths = []
    for path in os.listdir(button_icon_dir):
        button_icons_paths.append(os.path.join(button_icon_dir, path))

    # draw description rect text
    description_text = ["text line 1 here", "text line 2 here"]
    for i in range(len(description_text)):
        textSurfaceObj = bodyFontObj.render((description_text[i]), True, WHITE)
        # ^^ text, anti-aliasing, text colour, bg colour
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = (marginX, 2 * marginY + GUIy + ((3 * marginY)/len(description_text))*i)
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    for i in range(4):
        img = pygame.image.load(os.path.join(button_icon_dir, (df[currentDisplay]["Button" + str(i + 1)][1] + ".PNG")))
        DISPLAYSURF.blit(img, (2 * marginX + GUIx, marginY + (i * y4thButtons)))

    # draw ui base ui wireframe
    pygame.draw.rect(DISPLAYSURF, WHITE, (2 * marginX + GUIx, marginY, 3 * marginX, GUIy + 4 * marginY), 1)  # buttons rect
    pygame.draw.rect(DISPLAYSURF, WHITE, (marginX, 2 * marginY + GUIy, GUIx, 3 * marginY), 1)  # bottom rect, description rect
    for i in range(3):
        pygame.draw.line(DISPLAYSURF, WHITE, (2 * marginX + GUIx, int(marginY + (i + 1) * y4thButtons)),
                         (5 * marginX + GUIx, int(marginY + (i + 1) * y4thButtons)), 1)  # y4ths
def draw_camera_video_stream():
    global frameblitX, frameblitY, resX, resY, globalFrame
    for frameBuf in camera.capture_continuous(video, format="rgb", use_video_port=True):

        globalFrame = cv2.cvtColor(np.flipud(frameBuf.array), cv2.COLOR_RGB2BGR)
        frame = cv2.resize(np.rot90(frameBuf.array, 3), (int(resY), int(resX)))

        video.truncate(0)
        frame = pygame.surfarray.make_surface(frame)
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(frame, (frameblitX, frameblitY))

        if infoOverlay:
            draw_base_ui_overlay()

        pygame.display.update()
        break

# -------------------------------------------------------------------------------------------------------------------- #
# PYGAME GUI SETUP
# -------------------------------------------------------------------------------------------------------------------- #

# Display settings
pygame.display.init()
info = pygame.display.Info()
dX, dY = info.current_w, info.current_h  # display resolution
# dX, dY = 640, 480 # use if you want to set the display res to custom values

# GUI margins
marginX = int(dX / 32)
marginY = int(dY / 32)

# GUI boundaries and building blocks
GUIx, GUIy = int(dX - 6 * marginX), int(dY - 6 * marginY)  # GUI display size (dX or dY - at least 2* margin of X or Y)
# Settings box
x4thSettings = (GUIx / 4)
y3rdSettings = (GUIy / 3)
# Buttons Block
y4thButtons = ((GUIy + 4 * marginY) / 4)

# Resized video feed frame dimensions
resX = resY = None

# Video stream frame blit coordinates
frameblitX = frameblitY = None

# GUI colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Start Pygame
pygame.init()
DISPLAYSURF = pygame.display.set_mode((dX, dY))  # , pygame.FULLSCREEN)

# Fonts
bodyFontObj = pygame.font.Font(None, 30)  # font, font size

# -------------------------------------------------------------------------------------------------------------------- #
# MENU STRUCTURE AND SETTINGS SETUP
# -------------------------------------------------------------------------------------------------------------------- #

# display functions - displayFunctions = { currentDisplay: { Button: [function to run, function description,
# function button icon name] } }
df = {
    "viewFinder": {
        "Button1": [capture, "capture"],  # [name the function without brackets, cli description]
        "Button2": [toggle_info, "info"],
        "Button3": [settings_menu, "settings"],
        "Button4": [gallery, "gallery"]
    },
    "settingsMenu": {
        "Button1": [return_to_viewfinder, "return"],
        "Button2": [next_up, "up"],
        "Button3": [next_down, "down"],
        "Button4": [change_setting, "changeset"]
    },
    "gallery": {
        "Button1": [return_to_viewfinder, "return"],
        "Button2": [next_up, "up"],
        "Button3": [next_down, "down"],
        "Button4": [delete, "del"]
    }
}  # contains map of functions and their button assignment for different displays

# settings list
sl = ["Mode", "Active Camera(s)", "Shutter", "ISO", "AWB", "Red gain", "Blue gain", "Effect", "Resolution", "Crop",
      "Format", "fps"]

# settings current value index list
scvil = [
    0,  # 1) Mode index from list of strings (only two)
    2,  # 2) Active Camera index from list of strings
    0,  # 3) Shutter index from list of tuples: [("human value", computer value), ...]
    0,  # 4) ISO index from list of integers
    0,  # 5) AWB index from list of strings
    0,  # 6) Red gain value = value between 1 and 9
    0,  # 7) Blue gain value = value between 1 and 9
    0,  # 8) Effect index from list of strings
    0,  # 9) Photo and video resolution indexes from list of tuples [(x, y),(x, y), ...]
    0,  # 10) Crop (TBD) TODO
    0,  # 11) Format index from list of strings
    0,  # 12) fps (TBD) TODO
]

# settings dictionary - key: [[GUI coordinates of setting headers, coordinates of setting values][setting values list]]
sd = {
    "Mode": [[(marginX, marginY), (marginX, marginY + (y3rdSettings / 2))],
             ["Photo", "Video"]],
    "Active Camera(s)": [[(marginX + x4thSettings, marginY), (marginX + x4thSettings, marginY + (y3rdSettings / 2))],
                         ["left camera", "right camera", "stereo lr", "stereo tb", "stereo rl", "stereo bt"]],
    "Shutter": [[(marginX + (2 * x4thSettings), marginY), (marginX + (2 * x4thSettings), marginY + (y3rdSettings / 2))],
                [("auto", 0), ("1/8000", 125), ("1/6400", 156), ("1/5000", 200), ("1/4000", 250), ("1/3200", 312),
                 ("1/2500", 400), ("1/2000", 500), ("1/1600", 625), ("1/1250", 800), ("1/1000", 1000), ("1/800", 1250),
                 ("1/640", 1562), ("1/500", 2000), ("1/400", 2500), ("1/320", 3125), ("1/250", 4000), ("1/200", 5000),
                 ("1/160", 6250), ("1/125", 8000), ("1/100", 10000), ("1/80", 12500), ("1/60", 16666), ("1/50", 20000),
                 ("1/40", 25000), ("1/30", 33333), ("1/25", 40000), ("1/20", 50000), ("1/15", 66666), ("1/13", 76923),
                 ("1/10", 100000), ("1/8", 125000), ("1/6", 166666), ("1/5", 200000), ("1/4", 250000), ("0.3", 300000),
                 ("0.4", 400000), ("0.5", 500000), ("0.6", 600000), ("0.8", 800000), ("1", 1000000), ("1.3", 1300000),
                 ("1.6", 1600000), ("2", 2000000), ("2.5", 2500000), ("3.2", 3200000), ("4", 4000000), ("5", 5000000),
                 ("6", 6000000)]],
    "ISO": [[(marginX + (3 * x4thSettings), marginY), (marginX + (3 * x4thSettings), marginY + (y3rdSettings / 2))],
            [0, 100, 160, 200, 250, 320, 400, 500, 640, 800]],
    "AWB": [[(marginX, marginY + y3rdSettings), (marginX, marginY + y3rdSettings + (y3rdSettings / 2))],
            ["off", "greyworld", "auto", "sunlight", "cloudy", "shade", "tungsten", "fluorescent", "incandescent",
             "flash", "horizon"]],
    "Red gain": [[(marginX + x4thSettings, marginY + y3rdSettings),
                  (marginX + x4thSettings, marginY + y3rdSettings + (y3rdSettings / 2))],
                 [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9,
                  2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9,
                  4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9,
                  6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9,
                  8.0]],
    "Blue gain": [[(marginX + (2 * x4thSettings), marginY + y3rdSettings),
                   (marginX + (2 * x4thSettings), marginY + y3rdSettings + (y3rdSettings / 2))],
                  [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9,
                   2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9,
                   4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9,
                   6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9,
                   8.0]],
    "Effect": [[(marginX + (3 * x4thSettings), marginY + y3rdSettings),
                (marginX + (3 * x4thSettings), marginY + y3rdSettings + (y3rdSettings / 2))],
               ["none", "negative", "solarize", "hatch", "gpen", "film", "colorswap", "washedout", "colorbalance",
                "cartoon"]],
    # effects availablee: 'none', 'negative', 'solarize', 'sketch', 'denoise', 'emboss', 'oilpaint', 'hatch', 'gpen',
    # 'pastel', 'watercolor', 'film', 'blur', 'saturation', 'colorswap', 'washedout', 'posterise', 'colorpoint',
    # 'colorbalance', 'cartoon', 'deinterlace1', 'deinterlace2'
    "Resolution": [
        [(marginX, marginY + (2 * y3rdSettings)), (marginX, marginY + (2 * y3rdSettings) + (y3rdSettings / 2))],
        [(640, 480), (1980, 1080), (1080, 720)]],
    "Crop": [
        [(marginX + x4thSettings, marginY + (2 * y3rdSettings)),
         (marginX + x4thSettings, marginY + (2 * y3rdSettings) + (y3rdSettings / 2))],
        [(0, 0)]],  # TODO
    "Format": [[(marginX + (2 * x4thSettings), marginY + (2 * y3rdSettings)),
                (marginX + (2 * x4thSettings), marginY + (2 * y3rdSettings) + (y3rdSettings / 2))],
               ["avi", "jpg", "png"]],  # TODO
    "fps": [[(marginX + (3 * x4thSettings), marginY + (2 * y3rdSettings)),
             (marginX + (3 * x4thSettings), marginY + (2 * y3rdSettings) + (y3rdSettings / 2))],
            [30, 24, 25, 15, 10, 5]]  # TODO
}

# active camera mode properties list
acmpl = [
    [0, 'none', (0, 0), [1, 1]],
    [1, 'none', (0, 0), [1, 1]],
    [0, 'side-by-side', (0, dY / 4), [2, 1]],
    [0, 'top-bottom', (dX / 4, 0), [1, 2]],
    [1, 'side-by-side', (0, dY / 4), [2, 1]],
    [1, 'top-bottom', (dX / 4, 0), [1, 2]],
]

# -------------------------------------------------------------------------------------------------------------------- #
# PYGAME MAIN MOSSECAM PROGRAM LOOP
# -------------------------------------------------------------------------------------------------------------------- #

re_init_camera_object()
update_camera_settings()

while True:
    listen_for_button_press()
    if currentDisplay == "viewFinder":
        draw_camera_video_stream()

        if video_recording:
            video_out.write(globalFrame)
        elif not video_recording:
            if vid_capture_user_init == True:
                video_out.release()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            cv2.destroyAllWindows()
            camera.close()
            sys.exit()
    pygame.display.update()
