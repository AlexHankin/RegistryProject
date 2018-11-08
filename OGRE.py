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

canvas1 = tk.Canvas(root, width = 480, height = 480) 
canvas1.pack()

#root.filename = filedialog.asksaveasfilename(initialdir = "/",title = "Choose name of CSV file, and where it should be saved",defaultextension = ".csv",filetypes = (("CSV files","*.csv"),("all files","*.*")))
#print(root.filename)

v = IntVar()
comp = IntVar()
comp.set(0)
logVar = IntVar()

myIP = Entry(width=30, state=DISABLED)
myUser = Entry(width=30, state=DISABLED)
myPass = Entry(width=30, show="*", state=DISABLED)
myFile = Entry(width=48)
myLogs = Entry(width=48, state=DISABLED)
Comments = Text(root,height=4,width=38)
LogComments = Text(root,height=4,width=38)

FileLabel = Label(text="Save CSV as:")
LogFileLabel = Label(text="Save Log CSV as:")
ipLabel = Label(text="Name/IP:")
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

def toggleLogPath():
	lv = logVar.get()
	if lv == 0:
		myLogs.configure(state=DISABLED)
		logBrowse.configure(state=DISABLED)
	else:
		myLogs.configure(state=NORMAL)
		logBrowse.configure(state=NORMAL)
	myLogs.update()
	logBrowse.update()
	enableLogs()

def enableLogs():
	lv = logVar.get()
	cv = comp.get()
	if lv == 1 and cv == 1:
		logButton.configure(state=NORMAL)
		
	else:
		logButton.configure(state=DISABLED)
	logButton.update()

def updateEntry(myFilename):
	myFile.delete(0,last=len(myFile.get()))
	myFile.insert(0, myFilename)
def updateLogEntry(myFilename):
	myLogs.delete(0,last=len(myLogs.get()))
	myLogs.insert(0, myFilename)

def fileprompt():
	root.filename = filedialog.asksaveasfilename(initialdir = "/",title = "Choose Name of CSV file, and Where it should be saved",defaultextension = ".csv",filetypes = (("CSV files","*.csv"),("all files","*.*")))
	updateEntry(str(root.filename))
def logprompt():
	updateLogEntry(str(filedialog.asksaveasfilename(initialdir = "/",title = "Choose Name of CSV file, and Where it should be saved",defaultextension = ".csv",filetypes = (("CSV files","*.csv"),("all files","*.*")))))
	#root.filename = filedialog.asksaveasfilename(initialdir = "/",title = "Choose Name of CSV file, and Where it should be saved",defaultextension = ".csv",filetypes = (("CSV files","*.csv"),("all files","*.*")))
	#updateLogEntry(str(root.filename))

local = Radiobutton(root, text="Export from Local Computer", variable=v, value=1,command=disableEntry)
remote = Radiobutton(root, text="Export from Remote Computer", variable=v, value=2,command=enableEntry)
getlogs = Checkbutton(root, text='Export Log Metadata',variable=logVar,command=toggleLogPath)

local.pack()
local.place(y=5,anchor=NW)
local.select()
remote.pack()
remote.place(y=30,anchor=NW)
getlogs.pack()
getlogs.place(y=5,x=300,anchor=NW)

myIP.pack()
myIP.place(x=62,y=60,anchor=NW)
ipLabel.pack()
ipLabel.place(y=60,anchor=NW)

myUser.pack()
myUser.place(x=62,y=90,anchor=NW)
UserLabel.pack()
UserLabel.place(y=90,anchor=NW)

myPass.pack()
myPass.place(x=62,y=120,anchor=NW)
PassLabel.pack()
PassLabel.place(y=120,anchor=NW)

myFile.pack()
myFile.place(x=100,y=160,anchor=NW)
FileLabel.pack()
FileLabel.place(y=160,anchor=NW)

myLogs.pack()
myLogs.place(x=100,y=190,anchor=NW)
LogFileLabel.pack()
LogFileLabel.place(y=190,anchor=NW)

Comments.pack()
Comments.place(x=70,y=260,anchor=NW)
LogComments.pack()
LogComments.place(x=70,y=370,anchor=NW)

