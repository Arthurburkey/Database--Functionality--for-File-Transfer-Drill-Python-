##PyDrill Database Functionality for File Transfer 3.4
##Title: Database functionality for File Transfer - Python 3.4 – IDLE
##Scenario: You recently created a script that will check a folder for new or modified files, and then
##copy those new or modified files to another location. You also created a UI that makes using the script
##easier and more versatile.

##Users are reporting issues with the current system you've made. Specifically, they are having to manually
##initiate the 'file check' script at the same time each day. Because they aren't doing this at the EXACT
##same time each day, some files that were edited right around the time the script was meant to be run were
##missed, and weren't copied to the outgoing files destination.
##This means you will have to provide for recording the last time the 'file check' process was performed,
##so that you can be sure to cover the entire time period in which new or edited files could occur.

##To do this, you will need to create a database with a table that can store the date and time of the last 'file
##check' process. That way, you can use that date/time as a reference point in terms of finding new or
##modified files.

##As part of this project, the users are asking that their UI display the date and time of the last 'file check'
##process.

##You have been asked to implement this functionality. This means that you will need to
##• create a database and a table
##• modify your script to both record date/time of 'file check' runs and to retrieve that data for use in
##the 'file check' process, and
##• modify the UI to display the last 'file check' date/time

##Guidelines:
##Use Python 3.4 for this drill.
##Use sqlite for your database functionality.
##Use tkinter module for the UI.
##The layout of the UI is up to you.
##You should use IDLE or any text editor that you are comfortable with for the Drill.

from tkinter.filedialog import askdirectory 
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import shutil
import time
import datetime as dt
import sqlite3
conn = sqlite3.connect('DataModification.db')


timestamp = (time.time())
vorTimestamp = timestamp - 86400
print("nowTime",timestamp)

class MyGui:
    def __init__(self, master):
        
        self.master = master
        master.title("File Transfer")

        
        #display of previous file-check event
        self.srcLabel = StringVar()
        self.destLabel = StringVar()
        self.printToLabel = StringVar()
        self.printToLabel.set(PrintTimestampGUI)
##        self.printToLabelTime = Label(master, textvariable = self.printToLabel).pack
##        self.label.pack()

        #create a button that calls the sourceFolder function below
        self.sourceButton = Button(master, text="Browse Source", command = self.Source)
        self.sourceButton.pack()

        #create a button that calls the destination function below
        self.destinationButton = Button(master, text="Browse Destination", command = self.Destination)
        self.destinationButton.pack()
        
        #create a button that calls the copy/move function below
        self.moveButton = Button(master, text="Move to Destination", command=self.checkFile)
        self.moveButton.pack()

    
    def Destination(self):
        destX = askdirectory()
        self.destLabel.set(destX)

    def Source(self):
        srcX = askdirectory()
        self.srcLabel.set(srcX)

    def checkFile(self):
        
        destY = self.destLabel.get() + '/'
        srcY = self.srcLabel.get() + '/'
        prntSrc = os.listdir(srcY)
        for x in prntSrc:
            filetime = os.path.getmtime(srcY + x)
            if filetime > vorTimestamp:
                print (x)
                print (filetime)
                if x.endswith(".txt"):
                    shutil.copy(srcY + x, destY)
                    print ('')
                    print ('AFTER copy operations in Destination Dir: ')
                    DataMod()
        self.printToLabel.set(PrintTimestampGUI())
                    
def DataMod():

    conn = sqlite3.connect('DataModification.db')
    c = conn.cursor()

    ##create table
    c.execute('''CREATE TABLE IF NOT EXISTS DataMods(unique_index INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT)''');
    now=dt.datetime.now()

    ##insert data into table rows
    c.execute("INSERT INTO DataMods(timestamp) VALUES(?)", (now,))
    conn.commit()
    conn.close()

def PrintTimestampGUI():

    conn = sqlite3.connect('DataModification.db')
    c = conn.cursor()
    lastRuntime = c.execute('''SELECT timestamp FROM Datamods WHERE unique_index = (SELECT MAX(unique_index)FROM Datamods)''').fetchone() 
    

def main():
    
    root = Tk()
    my_gui = MyGui(root)
    root.mainloop()


if __name__ == "__main__": main()


#https://docs.python.org/2/library/time.html (time-stamp reference)
#https://stackoverflow.com/questions/17153779/how-can-i-print-variable-and-string-on-same-line-in-python
#https://learnpythonthehardway.org/book/ex5.html

## String variable with self.entry or self.label
