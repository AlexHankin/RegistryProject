#!/usr/bin/env python3
from winreg import *
import csv
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import wmi

ip = "10.139.2.105"
username = "DVT-SECAS-016\\administrator"
password = "Welcome1"
from socket import *
try:
    print("Establishing connection to %s" %ip)
    connection = wmi.WMI(ip, user=username, password=password).StdRegProv
    aReg = connection.ConnectRegistry(None,HKEY_LOCAL_MACHINE)
    print("Connection established")
except wmi.x_wmi:
    print("Your Username and Password of "+getfqdn(ip)+" are wrong.")

root= tk.Tk() 

   
#canvas1 = tk.Canvas(root, width = 450, height = 500) 
#canvas1.pack()

root.filename = filedialog.asksaveasfilename(initialdir = "/",title = "Choose name of CSV file, and where it should be saved",defaultextension = ".csv",filetypes = (("CSV files","*.csv"),("all files","*.*")))
print(root.filename)
      
#button1 = tk.Button (root, text='Exit Application', command=root.destroy) 
#canvas1.create_window(170, 130, window=button1) 

csvfile = open(root.filename, 'w', newline='')
csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

csvwriter.writerow(['Name','Type','Data'])

"""print r"*** Reading from SOFTWARE\Microsoft\Windows\CurrentVersion\Run ***" """
#aReg = ConnectRegistry(connection,HKEY_LOCAL_MACHINE)

aKey = OpenKey(aReg, r"SOFTWARE\WOW6432Node\Microsoft\RADAR\CommitExhaustion\Settings")

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

root.mainloop()