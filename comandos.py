import os

def clear():
    print("\033[H\033[J", end="")
    return 0
def cd(path):
    try:
        os.chdir(path)
    except:
        print("ERROR: Not a valid path")
    return 0
def cp(origin, destiny): #tal vez tenga que cambiar el planteamiento
    originFile = open(origin,"r")
    destinyFile = open(destiny,"a")
    destinyFile.write(str(originFile.read()))
    return 0
commandList = ["ir", "copiar", "limpiar"]
argNumber = [1,2,0]

def caller(command):
    foundCommand = False
    argc = len(command) - 1
    for i in commandList:
            if(command[0] == i):
                foundCommand = True
    if(foundCommand):
        if(command[0] == commandList[0] and argc == argNumber[0]):
            cd(command[1])
        elif(command[0]==commandList[1] and argc == argNumber[1]):
            cp(command[1],command[2])
        elif(command[0]==commandList[2] and argc == argNumber[2]):
            clear()
    return 0