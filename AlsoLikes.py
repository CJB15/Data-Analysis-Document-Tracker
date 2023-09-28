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

def getReaders(DataFr, docUUID, userUUID):
    tempReaderList = DataFr.loc[(DataFr["subject_doc_id"] == docUUID) & (DataFr["event_type"] == "impression" ) & (DataFr["visitor_uuid"] != userUUID)]  # Search through the data frame for rows that have the inputted docUUID, are of the impression event type and do not have the userUUID the user inputed
    userList = tempReaderList['visitor_uuid'].unique() # Generate a list of each unique user that appears in the new data frame 'visitor_uuid' collum
    return userList

def getDocsRead(DataFr, userUUID, docUUID):
    tempReadDocList = DataFr.loc[(DataFr["visitor_uuid"] == userUUID) & (DataFr["event_type"] == "impression") & (DataFr["subject_doc_id"] != docUUID)] # Search through the data frame for rows that have the userUUID from the list, are of the impression event type and do not have the docUUID the user inputed
    documentList = tempReadDocList['subject_doc_id'].unique() # Generate a list of each unique document that appears in the new data frame 'subject_doc_id' collum
    return documentList

def alsoLike(pdData, docUUID, userUUID, sorting):

    if docUUID == "": # Checks if the docUUID has been inputed by the user, if not print error message and the end program
        print("Error: -d 'doc_uuid' required")
        sys.exit(0)

    readerList = getReaders(pdData, docUUID, userUUID) # Calls getReaders function to get a list of all users that read the document related to the inputed docUUID

    docList = [] # Create a nparray
    pbar = tqdm(range(readerList.size)) # Generate a tqdm progress bar, used to notify the user that the program is still running as this can be a long loop. The progress bar is out of the number of users int the list retuened from getReaders
    for i in readerList: # Cyclce though the list of users
        tempDocs = getDocsRead(pdData, i, docUUID) # Call the getDocsRead to return the list of docuemnts that the user in the current cycle also viewed
        docList = np.concatenate((docList, tempDocs), axis=None) # Concatinate this with the previously created nparray, so that it collects all docuemnts each user viwed
        pbar.update(1) # Advance the progress bar by 1
    pbar.close() # CLose the progess bar when the loop is finished

    uniqueDocList = np.unique(docList, return_counts=True) # Get each unique document from the nparray of all documents, along with the counter for each document

    DocDict = {} # Create a blank dictionary
    for x, y in zip(uniqueDocList[0], uniqueDocList[1]): # Cycle through the nparray and assign each document to the dictionary with it's count as it's value
        DocDict[x] = y
    if sorting == "descending": # If the sorting paramenter is descending then return the dictionary sorted by value descending
        return dict(sorted(DocDict.items(), key=lambda x:x[1], reverse=True))
    elif sorting == "ascending": # If the sorting paramenter is ascending then return the dictionary sorted by value ascending
        return dict(sorted(DocDict.items(), key=lambda x:x[1], reverse=False))
    elif sorting == "nosort": # If the sorting paramenter is nosort then return the dictionary unsorted
        return DocDict

def task5d(docUUID, userUUID, taskID, pdData):
    print("Generating list of 'Also Liked' documents...")
    alsoLikedDocs = alsoLike(pdData, docUUID, userUUID, "descending") # Call the alsoLike function, save the retuened dictionary
    count = 0 # Create a counter
    print("----------------------------------")
    if userUUID != "": # If the user inputed a userUUID as the reader notify that theyre also read documents are not conted in the list
        print("Current reader is user '" + userUUID + "'.")
        print("As such their also liked documents are not counted.")
    print("People who viewed document '" + docUUID + "' also liked:")
    for i in alsoLikedDocs: # Cycle through the list printing each document and how many other users viewed it.
        if alsoLikedDocs[i] == 1 : # Only using the plural for user is more than 1 person viewed it
            print("- '" + i + "', viewed by " + str(alsoLikedDocs[i]) + " other user.")
        else:
            print("- '" + i + "', viewed by " + str(alsoLikedDocs[i]) + " other users.")
        count = count + 1 # incrament the counter each time
        if count == 10: # Once 10 documents have been printed stop printing
            break
    print("----------------------------------")

