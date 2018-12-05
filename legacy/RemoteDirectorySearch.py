import subprocess
import time
from datetime import date

url = "Get-WmiObject CIM_DataFile -Computername Kopprdlenapp01 -Credential GSICCORP\\ahankin -filter `  \'Drive=\"C:\" and Path=\"\\\\Program Files (x86)\\\\OnGuard\\\\logs\\\\\" and Extension=\"log\"\' | Format-List *"
p = subprocess.Popen(["powershell.exe",url], shell=True, stdout=subprocess.PIPE)
output = p.communicate()[0].decode("utf-8")
infoList = output.splitlines()
Counter = 0
filteredList = []

for info in infoList:
	#print(info)
	if("Name                  :" not in info):
		if("LastModified" not in info):
			if("FileSize" not in info):
				Counter += 1
				info = None
			else:
				filteredList.append(info)
		else:
			filteredList.append(info)
	else:
		filteredList.append(info)
	#print(info)
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


#print(len(infoList))
#print(Counter)
for entry in allEntries:
	entry[0] = entry[0].split('\\', -1)[-1]
	entry[1] = round(int(entry[1])/1024/1024,3)
	if(entry[1] == 0.0):
		entry[1] = "<0.001"
	entry[2] = entry[2].split('.', -1)[0]
	timeString = str(entry[2])
	timeTuple = (int(timeString[0:4]),int(timeString[4:6]),int(timeString[6:8]),int(timeString[8:10]),int(timeString[10:12]),int(timeString[12:14]),date(int(timeString[0:4]),int(timeString[4:6]),int(timeString[6:8])).weekday(),0,-1)
	entry[2] = time.asctime(timeTuple)
	print(entry)
