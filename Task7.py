import sys
import getopt
import json
import pandas as pd
import pycountry
import pycountry_convert as pc
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import graphviz
from tqdm import tqdm
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

def task7(docUUID, userUUID, inputFile):
    print("Enter data into the GUI text fields...")
    guiInputData = ["","","",False] # Create an empty array to hold the data the user will input, he false notfies the enter button has not been pressed yet
    window = Tk() # Create a new window
    window.title("Input Data For Graph") # Give the window a title

    fileframe = Frame(master=window, borderwidth = 10, relief = FLAT) # Create a frame for the inputFile lable, entry and button.
    filelabel = Label(text="Input .json File:", master=fileframe) # Create the text label
    fileentry = Entry(master=fileframe, width = 45) # Create the text entry for the inputFile
    fileentry.bind('<KeyRelease>', lambda event:task7_entry_on_key(event, fileentry, docentry, enterButton)) # Runs function task7_entry_on_key every time a button is pressed in the fileentry text entry

    docframe = Frame(master=window, borderwidth = 10, relief = FLAT) # Create a frame for the docUUID lable, entry and button.
    doclabel = Label(text="Input Document UUID:", master=docframe) # Create the te label
    docentry = Entry(master=docframe, width = 45)# Create the text entry for the docUUID
    docentry.bind('<KeyRelease>', lambda event:task7_entry_on_key(event, fileentry, docentry, enterButton)) # Runs function task7_entry_on_key every time a button is pressed in the fileentry text entry

    userframe = Frame(master=window, borderwidth = 10, relief = FLAT) # Create a frame for the userUUID lable, entry and button.
    userlabel = Label(text="Input User UUID (Optional):", master=userframe) # Create the text label
    userentry = Entry(master=userframe, width = 45)# Create the text entry for the userUUID

    buttonFrame = Frame(master=window, borderwidth = 10, relief = FLAT) # Create a frame for the enterButton and cancelButton
    enterButton = Button(text="Enter", width = 20, state = "disabled", command = lambda: enterButtonFunc(window, guiInputData, fileentry, docentry, userentry)) # Creates a button that runs the enterButtonFunc function on press
    cancelButton = Button(text="Cancel", width = 20, command = lambda: cancelButtonFunc(window)) # Creates a button that runs the cancelButtonFunc function on press

    fileentry.insert("1", inputFile) # Inputs the data from the commandline args into the text enteries if the user inputed any [Mainly used for testing]
    docentry.insert("1", docUUID)
    userentry.insert("1", userUUID)

    if fileentry.get() != "" and docentry.get() != "": # If either fileentry or docentry are empty disable the enter button
        enterButton.state(['!disabled'])

    filelabel.pack(fill=X) # Display all entries and lables, filling them all from left to right
    fileentry.pack(fill=X)
    doclabel.pack(fill=X)
    docentry.pack(fill=X)
    userlabel.pack(fill=X)
    userentry.pack(fill=X)

    fileframe.pack(fill=X) # Display all frames, filling them all from left to right
    docframe.pack(fill=X)
    userframe.pack(fill=X)

    enterButton.pack(side = LEFT, fill=X, expand = True) # Display all frames, displaying the enter and cancel butons next to each them, filling them all from left to right
    cancelButton.pack(side = RIGHT, fill=X, expand = True)
    buttonFrame.pack(fill=BOTH)

    window.mainloop() # Display the window

    if guiInputData[3] == False: # If after the window closes the array still has the False then it means the enter button was not pushed
        print("Window Closed!")
        sys.exit(0)
    return guiInputData # If it is true then retuen all the data to the main .py file

def enterButtonFunc(window, guiInputData, fileentry, docentry, userentry): # When the enterButton is pressed load all the data into the array and set it to true, close the window
    guiInputData[0] = fileentry.get()
    guiInputData[1] = docentry.get()
    guiInputData[2] = userentry.get()
    guiInputData[3] = True
    window.destroy()

def cancelButtonFunc(window): # When the cancelButton is pressed, close the window leaving the array false
    window.destroy()

def task7_entry_on_key(event, fileentry, docentry, enterButton): # If after a key is pressed in either the docentry or fileentry is empty disable the enter button, if they both have characters then enable. Theis stops the user sending no data  
    if fileentry.get() == "" or docentry.get() == "":
        enterButton.state(['disabled'])
    else:
        enterButton.state(['!disabled'])
