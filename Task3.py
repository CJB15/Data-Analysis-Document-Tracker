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

def task3(docUUID, userUUID, taskID, pdData):
    if docUUID == "": # Checks if the docUUID has been inputed by the user, if not print error message and the end program
        print("Error: -d 'doc_uuid' required")
        sys.exit(0)

    tempBrowserDp = pdData.loc[(pdData["subject_doc_id"] == docUUID) & (pdData["event_type"] == "impression")] # Search through the data frame for rows that have the inputed docUUID as their document and are for an impression event
    BrowserResults = dict(tempBrowserDp.visitor_useragent.value_counts()) # Creates a dictionary from the searched data frame where the key is each string that appears in the "visitor_useragent" collum and the value is the number of times that browser/os/other combination appeared

    if taskID == "3a":
        task3a(docUUID, BrowserResults) #  If the user inputed task3a then run the task3a funvtion
    else:
        task3b(docUUID, BrowserResults) #  If the user inputed task3b then run the task3b funvtion

def task3a(docUUID, BrowserResults):
    print("Generating Browser Histogram for document "  + docUUID + "...")
    plt.bar(BrowserResults.keys(), BrowserResults.values(), 1, color="g") # Generate the histogram using bar function and the new dictionary, note: this graph is unsable and very buggy as it uses the very long browser + everything names
    plt.show()

def task3b(docUUID, BrowserResults):
    print("Generating Browser Histogram (W/ Shortened Names) for document "  + docUUID + "...")
    BRShortName = {}
    for browser, count in BrowserResults.items(): # Cycle through the dictionary to create a new one now with the shrtened browser names
        browsernamesplit = browser.split("/") # The names are split on the /
        browsername = browsernamesplit[0] # And the browser name from teh jest side of the first / is saved
        if browsername in BRShortName: # If this browser name is already in the list then just add to it's count
            BRShortName[browsername] = BRShortName[browsername] + count
        else: # If not then add the browser to the list
            BRShortName[browsername] = count
    plt.bar(BRShortName.keys(), BRShortName.values(), 1, color="g") # Generate the histogram using bar function and the new dictionary
    plt.show()