def localmain():
	try:
		csvfile = open(myFile.get(), 'w', newline='')
		csvwriter = csv.writer(csvfile, delimiter=',',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)
		csvwriter.writerow(['Name','Type','Data'])
		aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)

		aKey = OpenKey(aReg, r"SOFTWARE\WOW6432Node\Lenel\OnGuard")
	except FileNotFoundError:
		Comments.delete('1.0', END)
		Comments.insert(INSERT, "No such file or directory on this system")

	try:
		i = 0
		while 1:
			name, data, rtype = EnumValue(aKey, i)
			RegistryType = ''
			if (rtype == 1):
				RegistryType = 'REG_SZ'
			elif (rtype == 2):
				RegistryType = 'REG_EXPAND_SZ'
			elif (rtype == 3):
				RegistryType = 'REG_BINARY'
				data = '(HEX STRING)'
			elif (rtype == 4):
				RegistryType = 'REG_DWORD'
			elif (rtype == 5):
				RegistryType = 'REG_DWORD_BIG_ENDIAN'
			elif (rtype == 6):
				RegistryType = 'REG_LINK'
			elif (rtype == 7):
				RegistryType = 'REG_MULTI_SZ'
			elif (rtype == 8):
				RegistryType = 'REG_RESOURCE_LIST'
			elif (rtype == 12):
				RegistryType = 'REG_QWORD'
			else:
				RegistryType = 'REG_NONE'
			
			if (name == ""):
				name = "(Default)"
			csvwriter.writerow([name,RegistryType,data])

			i += 1
	except WindowsError:
		print()
		if(i > 0):
			Comments.delete('1.0', END)
			Comments.insert(INSERT, "File Created Successfully")
			comp.set(1)
			enableLogs()
		else:
			Comments.delete('1.0', END)
			Comments.insert(INSERT, "No registries in the OnGuard directory on this \nsystem")

def remotemain():
	ip = myIP.get()
	username = myUser.get()
	password = myPass.get()
	
	try:
		csvfile = open(myFile.get(), 'w', newline='')
		csvwriter = csv.writer(csvfile, delimiter=',',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)
		csvwriter.writerow(['Name','Type','Data'])
	except FileNotFoundError:
		Comments.delete('1.0', END)
		Comments.insert(INSERT, "No such file or directory on this system")

	try:
		c = wmi.WMI(computer=ip, user=username,
		password=password,namespace="root/default").StdRegProv

		result, names, data = c.EnumValues (sSubKeyName="SOFTWARE\WOW6432Node\Lenel\OnGuard")

		for item in range(len(names)):
			RegistryType = ''
			DataName = ''
			if (data[item] == 1):
				RegistryType = 'REG_SZ'
				DataName = c.GetStringValue(sSubKeyName="SOFTWARE\WOW6432Node\Lenel\OnGuard", sValueName=names[item])[1]
			elif (data[item] == 2):
				RegistryType = 'REG_EXPAND_SZ'
				DataName = c.GetExpandedStringValue(sSubKeyName="SOFTWARE\WOW6432Node\Lenel\OnGuard", sValueName=names[item])[1]
			elif (data[item] == 3):
				RegistryType = 'REG_BINARY'
				DataName = '(HEX VALUE)'
			elif (data[item] == 4):
				RegistryType = 'REG_DWORD'
				DataName = c.GetDWORDValue(sSubKeyName="SOFTWARE\WOW6432Node\Lenel\OnGuard", sValueName=names[item])[1]
			elif (data[item] == 7):
				RegistryType = 'REG_MULTI_SZ'
				DataName = c.GetMultiStringValue(sSubKeyName="SOFTWARE\WOW6432Node\Lenel\OnGuard", sValueName=names[item])[1]
			elif (data[item] == 11):
				RegistryType = 'REG_QWORD'
				DataName = c.GetQWORDValue(sSubKeyName="SOFTWARE\WOW6432Node\Lenel\OnGuard", sValueName=names[item])[1]
			else:
				RegistryType = 'REG_NONE'
				DataName = ''	
			csvwriter.writerow([names[item],RegistryType,DataName])

		if(len(names) > 0):
			Comments.delete('1.0', END)
			Comments.insert(INSERT, "File Created Successfully")
			comp.set(1)
			#enableLogs()
		else:
			Comments.delete('1.0', END)
			Comments.insert(INSERT, "No registries in the OnGuard directory on this \nsystem")

	except wmi.x_wmi:
		Comments.delete('1.0', END)
		Comments.insert(INSERT, "Authentication Failed. Check credentials and/or network connection")  

def main():
	if (v.get()==1):
		localmain()

	elif (v.get()==2):
		remotemain()

browse = tk.Button (root, text='Browse...', command=fileprompt) 
#canvas1.create_window(x=150,y=160, window=button1)
browse.pack()
browse.place(x=400,y=156,anchor=NW)

logBrowse = tk.Button (root, text='Browse...', command=logprompt,state=DISABLED)
#canvas1.create_window(x=150,y=160, window=button1)
logBrowse.pack()
logBrowse.place(x=400,y=186,anchor=NW)

mainButton = tk.Button (root, text='Export and Create File',command=main) 
#canvas1.create_window(x=150,y=160, window=button1)
mainButton.pack()
mainButton.place(x=145,y=220,anchor=NW)

logButton = tk.Button (root, text='Export Log Directory Metadata',command=main,state=DISABLED) 
#canvas1.create_window(x=150,y=160, window=button1)
logButton.pack()
logButton.place(x=145,y=335,anchor=NW)

northlandLabel = Label(text="Northland Control Systems", fg='firebrick3')
northlandLabel.pack()
northlandLabel.place(x=325,y=450,anchor=NW)

root.mainloop()