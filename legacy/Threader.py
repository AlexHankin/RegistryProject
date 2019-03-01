import threading
import subprocess
import time
Counter = 0
newDir = ""
global output
output = ""

class Threading(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        newDir = ""
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        global newDir
        global output
        while True:
            if(newDir == ""):
                print("Nothing Yet")

            else:
                url = "Get-WmiObject CIM_DataFile -Computername Kopprdlenapp01 -Credential GSICCORP\\ahankin -filter `  \'Drive=\"C:\" and Path=\"\\\\Program Files (x86)\\\\OnGuard\\\\logs\\\\\" and Extension=\"log\"\' | Format-List *"

                p = subprocess.Popen(["powershell.exe",url], shell=True, stdout=subprocess.PIPE)
                print(p.stdout.read().decode("utf-8"))
                output = p.communicate()[0].decode("utf-8")
                print(output)
                newDir = ""


            # Do something
            time.sleep(self.interval)

example = ThreadingExample()
Counter = 2
time.sleep(3)
newDir = "\\\\Program Files (x86)\\\\OnGuard\\\\logs\\\\\""
while (newDir != ""):
    time.sleep(3)

print('Bye')
