#!/usr/bin/env python3
from winreg import *
import csv, os, time
from os import listdir
from os.path import isfile, join
#from stat import *
import tkinter as tk
from tkinter import filedialog,font,ttk
from tkinter import *
import wmi
import psutil
from idlelib.redirector import WidgetRedirector
from datetime import date
import threading
import subprocess

##############################################
#	OnGuard Registry Exporter				 #
#											 #
#	Created by Alex Hankin & Santiago Loane  #
#	for Northland Controls 11/5/18			 #
#											 #
#	Ver. 1.8.0 		10/28/19				 #
##############################################

if getattr(sys, 'frozen', False):
	# running in a bundle
	bundle_dir = sys._MEIPASS
else:
	# running in a python environment
	bundle_dir = os.path.dirname(os.path.abspath(__file__))

class ReadOnlyText(Text):
	def __init__(self, *args, **kwargs):
		Text.__init__(self, *args, **kwargs)
		self.redirector = WidgetRedirector(self)
		self.insert = self.redirector.register("insert", lambda *args,**kw: "break")
		self.delete = self.redirector.register("delete", lambda *args,**kw: "break")

root= tk.Tk() 

## define style
main_font = font.nametofont("TkDefaultFont")
main_font.configure(family="Tahoma")
root.option_add("*Font", main_font)
bg_color = "gainsboro"
fg_color = "#c8102e" #"firebrick2"
fg_inactive_color = "grey10"
fg_highlight_color = "#a20b20"#"firebrick3" #"#c8102e"
dark_text_color = "grey10"
light_text_color = "white"
inactive_field_color = bg_color#"grey75"
read_only_color = "#ededed"
border_color="grey55"
button_border_color="grey35"

s = ttk.Style()
T = {}
# Standard Button
T["TButton"] = {}
T["TButton"]["configure"] = {}
T["TButton"]["map"] = {}

T["TButton"]["configure"]["relief"] = "flat"
T["TButton"]["configure"]["padding"] = 2
#T["TButton"]["configure"]["borderwidth"] = 2
#T["TButton"]["configure"]["bordercolor"] = button_border_color
#T["TButton"]["configure"]["lightcolor"] = button_border_color
#T["TButton"]["configure"]["darkcolor"] = button_border_color
T["TButton"]["map"]["background"] = [("active", fg_highlight_color),("pressed",fg_highlight_color),("disabled",bg_color),("!disabled",fg_color)]
T["TButton"]["map"]["foreground"] = [("active", light_text_color),("pressed",light_text_color),("disabled",dark_text_color),("!disabled",light_text_color)]

# Label
T["TLabel"] = {}
T["TLabel"]["configure"] = {}
T["TLabel"]["map"] = {}

T["TLabel"]["configure"]["relief"] = "flat"
T["TLabel"]["configure"]["foreground"] = dark_text_color
T["TLabel"]["configure"]["background"] = bg_color

# Entry
T["TEntry"] = {}
T["TEntry"]["configure"] = {}
T["TEntry"]["map"] = {}

T["TEntry"]["configure"]["relief"] = "flat"
T["TEntry"]["configure"]["bordercolor"] = border_color
T["TEntry"]["configure"]["background"] = border_color
T["TEntry"]["configure"]["highlightthickness"] = 0
T["TEntry"]["configure"]["selectbackground"] = fg_color
T["TEntry"]["map"]["foreground"] = [("readonly","black"),("disabled","black"),("!disabled",dark_text_color)]
T["TEntry"]["map"]["fieldbackground"] = [("readonly",read_only_color),("disabled",inactive_field_color),("!disabled","white")]
T["TEntry"]["map"]["lightcolor"] = [("readonly",read_only_color),("disabled",inactive_field_color),("!disabled","white")]

s.theme_create("Northland",parent='clam',settings=T)
s.theme_use(themename="Northland")
## end style definition

root.iconbitmap("%s\\img\\northland.ico"%bundle_dir)
root.title("OnGuard Registry Exporter")

canvas1 = tk.Canvas(root, width = 500, height = 492)
canvas1.config(background=bg_color,bd=0,highlightthickness=0)

canvas1.pack()

#root.filename = filedialog.asksaveasfilename(initialdir = "/",title = "Choose name of CSV file, and where it should be saved",defaultextension = ".csv",filetypes = (("CSV files","*.csv"),("all files","*.*")))
#print(root.filename)

