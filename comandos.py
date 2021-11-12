import os
import subprocess
import shutil
"""
    Para que caller interactue de manera correcta con las funciones que deseen añadir
    Deben tener unicamente como parametro a command, esta es una lista que utiliza caller
    contiene todos los tokens incluidos por el comando.


    PD: TENGO QUE CAMBIAR LOS ERROR PRINTS JAJAJAJJA
"""

def clear(command):
    print("\033[H\033[J", end="")
    return 0
def cd(command):
    path = command[1]
    try:
        os.chdir(path)
    except:
        print("ERROR: Not a valid path")
    return 0
def cp(command): #tal vez tenga que cambiar el planteamiento
    origin=command[1]
    destiny = command[2]
    originFile = open(origin,"r")
    destinyFile = open(destiny,"a")
    destinyFile.write(str(originFile.read()))
    return 0
def pmod(command):
    
    try:
        os.chmod(command[0],int(command[1],8))
        print("<",command[0],">", "permisos cambiados")
    except OSError:
            print("ERROR: Not a valid path")
    except Exception as e:
        print("Error: Type \"pmod --help for more information\"") #
    return 0
def mv(command):
    #command[1] es el directorio de origen del archivo que queremos mover
    #command[2] es el el directorio de destino del archivo
    path = os.path.join(command[1],command[2])
    if not os.path.exists(path):
        os.mkdir(path)
    try:
        shutil.move(os.path.join(command[1]),os.path.join(command[2]))
        print(f"Se movio {command[1]} a {command[2]}")
    except:
        print("Pero que bobito no sabe usar el comando xD")
    return 0

commandFunction = [cd,cp,clear,pmod,mv]
commandList = ["ir", "copiar", "limpiar","pmod","mover"]
argNumber = [1,2,0,2,2]


def caller(command):
    out = 'ERROR'
    foundCommand = False
    argc = len(command) - 1
    #print(f"argc: {argc}")
    commandCounter = len(commandFunction)
    for i in commandList:
            if(command[0] == i):
                foundCommand = True
    if(foundCommand):
        for i in range(commandCounter):
            if(command[0] == commandList[i] and argc == argNumber[i]):
                commandFunction[i](command)
    else:
        try:
            out=subprocess.run(command)
        except:
            print(out)
    return 0