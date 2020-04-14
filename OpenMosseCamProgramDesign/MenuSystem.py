infoOverlay = True
currentDisplay = "viewFinder"

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
    print("you have pressed 'up'")
    # add 1 to setting value


def next_down():
    print("you have pressed 'down'")
    # remove 1 from setting value


def change_setting():
    print("you have pressed 'change selected setting'")
    # go down to change the setting


def delete():
    print("content deleted")


Displays = {
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
}
DisplayFunctions = {
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
}

while True:
    for i in range(4):
        print(DisplayFunctions[currentDisplay]["Button"+str(i+1)])

    print("please enter a number:")
    Displays[currentDisplay]["Button"+input()]()