lenel_services = ['LS Client Update Server','LS Communication Server','LS Config Download Service',	'LS DataConduIT Message Queue Server','LS DataConduIT Service',\
	'LS DataExchange Server','LS Event Context Provider','LS Global Output Server','LS ID Allocation','LS License Server','LS Linkage Server','LS Login Driver',\
	'LS Message Broker','LS Open Access','LS Open Access Web Proxy','LS PTZ Tour Server','LS Replicator','LS Site Publication Server','LS Video Archive Server',\
	'LS Web Event Bridge','LS Web Service']

v = IntVar()
v.set(1)
comp = IntVar()
comp.set(0)
logVar = IntVar()

remoteDirectory = ""
global output
global csvlogwriter
output = ""

myIP = ttk.Entry(width=30, state=DISABLED, style="Northland.TEntry")
myUser = ttk.Entry(width=30, state=DISABLED, style="Northland.TEntry")
myPass = ttk.Entry(width=30, show="*", state=DISABLED, style="Northland.TEntry")
myFile = ttk.Entry(width=45, style="Northland.TEntry")
myLogs = ttk.Entry(width=45, state=DISABLED, style="Northland.TEntry")
Comments = ReadOnlyText(root,height=4,width=50,highlightthickness=1,highlightbackground=border_color,selectbackground=fg_color,relief="flat",bg=read_only_color)
LogComments = ReadOnlyText(root,height=4, width=50,highlightthickness=1,highlightbackground=border_color,selectbackground=fg_color,relief="flat",bg=inactive_field_color)

FileLabel = ttk.Label(text="Save CSV as:",style="Northland.TLabel")
LogFileLabel = ttk.Label(text="Save Log CSV as:",style="Northland.TLabel")
ipLabel = ttk.Label(text="Domain/IP:",style="Northland.TLabel")
UserLabel = ttk.Label(text="Username:",style="Northland.TLabel")
PassLabel = ttk.Label(text="Password:",style="Northland.TLabel")
LogNotice = ttk.Label(text="*For Security Purposes, \ncredentials will be required again",style="Northland.TLabel")

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
		LogNotice.configure(state=DISABLED)
		LogNotice.update()
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
		LogComments.configure(state=NORMAL,bg=read_only_color)
		if (v.get()==2):
			LogNotice.pack()
			LogNotice.place(x=260,y=332,anchor=NW)

		
	else:
		logButton.configure(state=DISABLED)
		LogComments.configure(state=DISABLED,bg=inactive_field_color)
		LogNotice.pack_forget()
		LogNotice.update()
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

def getfiles(dirPath):
	return [f for f in listdir(dirPath) if isfile(join(dirPath,f)) and f[-4:] == ".log"]

local = ttk.Radiobutton(root, style="Northland.TRadiobutton", text="Export from Local Computer", variable=v, value=1,command=disableEntry)
remote = ttk.Radiobutton(root, style="Northland.TRadiobutton", text="Export from Remote Computer", variable=v, value=2,command=enableEntry)
getlogs = ttk.Checkbutton(root, style="Northland.TCheckbutton", text='Export Log Metadata',variable=logVar,command=toggleLogPath)

local.pack()
local.place(y=5,anchor=NW)
#local.cget(option="current")
remote.pack()
remote.place(y=30,anchor=NW)
getlogs.pack()
getlogs.place(y=5,x=300,anchor=NW)

myIP.pack()
myIP.place(x=70,y=60,anchor=NW)
ipLabel.pack()
ipLabel.place(x=5,y=60,anchor=NW)

myUser.pack()
myUser.place(x=70,y=90,anchor=NW)
UserLabel.pack()
UserLabel.place(x=5,y=90,anchor=NW)

myPass.pack()
myPass.place(x=70,y=120,anchor=NW)
PassLabel.pack()
PassLabel.place(x=5,y=120,anchor=NW)

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
LogComments.place(x=70,y=373,anchor=NW)

