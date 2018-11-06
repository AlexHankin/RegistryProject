#!/usr/bin/env python3
from winreg import *
import csv
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import wmi

root= tk.Tk() 
root.title("OnGuard Registry Exporter")

canvas1 = tk.Canvas(root, width = 450, height = 250) 
canvas1.pack()

#root.filename = filedialog.asksaveasfilename(initialdir = "/",title = "Choose name of CSV file, and where it should be saved",defaultextension = ".csv",filetypes = (("CSV files","*.csv"),("all files","*.*")))
#print(root.filename)

v = IntVar()



myIP = Entry(width=30, state=DISABLED)
myUser = Entry(width=30, state=DISABLED)
myPass = Entry(width=30, show="*", state=DISABLED)
myFile = Entry(width=48)

FileLabel = Label(text="Save CSV as:")
ipLabel = Label(text="IP:")
UserLabel = Label(text="Username:")
PassLabel = Label(text="Password:")

def enableEntry():
	myIP.configure(state=NORMAL)
	myIP.update()
	myUser.configure(state=NORMAL)
	myUser.update()
	myPass.configure(state=NORMAL)
	myPass.update()

def disableEntry():
	myIP.configure(state=DISABLED)
	myIP.update()
	myUser.configure(state=DISABLED)
	myUser.update()
	myPass.configure(state=DISABLED)
	myPass.update()

def updateEntry(myFilename):
	myFile.delete(0,last=len(myFile.get()))
	myFile.insert(0, myFilename)

def fileprompt():
	root.filename = filedialog.asksaveasfilename(initialdir = "/",title = "Choose Name of CSV file, and Where it should be saved",defaultextension = ".csv",filetypes = (("CSV files","*.csv"),("all files","*.*")))
	updateEntry(str(root.filename))


local = Radiobutton(root, text="Export from Local Computer", variable=v, value=1,command=disableEntry)
remote = Radiobutton(root, text="Export from Remote Computer", variable=v, value=2,command=enableEntry)

local.pack()
local.place(y=5,anchor=NW)
local.select()
remote.pack()
remote.place(y=30,anchor=NW)
myIP.pack()
myIP.place(x=20,y=60,anchor=NW)
ipLabel.pack()
ipLabel.place(y=60,anchor=NW)
myUser.pack()
myUser.place(x=62,y=90,anchor=NW)
UserLabel.pack()
UserLabel.place(y=90,anchor=NW)
myPass.pack()
myPass.place(x=60,y=120,anchor=NW)
PassLabel.pack()
PassLabel.place(y=120,anchor=NW)
FileLabel.pack()
FileLabel.place(y=160,anchor=NW)
myFile.pack()
myFile.place(x=73,y=160,anchor=NW)



browse = tk.Button (root, text='Browse...', command=fileprompt) 
#canvas1.create_window(x=150,y=160, window=button1)
browse.pack()
browse.place(x=375,y=156,anchor=NW)

mainButton = tk.Button (root, text='Export and Create File',) 
#canvas1.create_window(x=150,y=160, window=button1)
mainButton.pack()
mainButton.place(x=155,y=190,anchor=NW)

northlandLabel = Label(text="Northland Control Systems", fg='firebrick3')
northlandLabel.pack()
northlandLabel.place(x=301,y=232,anchor=NW)

root.mainloop()