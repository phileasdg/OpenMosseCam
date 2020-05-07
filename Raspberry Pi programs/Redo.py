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

# TODO: redo the menu structure and settings lookup system
# Todo: redo the camera setup and tie it to OpenCV and the GUI
# Todo: make it so the program only commits the setting changes when the user returns to the viewfinder

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# PROGRAM GLOBAL VARIABLE DECLARATIONS
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

infoOverlay = True
currentDisplay = "viewFinder"
# current setting index
csi = 0  # defaults to ISO

# Camera program GUI assets
setting_header_dir = r"/home/pi/Desktop/OpenMosseCam/Raspberry Pi programs/app_icons/setting_cell_icons_no_transparency"

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# CAMERA SETUP (PICAMERA)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

# TODO: def setup_camera():s

c_num = 0
s_mode = 'side-by-side'

camera = picamera.PiCamera(camera_num=c_num, stereo_mode=s_mode, stereo_decimate=False, led_pin=3)
# camera_num options = [0, 1]
# stereo mode options = ['none', 'side-by-side', top-bottom]

# Important: Camera resolution height must be dividable by 16, and width by 32
camera.resolution = (640*2, 480)
# camera.resolution = (640, 480)
print ("Camera resolution: "+str(camera.resolution))

# Video stream
video = picamera.array.PiRGBArray(camera)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# GPIO SETUP
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