def task6(docUUID, userUUID, taskID, pdData):
    shownReaderCount = 0 # A counter for all the users that read the specified document and another document, therefor having a node genreated in the graph
    totalReaderCount = 0 # A counter for all the users that read the specified document
    usersAlsoRead = [] # A list to hold each document that the users also read

    if userUUID != "": # If the user entered a userUUID, specify that they're the reader
        print("Generating 'Also Like' Graph for document " + docUUID + ", with " + userUUID + " as the reader...")
    else: # If not then don't mention the reader
        print("Generating 'Also Like' Graph for document " + docUUID + "...")

    if taskID == "7": # If the taskID is 7 then genreate a png so it can be loaded into the GUI screen, otehrwise generate a pdf
        dot = graphviz.Digraph("Also_Likes_Graph", format='png')
    else:
        dot = graphviz.Digraph("Also_Likes_Graph", format='pdf')

    dot.node(docUUID, label=docUUID[-4:], shape="circle", color="green", style="filled") # Generate a node for the specified document, higlighting it as green

    if userUUID != "": # If the user entered a userUUID, generate a node for it and highlight it as green
        dot.node(userUUID, label=userUUID[-4:], shape="square", color="green", style="filled")
        dot.edge(userUUID, docUUID) # Connect it to the previous document node

    readerList = getReaders(pdData, docUUID, userUUID) # Calls getReaders function to get a list of all users that read the document related to the inputed docUUID
    totalReaderCount = readerList.size # Gets the size of the list of users that read the document, giving the number of users who read the specifed document
    if totalReaderCount == 0: # If no user who viewed the document also viewed another document then display an error as there isn't a graph to generate, end the program
        print("Cant generate 'Also Likes' graph, no other user viewed graph")
        sys.exit(0)
    pbar = tqdm(range(totalReaderCount)) # Generate a tqdm progress bar, used to notify the user that the program is still running as this can be a long loop. The progress bar is out of the number of users int the list retuened from getReaders
    for i in readerList: # Loop through the list of readers
        docList = getDocsRead(pdData, i, docUUID) # Call the getDocsRead to return the list of docuemnts that the user in the current cycle also viewed
        if docList.size > 0: # If the user dodn't read any documents other than the specified, don't add them to the graph
            shownReaderCount = shownReaderCount + 1 # If they did, increment the counter for useres who did and generate a node for them, connecting it to the specified document
            dot.node(i, label=i[-4:], shape="square", color="black")
            dot.edge(i, docUUID)
            for j in docList: # For each document that the user viewed
                usersAlsoRead.append(j) # Add to the list of all documents users also read
                dot.node(j, label=j[-4:], shape="circle", color="#63C5FF", style="filled") # Genreate a node for this document
                dot.edge(i, j) # And connect it to the user who viewed it
        pbar.update(1) # Advance the progress bar by one after each user is completed
    pbar.close() # When the loop is finished close the progess bar

    docarray = np.array(usersAlsoRead) # Convert the list to an nparray
    docunique = np.unique(docarray, return_counts = True) # And get each unique document viewed along with how many users also viewed it
    docDict = {} # Create a blank dictionary
    for x, y in zip(docunique[0], docunique[1]): # Cycle through the nparray and assign each document to the dictionary with it's count as it's value
        docDict[x] = y

    maxDocEntry = max(docDict, key=docDict.get) # Get the key with the highest value

    minDocEntry = min(docDict, key=docDict.get) # Get the key with the lowest value

    for x in docDict: # Cycle through each document in the dictionary
        if docDict[x] == docDict[maxDocEntry]: # If it has the same number of ussers who viewed as the highest viewed document it then change it's colour to a darker shade of blue
            dot.node(x, label=x[-4:], shape="circle", color="#0492C2", style="filled")
        elif docDict[x] == docDict[minDocEntry]: # If it has the same number of ussers who viewed as the lowest viewed document it then change it's colour to a lighter shade of blue
            dot.node(x, label=x[-4:], shape="circle", color="#63C5DA", style="filled")


    if taskID == "6": # If taskID 6 then display the pdf of the graph
        dot.render(view=True)
    else: # If taskID 7 then genereate the graph image but don't display it
        dot.render(view=False)

        imagewindow = Tk() # Create a GUI window called imagewindow
        imagewindow.configure(background = "white") # Set backround colour
        imagewindow.title("Also Likes Graph") # Set page title
        imagewindow.resizable(False,False) # Set page to be not resizable

        graphimage = ImageTk.PhotoImage(Image.open("Also_Likes_Graph.gv.png")) # Load the generated graph png as an image
        imagelabel = Label(image=graphimage, background = "white") # Create a label with the image
        imagelabel.pack() # Display the label

        textlabel1 = Label(text="This is the generated 'Also Likes' Graph.", background = "white") # Create a label with some text
        textlabel1.pack() # Display the label
        textlabel2 = Label(text="It was generated for document '" + docUUID + "'.", background = "white") # Create a label with some text
        textlabel2.pack() # Display the label
        if userUUID != "": # If the user specifed a userUUID to be the reader
            textlabel3 = Label(text="With user '" + userUUID + "' as the reader.", background = "white") # Create a label with some text
            textlabel3.pack() # Display the label
            textlabel4 = Label(text="There were " + str(totalReaderCount) + " user(s), not counting the reader, who viewed the document.", background = "white") # Create a label with some text
        else: # If no user reader was specifed
            textlabel4 = Label(text="There were " + str(totalReaderCount) + " user(s) who viewed the document.", background = "white") # Create a label with some text
        textlabel4.pack() # Display the label
        if totalReaderCount != shownReaderCount: # If there were users who viewed the specifed document who didn't view other documents
            textlabel5 = Label(text="Of which only " + str(shownReaderCount) + " viewed other documents.", background = "white") # Create a label with some text
            textlabel5.pack() # Display the label
        textlabel6 = Label(text="These user(s) viewed " + str(len(np.unique(docarray))) + " other documents.", background = "white") # Create a label with some text
        textlabel6.pack() # Display the label

        buttonFrame = Frame() # Create a frame
        cancelButton = Button(text="Close", master=buttonFrame, command = lambda: cancelButtonFunc(imagewindow)) # Create a button in the frame, running the cancelButtonFunc function on press
        cancelButton.pack(fill=X) # Display the button, filling the screen from left to right
        buttonFrame.pack(fill=X) # Display the frame, filling the screen from left to right

        imagewindow.mainloop() # Run the window and display it

def cancelButtonFunc(window): # Closes the window
    print("Window Closed!")
    window.destroy()
