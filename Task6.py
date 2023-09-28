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
    tempReaderList = DataFr.loc[(DataFr["subject_doc_id"] == docUUID) & (DataFr["event_type"] == "impression" ) & (DataFr["visitor_uuid"] != userUUID)]
    userList = tempReaderList['visitor_uuid'].unique()
    return userList

def getDocsRead(DataFr, userUUID, docUUID):
    tempReadDocList = DataFr.loc[(DataFr["visitor_uuid"] == userUUID) & (DataFr["event_type"] == "impression") & (DataFr["subject_doc_id"] != docUUID)]
    documentList = tempReadDocList['subject_doc_id'].unique()
    return documentList

def alsoLike(pdData, docUUID, userUUID, sorting):

    if docUUID == "":
        print("Error: -d 'doc_uuid' required")
        sys.exit(0)

    readerList = getReaders(pdData, docUUID, userUUID)

    docList = []
    pbar = tqdm(range(readerList.size))
    for i in readerList:
        tempDocs = getDocsRead(pdData, i, docUUID)
        docList = np.concatenate((docList, tempDocs), axis=None)
        pbar.update(1)
    pbar.close()

    uniqueDocList = np.unique(docList, return_counts=True)

    DocDict = {}
    for x, y in zip(uniqueDocList[0], uniqueDocList[1]):
        DocDict[x] = y
    if sorting == "descending":
        return dict(sorted(DocDict.items(), key=lambda x:x[1], reverse=True))
    elif sorting == "ascending":
        return dict(sorted(DocDict.items(), key=lambda x:x[1], reverse=False))
    elif sorting == "nosort":
        return DocDict

def task6(docUUID, userUUID, taskID, pdData):
    shownReaderCount = 0
    totalReaderCount = 0
    doclist = []

    if userUUID != "":
        print("Generating 'Also Like' Graph for document " + docUUID + ", with " + userUUID + " as the reader...")
    else:
        print("Generating 'Also Like' Graph for document " + docUUID + "...")

    if taskID == "7":
        dot = graphviz.Digraph("Also_Likes_Graph", format='png')
    else:
        dot = graphviz.Digraph("Also_Likes_Graph", format='pdf')

    dot.node(docUUID, label=docUUID[-4:], shape="circle", color="green", style="filled")

    if userUUID != "":
        dot.node(userUUID, label=userUUID[-4:], shape="square", color="green", style="filled")
        dot.edge(userUUID, docUUID)

    readerList = getReaders(pdData, docUUID, userUUID)
    totalReaderCount = readerList.size
    if totalReaderCount == 0:
        print("Cant generate 'Also Likes' graph, no other user viewed graph")
        sys.exit(0)
    pbar = tqdm(range(totalReaderCount))
    for i in readerList:
        docList = getDocsRead(pdData, i, docUUID)
        if docList.size > 0:
            shownReaderCount = shownReaderCount + 1
            dot.node(i, label=i[-4:], shape="square", color="black")
            dot.edge(i, docUUID)
            for j in docList:
                doclist.append(j)
                dot.node(j, label=j[-4:], shape="circle", color="#63C5FF", style="filled")
                dot.edge(i, j)
        pbar.update(1)
    pbar.close()

    docarray = np.array(doclist)
    docunique = np.unique(docarray, return_counts = True)
    docDict = {}
    for x, y in zip(docunique[0], docunique[1]):
        docDict[x] = y

    maxDocEntry = max(docDict, key=docDict.get)
    print(docDict[maxDocEntry])

    minDocEntry = min(docDict, key=docDict.get)
    print(docDict[minDocEntry])

    for x in docDict:
        if docDict[x] == docDict[maxDocEntry]:
            dot.node(x, label=x[-4:], shape="circle", color="#0492C2", style="filled")
        elif docDict[x] == docDict[minDocEntry]:
            dot.node(x, label=x[-4:], shape="circle", color="#63C5DA", style="filled")


    if taskID == "6":
        dot.render(view=True)
    else:
        dot.render(view=False)

        imagewindow = Tk()
        imagewindow.configure(background = "white")
        imagewindow.title("Also Likes Graph")
        imagewindow.resizable(False,False)

        graphimage = ImageTk.PhotoImage(Image.open("Also_Likes_Graph.gv.png"))
        imagelabel = Label(image=graphimage, background = "white")
        imagelabel.pack()

        textlabel1 = Label(text="This is the generated 'Also Likes' Graph.", background = "white")
        textlabel1.pack()
        textlabel2 = Label(text="It was generated for document '" + docUUID + "'.", background = "white")
        textlabel2.pack()
        if userUUID != "":
            textlabel3 = Label(text="With user '" + userUUID + "' as the reader.", background = "white")
            textlabel3.pack()
            textlabel4 = Label(text="There were " + str(totalReaderCount) + " user(s), not counting the reader, who viewed the document.", background = "white")
        else:
            textlabel4 = Label(text="There were " + str(totalReaderCount) + " user(s) who viewed the document.", background = "white")
        textlabel4.pack()
        if totalReaderCount != shownReaderCount:
            textlabel5 = Label(text="Of which only " + str(shownReaderCount) + " viewed other documents.", background = "white")
            textlabel5.pack()
        textlabel6 = Label(text="These user(s) viewed " + str(len(np.unique(docarray))) + " other documents.", background = "white")
        textlabel6.pack()

        buttonFrame = Frame()
        cancelButton = Button(text="Close", master=buttonFrame, command = lambda: cancelButtonFunc(imagewindow))
        cancelButton.pack(fill=X)
        buttonFrame.pack(fill=X)

        imagewindow.mainloop()

