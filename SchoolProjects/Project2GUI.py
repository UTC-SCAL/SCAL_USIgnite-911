import tkinter
from tkinter import *


def clicked():
    lbl.configure(text="Button was clicked !! Time to die!")


def clicked_text():
    res = "Welcome to " + txt.get()
    lbl.configure(text=res)


window = Tk()

# Widgets #:
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://likegeeks.com/python-gui-examples-tkinter-tutorial/
    # Button: displays a button
    # Canvas: used to draw shapes
    # Checkbutton: display a number of options as check boxes (can select multiple options)
    # Entry: display a single-line text field for accepting user values
    # Frame: a container widget to organize other widgets
    # Label: provides a single-line caption for other widgets (can also contain an image)
    # Listbox: provides a list of options to user
    # Menubutton: used to display menus in your app
    # Menu: provide various commands to user (commands are contained inside Menubutton)
    # Message: display multiline text fields for accepting values from a user
    # Radiobutton: used to display a number of options as radio buttons (select 1 at a time)
    # Scale: provides slider widgets
    # Scrollbar: adds scrolling capability to various widgest (like list boxes)
    # Text: display text in multiple lines
    # Toplevel: used to provide a separate window container
    # Spinbox: can be used to select from a fixed number of values
    # PanedWindow: may contain any number of panes, arranged horizontally or vertically
    # LabelFrame: simple container widget; acts as a spacer or container for complex window layouts
    # tkMessageBox: displays message boxes in app

# Set window size
window.geometry("450x300")
window.title("Sample GUI Window")

# Adding a label and setting font size
lbl = Label(window, text="What it do?", font=("Arial Bold", 35))
# Set label position
lbl.grid(column=0, row=0)

# Adding a button
# Change button foreground (fg) and background (bg) colors
# Handle button click event by calling the clicked() method made above
btn = Button(window, text="Don't Click Me", bg="orange", fg="red", command=clicked)  # Note the absence of ()
btn.grid(column=1, row=0)  # Set the column to something other than column 0, since something else is already there

# Get input using Entry class (Tkinter textbox)
# To add button functionality, use the command= param
txt = Entry(window, width=10)  # Create the textbox
txt.grid(column=0, row=1)
btn2 = Button(window, text="Click Me", bg="green", fg="black", command=clicked_text)
btn2.grid(column=1, row=1)

# Add a combobox widget


window.mainloop()  # this calls the endless loop of the window, so it waits for user interaction before closing