class Threading(object):
	""" 
	The run() method will be started and it will run in the background
	until the application exits.
	"""

	def __init__(self, interval=1):

		self.interval = interval
		newDir = ""
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True                            # Daemonize thread
		thread.start()

	def run(self):
		""" Method that runs forever """
		global newDir
		global output
		global remoteDirectory
		filler = 0
		while True:

			if(remoteDirectory == ""):
				filler = 1

			else:
				csvlogfile = open(myLogs.get(), 'w', newline='')
				csvlogwriter = csv.writer(csvlogfile, delimiter=',',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)

				cmdLine = "Get-WmiObject CIM_DataFile -Computername " + myIP.get() + " -Credential User... -filter `  \'Drive=\"C:\" and Path=\"" + remoteDirectory + "\" and Extension=\"log\"\' | Format-List *"
				p = subprocess.Popen(["powershell.exe",cmdLine], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				output = p.communicate()[0].decode("utf-8")

				infoList = output.splitlines()
				filteredList = []
				csvlogwriter.writerow(['Name','Size (MB)','Last Modified (Time Zone Respective to Remote Destination)'])


				for info in infoList:
					if("Name                  :" not in info):
						if("LastModified" not in info):
							if("FileSize" not in info):
								info = None
							else:
								filteredList.append(info)
						else:
							filteredList.append(info)
					else:
						filteredList.append(info)
				shift = 0
				newEntry = []
				allEntries = []
				
				for info in filteredList:
					if(shift == 3):
						shift = 0
						allEntries.append(newEntry)
						newEntry = []
					newEntry.append(info.split(': ', 1)[-1])
					shift += 1
				allEntries.append(newEntry)

				try:
					for entry in allEntries:
						entry[0] = entry[0].split('\\', -1)[-1]
						entry[1] = round(int(entry[1])/1024/1024,3)
						if(entry[1] == 0.0):
							entry[1] = "<0.001"
						entry[2] = entry[2].split('.', -1)[0]
						timeString = str(entry[2])
						timeTuple = (int(timeString[0:4]),int(timeString[4:6]),int(timeString[6:8]),int(timeString[8:10]),int(timeString[10:12]),int(timeString[12:14]),date(int(timeString[0:4]),int(timeString[4:6]),int(timeString[6:8])).weekday(),0,-1)
						entry[2] = time.asctime(timeTuple)
						csvlogwriter.writerow(entry)
					LogComments.insert(INSERT, "Logs exported successfully")
					#remoteDirectory = ""
					csvlogfile.close()
				except IndexError:
					LogComments.insert(INSERT, "Authentication Failed. Check both credential submissions and/or network connection")
			# Do something
			remoteDirectory = ""
			time.sleep(self.interval)

def localmain():
	hasKey = False
	try:
		csvfile = open(myFile.get(), 'w', newline='')
		csvwriter = csv.writer(csvfile, delimiter=',',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)
		csvwriter.writerow(['Name','Type','Data'])
		aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)

		aKey = OpenKey(aReg, r"SOFTWARE\WOW6432Node\Lenel\OnGuard")
		hasKey = True
	except FileNotFoundError:
		Comments.delete('1.0', END)
		Comments.insert(INSERT, "No such file or directory on this system")

	if hasKey:
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
				Comments.insert(INSERT, "Registry exported successfully")
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
			Comments.insert(INSERT, "Registry exported successfully")
			comp.set(1)
			enableLogs()
		else:
			Comments.delete('1.0', END)
			Comments.insert(INSERT, "No registries in the OnGuard directory on this \nsystem")

	except wmi.x_wmi:
		Comments.delete('1.0', END)
		Comments.insert(INSERT, "Authentication Failed. Check credentials and/or network connection") 

def getlogs():
	if (v.get()==1):
		localgetlogs()
	elif (v.get()==2):
		remotegetlogs()

def localgetlogs():
	#tzone = time.tzname[time.daylight]
	try:
		csvlogfile = open(myLogs.get(), 'w', newline='')
		csvlogwriter = csv.writer(csvlogfile, delimiter=',',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)
		csvlogwriter.writerow(['Name','Size (MB)','Last Modified (local time)'])

		exportfile = open(myFile.get(), 'r',newline='')
		exportvals = csv.reader(exportfile, delimiter=',')
		temp = [row[2] for row in exportvals if row[0] == "LogFilePath"]
		logDir = temp[0]
		LogComments.delete('1.0', END)
		LogComments.insert(INSERT, "Exporting from:\n%s::%s\n" %(myIP.get(),logDir))
		logFiles = getfiles(logDir)
		for filename in logFiles:
			#metadata = (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)
			try:
				_, _, _, _, _, _, logSize, _, logModTime, _ = os.stat(logDir+"/"+filename)
			except IOError:
				logSize, logModTime = "error", "error"
			newLogSize = round(logSize/1024/1024,3)
			if(newLogSize == 0.0):
				newLogSize = "<0.001"
			csvlogwriter.writerow([filename,newLogSize,time.asctime(time.localtime(logModTime))])

		if len(logFiles)>0:
			LogComments.insert(INSERT, "Logs exported successfully")
		else:
			LogComments.insert(INSERT, "No .log files found in this directory")


		#aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)

		#aKey = OpenKey(aReg, r"SOFTWARE\WOW6432Node\Lenel\OnGuard")
	except FileNotFoundError:
		#LogComments.delete('1.0', END)
		LogComments.insert(INSERT, "No such file or directory on this system")

