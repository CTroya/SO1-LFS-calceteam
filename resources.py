import shutil
import os
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def processText(text):
    processedText = text
    for i in range(len(text)):
        processedText[i] = processedText[i].split(':')
    return processedText

def readFile(filename):
    with open(filename) as file:
        lines = file.readlines() 
        lines = [line.rstrip() for line in lines]
    print(lines)
    return lines

def getNewUserID():#requiere root
    passwdPath = "/etc/passwd"
    passwd = open(passwdPath,"r")
    userID = 0
    passwd = readFile(passwdPath)      
    for i in range(len(passwd)):
        passwd[i] = passwd[i].split(':')
    for i in range(len(passwd)):
        if userID < int(passwd[i][2]):
            userID = int(passwd[i][2])
    return userID + 1
def getNewGroupID():#requiere root
    groupPath = "/etc/group"
    groupID = 0
    with open(groupPath) as file:
        group = file.readlines()
        group = [group.rstrip() for group in group]
    for i in range(len(group)):
        group[i] = group[i].split(':')
    for i in range(len(group)):
        if groupID < int(group[i][2]):
            groupID = int(group[i][2])
    return groupID + 1
