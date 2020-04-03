from guizero import App, Text, TextBox, PushButton
# app background functions and code starts here

# app background functions and code end here

MosseApp = App(title="MosseAppTest", width=640, height=480, layout="grid")
# GUI content code starts here

welcome_message = Text(MosseApp, text="Welcome to MosseCam")
# welcome_message = Text(MosseApp, text="Welcome to MosseCam", size=40, font="Times New Roman", color="lightblue")
#you can use hexcodes such as #ff0000 to se colours

# GUI content code ends here
MosseApp.display().set_full_screen()