def task7(docUUID, userUUID, inputFile):
    print("Enter data into the GUI text fields...")
    guiInputData = ["","","",False]
    window = Tk()
    window.title("Input Data For Graph")

    fileframe = Frame(master=window, borderwidth = 10, relief = FLAT)
    filelabel = Label(text="Input .json File:", master=fileframe)
    fileentry = Entry(master=fileframe, width = 45)
    fileentry.bind('<KeyRelease>', lambda event:task7_entry_on_key(event, fileentry, docentry, enterButton))

    docframe = Frame(master=window, borderwidth = 10, relief = FLAT)
    doclabel = Label(text="Input Document UUID:", master=docframe)
    docentry = Entry(master=docframe, width = 45)
    docentry.bind('<KeyRelease>', lambda event:task7_entry_on_key(event, fileentry, docentry, enterButton))

    userframe = Frame(master=window, borderwidth = 10, relief = FLAT)
    userlabel = Label(text="Input User UUID (Optional):", master=userframe)
    userentry = Entry(master=userframe, width = 45)

    buttonFrame = Frame(master=window, borderwidth = 10, relief = FLAT)
    enterButton = Button(text="Enter", width = 20, state = "disabled", command = lambda: enterButtonFunc(window, guiInputData, fileentry, docentry, userentry))
    cancelButton = Button(text="Cancel", width = 20, command = lambda: cancelButtonFunc(window))

    fileentry.insert("1", inputFile)
    docentry.insert("1", docUUID)
    userentry.insert("1", userUUID)

    if fileentry.get() != "" and docentry.get() != "":
        enterButton.state(['!disabled'])

    filelabel.pack(fill=X)
    fileentry.pack(fill=X)
    doclabel.pack(fill=X)
    docentry.pack(fill=X)
    userlabel.pack(fill=X)
    userentry.pack(fill=X)

    fileframe.pack(fill=X)
    docframe.pack(fill=X)
    userframe.pack(fill=X)

    enterButton.pack(side = LEFT, fill=X, expand = True)
    cancelButton.pack(side = RIGHT, fill=X, expand = True)
    buttonFrame.pack(fill=BOTH)

    window.mainloop()

    if guiInputData[3] == False:
        print("Window Closed!")
        sys.exit(0)
    print(guiInputData)
    return guiInputData

def enterButtonFunc(window, guiInputData, fileentry, docentry, userentry):
    guiInputData[0] = fileentry.get()
    guiInputData[1] = docentry.get()
    guiInputData[2] = userentry.get()
    guiInputData[3] = True
    window.destroy()

def cancelButtonFunc(window):
    window.destroy()

def task7_entry_on_key(event, fileentry, docentry, enterButton):
    if fileentry.get() == "" or docentry.get() == "":
        enterButton.state(['disabled'])
    else:
        enterButton.state(['!disabled'])
