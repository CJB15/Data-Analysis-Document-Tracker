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

def task4(docUUID, userUUID, taskID, pdData):
    print("Generating Top 10 Readers List...")

    tempReadingTimeList = pdData.loc[(pdData["event_type"] == "pagereadtime")] # Search through the data frame for rows that are for a pagereadtime event

    userlist = tempReadingTimeList['visitor_uuid'].unique() # Get a list of each user that generated a pagereadtime event
    userdict = {} # And an empty dictionary

    for i in userlist: # Cycle through the list and load each list entry into the dictionary with a value of 0
        userdict[i] = 0
    pbar = tqdm(range(len(tempReadingTimeList.index))) # Generate a tqdm progress bar, used to notify the user that the program is still running as this can be a long loop. The progress bar is out of the number of entries that are pagereadtime events
    for i, row in tempReadingTimeList.iterrows(): # Cycle through the data sheet of all pagereadtime events
        userdict[row["visitor_uuid"]] = userdict[row["visitor_uuid"]] + row["event_readtime"] # Add the read time from each row to their respecive users count in the dictionary
        pbar.update(1) # Each time a row is processed advance the progress bar by 1
    pbar.close() # Once the loop is done close the progrssbar

    sorteduserdict = dict(sorted(userdict.items(), key=lambda x:x[1], reverse=True)) # Sort the dictionary by value, highest value first, and create a new dictionary form it,
    userindex = 1
    print("----------------------------------")
    print("No. | User UUID        | Read Time (Ms)")
    for i in sorteduserdict: # Print the first 10 entries in the new dictionary, this will as such print the users with the 10 highest read times.
        if userindex == 10:
            print(str(userindex) + "  | " + i + " | " + str(sorteduserdict[i])) # Print the 10th entry with 1 less space in the left collum to acount for it being the 10 entry and the no 10 in the No. collum taking up more space
            break
        print(str(userindex) + "   | " + i + " | " + str(sorteduserdict[i])) # Print each entry like this to create a table in the command line
        userindex = userindex + 1
    print("----------------------------------")
