import os
from posix import listdir
import subprocess
import shutil
"""
    Para que caller interactue de manera correcta con las funciones que deseen añadir
    Deben tener unicamente como parametro a command, esta es una lista que utiliza caller
    contiene todos los tokens incluidos por el comando.
    hola que tal?

    PD: TENGO QUE CAMBIAR LOS ERROR PRINTS JAJAJAJJA
    #Investigar/preguntar acerca de los error logs
    
"""
#Funcion listar
def ls(command):
    argc = len(command) - 1
    if argc == 0:
        argc = os.listdir(os.path.join(os.getcwd()))
    else:
        print(command[1])
        #argc = os.listdir(os.path.join(os.getcwd(),command[1]))
        argc = os.listdir(os.path.join(os.getcwd(),os.path.abspath(command[1])))

    print(*argc,sep ="      ")
    return 0
#Funcion limpiar terminal
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

def cp(command):
    #command[1] es el directorio de origen del archivo que queremos mover (creo que solo nombre de archivo (?))
    #command[2] es el el directorio de destino del archivo
    origin = os.path.join(os.getcwd(),command[1])
    destiny = os.path.join(os.getcwd(),command[2])
    try:
        shutil.copy(os.path.join(command[1]),os.path.join(command[2]))
        print(f"Se movio {command[1]} a {command[2]}")
    except:
        print("Pero que bobito no sabe usar el comando xD")
    return 0

def mv(command):
    #command[1] es el directorio de origen del archivo que queremos mover (creo que solo nombre de archivo (?))
    #command[2] es el el directorio de destino del archivo
    origin = os.path.join(os.getcwd(),command[1])
    destiny = os.path.join(os.getcwd(),command[2])
    try:
        shutil.move(os.path.join(command[1]),os.path.join(command[2]))
        print(f"Se movio {command[1]} a {command[2]}")
    except:
        print("Pero que bobito no sabe usar el comando xD")
    return 0

def pmod(command):
    try:
        os.chmod(command[0],int(command[1],8))
        print(f"{command[0]} permissions changed")
    except OSError:
            print("ERROR: Not a valid path")
    except Exception:
        print("Error: Type \"pmod --help for more information\"")
    return 0
def mkdir(command):
    if len(command) == 0:
        print(f"crearDir: no directory specified")
        return 1
    if os.path.exists(os.path.join(os.getcwd(),command[1])):
        print(f"crearDir: cannot create directory ‘{command[1]}’: File exists")
    else:
        os.mkdir(os.path.join(os.getcwd(),command[1]))
    return 0
def rename(command):
    if len(command) < 2:
        print("rename: missing operand")
        return 1
    else:
        os.rename(os.path.join(os.getcwd(),command[1]),os.path.join(os.getcwd(),command[2]))
        
    return 0

commandFunction = [cd,cp,clear,pmod,mv,ls,mkdir,rename]
commandList = ["ir", "copiar", "limpiar","cpermi","mover","listar","crearDir","renombrar"]
argNumber = [1,2,0,2,2,1,1,2]#cantidad maxima de argumentos

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
            if(command[0] == commandList[i] and argc <= argNumber[i]):
                commandFunction[i](command)
    else:
        try:
            out=subprocess.run(command)
        except:
            print(out)
    return 0




"""
def mv(command):
    #command[1] es el directorio de origen del archivo que queremos mover (creo que solo nombre de archivo (?))
    #command[2] es el el directorio de destino del archivo
    try:
        shutil.move(os.path.join(command[1]),os.path.join(command[2]))
        print(f"Se movio {command[1]} a {command[2]}")
    except:
        print("Pero que bobito no sabe usar el comando xD")
    return 0


def mv(command): #tal vez tenga que cambiar el planteamiento
    origin=command[1]
    destiny = command[2]
    a = 0
    if os.path.exists(destiny):
        a = input(f"La direccion de destino: {destiny} ya existe, quieres sobreescribir el archivo? ('yes' para continuar)")
        if a != "yes":
            return 0
    try:
        if os.path.exists(os.path.join(origin,destiny)):
            originFile = open(origin,"rb")
            destinyFile = open(destiny,"wb")
            destinyFile.write(originFile.read())
            destinyFile.close()
            originFile.close()
            os.remove(originFile)
            print(f"El archivo {origin} se movio a {destiny}")
    except:
        print("F")
    return 0

"""
