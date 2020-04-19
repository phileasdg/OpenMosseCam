# Global variables
infoOverlay = True
currentDisplay = "viewFinder"

# current setting index
csi = 0  # defaults to ISO

# Function definitions
def take_picture():
    print("taking picture")
def toggle_info():
    global infoOverlay
    infoOverlay = not infoOverlay
    print("infoOverlay is " + str(infoOverlay))
def settingsMenu():
    global currentDisplay
    currentDisplay = "settingsMenu"

    print("you have pressed 'settings menu'")
    # change values of the thing (maybe a single function could work)
def gallery():
    global currentDisplay
    currentDisplay = "gallery"

    print("you have pressed 'gallery'")
    # change values of the thing (maybe a single function could work)
def back():
    global currentDisplay
    currentDisplay = "viewFinder"

    # change the value of the buttons
def next_up():
    if currentDisplay == "settingsMenu":
        # adds one to setting index value if value is in range 0 to list length
        if 0 <= scvil[csi] < len(sd[sl[csi]])-1:  # note the "-1", it is important.
            scvil[csi] += 1
        # sets setting index value to 0
        else:
            scvil[csi] = 0

        print("you have pressed 'up'")
        print(sl[csi]+" = "+str(sd[sl[csi]][scvil[csi]]))
        # add 1 to setting value
    else:  # can only be called from the gallery
        print("next picture up")
def next_down():
    if currentDisplay == "settingsMenu":
        if 0 < scvil[csi] <= (len(sd[sl[csi]])):
            scvil[csi] -= 1
        else:
            scvil[csi] = len(sd[sl[csi]])-1

        print("you have pressed 'down'")
        print(sl[csi] + " = " + str(sd[sl[csi]][scvil[csi]]))
    else: # can only be called from the gallery
        print("next picture down")
def change_setting():
    global csi
    if 0 <= csi <8:  # between 0 and highest index in settingsList (8 for now)
        csi += 1
    else:
        csi = 0
    print("you have pressed 'change selected setting' \n the new setting is " + sl[csi])
    # go down to change the setting
def delete():
    print("content deleted")

# Dictionaries and lists (camera settings and UI)
displayFunctions = {
    "viewFinder": {
        "Button1": take_picture,  # the name of the function without the brackets
        "Button2": toggle_info,
        "Button3": settingsMenu,
        "Button4": gallery
    },
    "settingsMenu": {
        "Button1": back,
        "Button2": next_up,
        "Button3": next_down,
        "Button4": change_setting
    },
    "gallery": {
        "Button1": back,
        "Button2": next_up,
        "Button3": next_down,
        "Button4": delete
    }
}  # contains map of functions and their button assignment for different displays
displayDescriptions = {
    "viewFinder": {
        "Button1": "1: take_picture",  # the name of the function without the brackets
        "Button2": "2: toggle_info",
        "Button3": "3: settingsMenu",
        "Button4": "4: gallery"
    },
    "settingsMenu": {
        "Button1": "1: back",
        "Button2": "2: next_up",
        "Button3": "3: next_down",
        "Button4": "4: change_setting"
    },
    "gallery": {
        "Button1": "1: back",
        "Button2": "2: next_up",
        "Button3": "3: next_down",
        "Button4": "4: delete"
    }
}  # primarily for dev purposes: reference dict of the descriptions of btn functions to print

# settings list
sl = ["ISO", "Shutter", "Mode", "Effect", "Format", "Resolution", "AWB", "Red gain", "Blue gain"]
# settings dictionary
sd = {
    "ISO": [100, 200, 300],  # limited number of values
    "Shutter": [(1, 100), (2, 200), (3,300)],  # values seen by user and values read by program are different
    "Mode": ["photo", "video"], # only two modes, could be tied to a boolean
    "Effect": ["none", "negative"],  # limited number of values
    "Format": ["jpg", "png"],  # limited number of values
    "Resolution": [(1980, 1080), (1080, 720)],  # limited number of tuples, different
    "AWB": ["auto", "greyworld", "off"],
    "Red gain:": 0,
    "Blue gain:": 0
}
# settings current value index list
scvil = [
    0,  # ISO index from list of integers
    0,  # Shutter index from list of tuples: [("human value", computer value), ...]
    0,  # Mode index from list of strings (only two)
    0,  # Effect index from list of strings
    0,  # Format index from list of strings
    0,  # Resolution index from list of tuples [(x, y),(x, y), ...]
    0,  # AWB index from list of strings
    0,  # Red gain value = value between 1 and 9
    0   # Blue gain value = value between 1 and 9
]

while True:

    # button function descriptions print
    for i in range(4):
        print(displayDescriptions[currentDisplay]["Button" + str(i + 1)])

    # take user input and run function accordingly
    print("please enter a number:")
    displayFunctions[currentDisplay]["Button" + input()]()