buttons = {1: 17, 2: 22, 3: 23, 4: 27}
GPIO.setmode(GPIO.BCM)
for v in buttons.values():
    GPIO.setup(v, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# FUNCTIONS DECLARATIONS
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

# Button functions declarations
def capture():
    # run function
    # update gui display

    # update cli display
    update_cli_display("Recording " + sd["Mode"][1][scvil[csi]])


def toggle_info():
    # run function
    global infoOverlay
    infoOverlay = not infoOverlay

    # update gui display

    # update cli display
    update_cli_display("infoOverlay is " + str(infoOverlay))


def settings_menu():
    # run function
    global currentDisplay
    currentDisplay = "settingsMenu"
    # update gui display
    DISPLAYSURF.fill(BLACK)

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

    # update cli display
    update_cli_display("You have pressed settings menu")

# TODO: blit images and videos from saved images and videos folder
def gallery():
    # run function
    global currentDisplay
    currentDisplay = "gallery"

    # update gui display
    DISPLAYSURF.fill(BLACK)
    # draw settings box
    pygame.draw.rect(DISPLAYSURF, WHITE, (marginX, marginY, GUIx, GUIy), 1)  # settings rect

    # blit images and video here

    draw_base_ui_overlay()

    # update cli display
    update_cli_display("you have pressed gallery")


def return_to_viewfinder():
    # run function
    global currentDisplay
    currentDisplay = "viewFinder"

    # update cli display
    update_cli_display("you have pressed viewFinder")

# TODO: implement next_up and next down into the gallery
# TODO: implement resolutions for video and photo modes in the next up and next down functions
def next_up():
    # run function and update GUI display
    if currentDisplay == "settingsMenu":
        if 0 <= scvil[csi] < len(sd[sl[csi]][1]) - 1:  # note the "-1", it is important.
            # current setting value from index in list of values in dictionary += 1
            scvil[csi] += 1
        # sets setting index value to 0
        else:
            scvil[csi] = 0
        settings_menu()
        print(sl[csi] + " = " + str(sd[sl[csi]][1][scvil[csi]]))

        # re-init camera if there is a user request to do so
        if csi == 1:
            re_init_camera_object()

    elif currentDisplay == "gallery":
        pass

    # update cli display
    update_cli_display("you have pressed next up")


def next_down():
    # run function and update GUI display
    if currentDisplay == "settingsMenu":
        if 0 < scvil[csi] <= len(sd[sl[csi]][1]):
            # current setting value from index in list of values in dictionary -= 1
            scvil[csi] -= 1
        # sets setting index value to the highest index in the list
        else:
            scvil[csi] = len(sd[sl[csi]][1]) - 1
        settings_menu()
        print(sl[csi] + " = " + str(sd[sl[csi]][1][scvil[csi]]))

        # re-init camera if there is a user request to do so
        if csi == 1:
            re_init_camera_object()

    elif currentDisplay == "gallery":
        pass

    # update cli display
    update_cli_display("you have pressed next down")

def change_setting():
    # run function
    global csi
    if 0 <= csi < (len(sl)-1):  # between 0 and highest index in sl (settings list)
        csi += 1
    else:
        csi = 0
    print("you have pressed 'change selected setting' \nthe new setting is " + sl[csi])

    # update gui display
    settings_menu()

    # update cli display
    update_cli_display("you have pressed change setting")


def delete():
    # run function
    # update gui display

    # update cli display
    update_cli_display("you have pressed delete")


# Pygame loop functions declarations
def listen_for_button_press():
    for k, v in buttons.items():
        if GPIO.input(v) == False:  # for any GPIO input equal to a value from the button dictionary
            print("button " + str(k) + " pressed")  # print the action taken to the terminal
            displayFunctions[currentDisplay]["Button" + str(k)][0]()  # run function associated with button
            update_cli_display()
            sleep(0.3)


def update_cli_display(text_to_print=None):
    if text_to_print == None:
        for i in range(4):
            print(displayFunctions[currentDisplay]["Button" + str(i + 1)][1])
        print("please press a button:")
    else:
        print(text_to_print)


def draw_base_ui_overlay():
    pygame.draw.rect(DISPLAYSURF, WHITE, (2 * marginX + GUIx, marginY, 3 * marginX, GUIy + 4 * marginY), 1)  # buttons rect
    pygame.draw.rect(DISPLAYSURF, WHITE, (marginX, 2 * marginY + GUIy, GUIx, 3 * marginY), 1)  # bottom rect description rext
    for i in range(3):
        pygame.draw.line(DISPLAYSURF, WHITE, (2 * marginX + GUIx, int(marginY + (i + 1) * y4thButtons)), (5 * marginX + GUIx, int(marginY + (i + 1) * y4thButtons)), 1)  # y4ths


def draw_camera_video_stream():
    global frameblitX, frameblitY, resX, resY
    for frameBuf in camera.capture_continuous(video, format="rgb", use_video_port=True):

        frame = np.rot90(frameBuf.array)
        frame = cv2.resize(frame, (int(resY), int(resX)))

        video.truncate(0)
        frame = pygame.surfarray.make_surface(frame)
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(frame, (frameblitX, frameblitY))

        if infoOverlay == True:
            draw_base_ui_overlay()
        pygame.display.update()
        break

# this function should only be run when a the user requests a change to settings which must be declared during picam init
def re_init_camera_object():
    global resX, resY, s_mode, c_num, frameblitX, frameblitY, camera, video

    # update the video frame blit coordinates
    frameblitX, frameblitY = acmpl[scvil[1]][2]

    # update the picamera object camera number and stereo mode
    c_num = acmpl[scvil[1]][0]
    s_mode = acmpl[scvil[1]][1]
    camera.close()
    camera = picamera.PiCamera(camera_num=c_num, stereo_mode=s_mode, stereo_decimate=False, led_pin=3)

    # define and apply resolutions to fit active camera settings
    camResX, camResY = sd["Resolution"][1][scvil[sl.index("Resolution")]]
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

    # update cli
    update_cli_display(("res ", resX, resY))
    update_cli_display(("frameblit ", frameblitX, frameblitY))


# TODO: make and integrate the following functions:
def read_and_show_image():
    pass


def read_and_show_video():
    pass

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# PYGAME GUI SETUP
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

# Display settings
pygame.display.init()
info = pygame.display.Info()
dX, dY = info.current_w, info.current_h  # display resolution
# dX, dY = 640, 480 # use if you want to set the display res to custom values

marginX = int(dX / 32)
marginY = int(dY / 32)

# GUI boundaries declarations
GUIx, GUIy = int(dX - 6 * marginX), int(dY - 6 * marginY)  # GUI display size (dX or dY - at least 2* margin of X or Y)
# GUI top left = marginX, marginY

# UI BUILDING BLOCKS:
# Settings block (the settings rectangle):
x4thSettings = (GUIx / 4)
y3rdSettings = (GUIy / 3)
# Buttons Block:
y4thButtons = ((GUIy + 4 * marginY) / 4)

# reference resized video feed resolution values
resX, resY = (640, 240) # TODO: update to be an actual test resolution

# video stream frame blit coordinates
frameblitX = 0
frameblitY = dY/4

# Start Pygame
pygame.init()
pygame.display.set_caption("OpenMosseCam-Stereo")
DISPLAYSURF = pygame.display.set_mode((dX, dY))  # , pygame.FULLSCREEN)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# MENU STRUCTURE AND SETTINGS SETUP
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

# dictionary structure - displayFunctions = { currentDisplay: { Button: [function to run, function description] } }
displayFunctions = {
    "viewFinder": {
        "Button1": [capture, "1: run capture()"],  # [name the function without brackets, cli description]
        "Button2": [toggle_info, "2: run toggle_info()"],
        "Button3": [settings_menu, "3: run settings_menu()"],
        "Button4": [gallery, "4: run gallery()"]
    },
    "settingsMenu": {
        "Button1": [return_to_viewfinder, "1: run return_to_viewfinder()"],
        "Button2": [next_up, "2: run next_up()"],
        "Button3": [next_down, "3: run next_down()"],
        "Button4": [change_setting, "4: run change_setting()"]
    },
    "gallery": {
        "Button1": [return_to_viewfinder, "1: run return_to_viewfinder()"],
        "Button2": [next_up, "2: run next_up()"],
        "Button3": [next_down, "3: run next_down()"],
        "Button4": [delete, "4: run delete()"]
    }
}  # contains map of functions and their button assignment for different displays

# settings list
sl = ["Mode", "Active Camera(s)", "Shutter", "ISO", "AWB", "Red gain", "Blue gain", "Effect", "Resolution", "Crop",
      "Format", "fps"]

# settings dictionary - key: [[GUI coordinates of setting headers, coordinates of setting values][setting values list]]
# there are two resolution keys, one for photo mode and one for video mode
sd = {
    # TODO: reformat and clean up when finished
    # TODO: implement the two resolution modes in the program
    "Mode": [[(marginX, marginY), (marginX, marginY + (y3rdSettings / 2))], ["Photo", "Video"]],
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
    "Red gain": [[(marginX + x4thSettings, marginY + y3rdSettings), (marginX + x4thSettings,
                                                                     marginY + y3rdSettings + (y3rdSettings / 2))],
                 [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9,
                  2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9,
                  4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9,
                  6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9,
                  8.0]],
    "Blue gain": [[(marginX + (2 * x4thSettings), marginY + y3rdSettings), (marginX + (2 * x4thSettings),
                                                                            marginY + y3rdSettings + (
                                                                                        y3rdSettings / 2))],
                  [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9,
                   2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9,
                   4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9,
                   6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9,
                   8.0]],
    "Effect": [[(marginX + (3 * x4thSettings), marginY + y3rdSettings), (marginX + (3 * x4thSettings),
                                                                         marginY + y3rdSettings + (y3rdSettings / 2))],
               ["none", "negative", "solarize", "hatch", "gpen", "film", "colorswap", "washedout", "colorbalance",
                "cartoon"]],
    # effects availablee: 'none', 'negative', 'solarize', 'sketch', 'denoise', 'emboss', 'oilpaint', 'hatch', 'gpen',
    # 'pastel', 'watercolor', 'film', 'blur', 'saturation', 'colorswap', 'washedout', 'posterise', 'colorpoint',
    # 'colorbalance', 'cartoon', 'deinterlace1', 'deinterlace2'
    "Resolution": [
        [(marginX, marginY + (2 * y3rdSettings)), (marginX, marginY + (2 * y3rdSettings) + (y3rdSettings / 2))],
        [(640, 480), (1980, 1080), (1080, 720)]],  # limited number of tuples, different
    "Crop": [
        [(marginX + x4thSettings, marginY + (2 * y3rdSettings)), (marginX + x4thSettings, marginY + (2 * y3rdSettings) +
                                                                  (y3rdSettings / 2))],
        [(0, 0)]],  # TODO
    "Format": [[(marginX + (2 * x4thSettings), marginY + (2 * y3rdSettings)), (marginX + (2 * x4thSettings),
                                                                               marginY + (2 * y3rdSettings) + (
                                                                                           y3rdSettings / 2))],
               ["jpg", "png"]],
    "fps": [[(marginX + (3 * x4thSettings), marginY + (2 * y3rdSettings)), (marginX + (3 * x4thSettings),
                                                                            marginY + (2 * y3rdSettings) + (
                                                                                        y3rdSettings / 2))],
            [30]]  # TODO

}

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

# active camera mode properties list
acmpl = [
    [0, 'none', (0, 0), [1, 1]],
    [1, 'none', (0, 0), [1, 1]],
    [0, 'side-by-side', (0, dY/4), [2, 1]],
    [0, 'top-bottom', (dX/4, 0), [1, 2]],
    [1, 'side-by-side', (0, dY / 4), [2, 1]],
    [1, 'top-bottom', (dX / 4, 0), [1, 2]],
]

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# PYGAME MAIN MOSSECAM PROGRAM LOOP
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

update_cli_display()

while True:
    listen_for_button_press()
    if currentDisplay == "viewFinder":
        draw_camera_video_stream()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            cv2.destroyAllWindows()
            camera.close()
            sys.exit()
    pygame.display.update()
