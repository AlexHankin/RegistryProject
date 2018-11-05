from winreg import *
import csv
import os

csvfile = open('tester.csv', 'w', newline='')
csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

csvwriter.writerow(['Name','Type','Data'])

"""print r"*** Reading from SOFTWARE\Microsoft\Windows\CurrentVersion\Run ***" """
aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)

aKey = OpenKey(aReg, r"SOFTWARE\WOW6432Node\Lenel\OnGuard")
#print(QueryValueEx(aKey,"Name"))
try:
    i = 0
    while 1:
        name, data, rtype = EnumValue(aKey, i)
        print(data)
        RegistryType = ''
        if (rtype == 1):
        	RegistryType = 'REG_SZ'
        elif (rtype == 2):
        	RegistryType = 'REG_EXPAND_SZ'
        elif (rtype == 3):
        	RegistryType = '(HEX STRING)'
        	#data = chr(data)
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
        #print(RegistryType)
        #print(name, data, rtype)
        i += 1
except WindowsError:
    print()