def remotegetlogs():
	#tzone = time.tzname[time.daylight]
	global remoteDirectory
	try:
		#csvlogfile = open(myLogs.get(), 'w', newline='')
		#csvlogwriter = csv.writer(csvlogfile, delimiter=',',
		#						quotechar='|', quoting=csv.QUOTE_MINIMAL)
		#csvlogwriter.writerow(['Name','Size (MB)','Last Modified (local time)'])

		exportfile = open(myFile.get(), 'r',newline='')
		exportvals = csv.reader(exportfile, delimiter=',')
		temp = [row[2] for row in exportvals if row[0] == "LogFilePath"]
		logDir = temp[0]
		LogComments.delete('1.0', END)
		LogComments.insert(INSERT, "Exporting from %s\n" %logDir)

		newDir = ""
		for char in logDir:
			if char == "\\":
				newDir = newDir + "\\\\"
			else:
				newDir = newDir + char
		newDir = newDir[2:] + "\\\\"

		remoteDirectory = newDir
		
	except FileNotFoundError:
		#LogComments.delete('1.0', END)
		LogComments.insert(INSERT, "No such file or directory on this system")

def getservices():
	if (v.get() == 1):
		serv_res = localgetservices()
	elif (v.get() == 2):
		serv_res = remotegetservices()

	print(serv_res)
	return serv_res

def localgetservices():
	return [(serviceName,psutil.win_service_get(serviceName)['status'] == 'running') for serviceName in lenel_services]

def remotegetservices():
	ip = myIP.get()
	username = myUser.get()
	password = myPass.get()

	try:
		c = wmi.WMI(computer=ip, user=username, password=password)

		# Below will output all possible service names
		return [(service.Name,service.State == 'Running') for service in [s for s in c.Win32_Service() if s.Name in lenel_services]]

	except wmi.x_wmi:
		print("Authentication Failed. Check credentials and/or network connection") 

def main():
	if (v.get()==1):
		localmain()

	elif (v.get()==2):
		remotemain()

# establish coords for buttons
b1x,b1y = 430,156
b2x,b2y = 430,186
mbx,mby = 70,220
lbx,lby = 70,335
sbx,sby = 300,60

# instantiate buttons
browse = ttk.Button (root, style="Northland.TButton",text='Browse...', command=fileprompt) 
browse.pack()
logBrowse = ttk.Button (root, style="Northland.TButton",text='Browse...', command=logprompt,state=DISABLED)
logBrowse.pack()
mainButton = ttk.Button (root, style="Northland.TButton", text='Export and Create File',command=main) 
mainButton.pack()
logButton = ttk.Button (root, style="Northland.TButton", text='Export Log Directory Metadata',command=getlogs,state=DISABLED) 
logButton.pack()
serviceButton = ttk.Button (root, style="Northland.TButton", text='Check Services',command=getservices) 
serviceButton.pack()

# draw button borders
bw = 1 		# define border width around buttons in pixels
canvas1.update()
b1 = canvas1.create_rectangle(b1x,b1y,b1x+browse.winfo_width()+2*bw-1,b1y+browse.winfo_height()+2*bw-1,fill=button_border_color,outline=button_border_color)
b2 = canvas1.create_rectangle(b2x,b2y,b2x+logBrowse.winfo_width()+2*bw-1,b2y+logBrowse.winfo_height()+2*bw-1,fill=button_border_color,outline=button_border_color)
b3 = canvas1.create_rectangle(mbx,mby,mbx+mainButton.winfo_width()+2*bw-1,mby+mainButton.winfo_height()+2*bw-1,fill=button_border_color,outline=button_border_color)
b4 = canvas1.create_rectangle(lbx,lby,lbx+logButton.winfo_width()+2*bw-1,lby+logButton.winfo_height()+2*bw-1,fill=button_border_color,outline=button_border_color)
b4 = canvas1.create_rectangle(sbx,sby,sbx+serviceButton.winfo_width()+2*bw-1,sby+serviceButton.winfo_height()+2*bw-1,fill=button_border_color,outline=button_border_color)

# place buttons 
browse.place(x=b1x+bw,y=b1y+bw,anchor=NW)
logBrowse.place(x=b2x+bw,y=b2y+bw,anchor=NW)
mainButton.place(x=mbx+bw,y=mby+bw,anchor=NW)
logButton.place(x=lbx+bw,y=lby+bw,anchor=NW)
serviceButton.place(x=sbx+bw,y=sby+bw,anchor=NW)

northlandLabel = Label(text="Northland Control Systems",fg=fg_color,bg=bg_color)
northlandLabel.pack()
northlandLabel.place(x=345,y=470,anchor=NW)

thread = Threading()

root.mainloop()

# To build, run: pyinstaller --windowed --onefile --icon=northland.ico --clean OGRE.py