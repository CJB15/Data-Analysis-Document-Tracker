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

def task2(docUUID, userUUID, taskID, pdData):
    if docUUID == "": # Checks if the docUUID has been inputed by the user, if not print error message and the end program
        print("Error: -d 'doc_uuid' required")
        sys,exit(2)

    tempCountryDp = pdData.loc[(pdData["subject_doc_id"] == docUUID) & (pdData["event_type"] == "impression")] # Search through the data frame for rows that have the inputed docUUID as their document and are for an impression event
    CountryResults = dict(tempCountryDp.visitor_country.value_counts()) # Creates a dictionary from the searched data frame where the key is each string that appears in the "visitor_country" collum and the value is the number of times that country appeared

    if taskID == "2a": #  If the user inputed task2a then run the task2a funvtion

        task2a(docUUID, CountryResults)

    elif taskID == "2b": #  If the user inputed task2b then run the task2b funvtion

        task2b(docUUID, CountryResults)

def task2a(docUUID, CountryResults):
    print("Generating Country Histogram for document " + docUUID + "...")
    CRFullName = {}
    for countrycode, count in CountryResults.items(): # Cycle through the dictionary to create a new one now with the full country names rather than the 2 letter codes used in the data
        countryname = pycountry.countries.get(alpha_2=countrycode).name
        CRFullName[countryname] = count
        #print(countryname + " - " + str(count))
    plt.bar(CRFullName.keys(), CRFullName.values(), 1, color="g") # Generate the histogram using bar function and the new dictionary
    plt.show()

def task2b(docUUID, CountryResults):
    conCount = [0, 0, 0, 0, 0, 0] # Create an array with an entry for each continent

    for countrycode, count in CountryResults.items(): # Cycle through the dictionary converting each country code to it's continent code.
        continentCode = pc.country_alpha2_to_continent_code(countrycode)
        if continentCode == "NA": # The counter each country had is then added to their respective continent
            conCount[0] = conCount[0] + count
        elif continentCode == "SA":
            conCount[1] = conCount[1] + count
        elif continentCode == "AS":
            conCount[2] = conCount[2] + count
        elif continentCode == "OC":
            conCount[3] = conCount[3] + count
        elif continentCode == "AF":
            conCount[4] = conCount[4] + count
        elif continentCode == "EU":
            conCount[5] = conCount[5] + count

    print("Generating Continent Histogram for document " + docUUID + "...")
    #print("North America - " + str(NAcount))
    #print("South America - " + str(SAcount))
    #print("Asia - " + str(AScount))
    #print("Africa - " + str(AFcount))
    #print("Europe - " + str(EUcount))
    plt.bar(["N. America", "S. America", "Asia", "Oceania", "Africa", "Europe"], conCount, 1, color="g") # Generate the histogram using bar function and the array with the new continent counts
    plt.show()
