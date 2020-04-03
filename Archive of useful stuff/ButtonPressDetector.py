#this program should be able to tell
# 1) if a button is pressed or not
# 2) how long a button is pressed for
# 3) if the button was double pressed or single pressed

from gpiozero import Button

def say_hello():
    print ("hello")

Button = Button(23)  # type: Button

while True:
    Button.when_activated = say_hello
