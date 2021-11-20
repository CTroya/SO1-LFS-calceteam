from genericpath import isdir, isfile
import os
from posix import listdir
import subprocess
import shutil
from Crypto.Cipher import DES
import shell
import getpass
import hashlib
import psutil
import time
import sys

"""
    Para que caller interactue de manera correcta con las funciones que deseen añadir
    Deben tener unicamente como parametro a command, esta es una lista que utiliza caller
    contiene todos los tokens incluidos por el comando.
    hola que tal?

    PD: TENGO QUE CAMBIAR LOS ERROR PRINTS JAJAJAJJA
    #Investigar/preguntar acerca de los error logs
    xd
    passwd
    shadow
    group
    directorios del usuario
    /skel
"""
def adduser(command):
    if shell.user != 'root': 
        print("ERROR: You dont posses the required permissions to execute this command")
        return 1
    if len(command) != 2:
        print("ERROR: argument quantity mismatch")
        return 1
    userName = command[1]
    check,userPassword =  0,1
    
    shadowPath = "/etc/shadow"
    passwdPath = "/etc/passwd"
    groupPath = "/etc/group"
    #vamos a crear una copia de los archivos para no cagarla despues xD
    shutil.copy(shadowPath,os.getcwd())
    shutil.copy(passwdPath,os.getcwd())

    shadowPath = os.path.join(os.getcwd(),"shadow")
    passwdPath = os.path.join(os.getcwd(),"passwd")
    
    shadow = open("shadow","r+")
    passwd = open("passwd","r+")
    #desde este punto las variables passwd y shadow se vuelven vectores de cadenas
    with open(passwdPath) as file:
        passwd = file.readlines()
        passwd = [passwd.rstrip() for passwd in passwd]
    with open(shadowPath) as file:
        shadow = file.readlines()
        shadow = [shadow.rstrip() for shadow in shadow]   
    with open(groupPath) as file:
        group = file.readlines()
        group = [group.rstrip() for group in group]         
    for i in range(len(passwd)):
        passwd[i] = passwd[i].split(':')
    for i in range(len(shadow)):
        shadow[i] = shadow[i].split(':')
    for i in range(len(group)):
        group[i] = group[i].split(':')
    for i in range(len(group)):
        if group[i][0] == userName:
            print(f"{userName} already exists. Exiting...")
            return 1
    while check != userPassword:
        userPassword = getpass.getpass("Create password: ")
        check = getpass.getpass("Verify your password: ")
    userPassword = hashlib.sha512(str(userPassword).encode('UTF-8')).hexdigest()
    print(userPassword)
    return 0


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

#NUEVO MOD    
def cd(command):
    if len(command)-1 !=  1: return 0
    path = command[1]
    try:
        print(os.path.abspath(path))
        os.chdir(os.path.abspath(path))
    except:
        print("ERROR: Not a valid path")
    return 0

#NUEVO MOD    
def cp(command):
    if len(command)-1 !=  2: return 1
    #command[1] es el directorio de origen del archivo que queremos mover (creo que solo nombre de archivo (?))
    #command[2] es el el directorio de destino del archivo
    origin = os.path.join(os.getcwd(),command[1])
    destiny = os.path.join(os.getcwd(),command[2])
    try:
        if isdir(origin):
            shutil.copytree(os.path.join(command[1]),os.path.join(command[2]))
            print(f"Se copió la carpeta {command[1]} a {command[2]}")
        else:        
            shutil.copy(os.path.join(command[1]),os.path.join(command[2]))
            print(f"Se copio el archivo {command[1]} a {command[2]}")
    except:
        print("Error:No se pudo realizar la copia")
    return 0

def mv(command):
    if len(command)-1 !=  2: return 1
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
    print(command)
    if len(command)-1 !=  2: return 0
    try:
        os.chmod(command[0],333)
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



#NUEVO
def passwd(command):

    return 0


#NUEVO
def uptime(command):
    print(time.strftime("%H:%M:%S", time.gmtime()))    
    print(time.strftime("%Hh%Mm", time.gmtime(round(time.time()-psutil.boot_time()))))
    print("Carga promedio:",[str(x) for x in os.getloadavg()])
    #    /var/run/utmp
    return 0



#NUEVO
def cat(command):
    print(command[1])
    archivo=os.path.abspath(command[1])
    if isfile(archivo):
        try:
            fd = os.open(archivo, os.O_RDONLY)
            data = os.read(fd, 4096)
            if len(data) == 0:
                print("Archivo Vacio")
                return 0
            os.close(fd)
            os.write(sys.stdout.fileno(), data)
        except:
            print("Error al abrir el archivo")
    else:
        print("Error no es un archivo")
    return 0


commandFunction = [cd,cp,clear,pmod,mv,ls,mkdir,rename,adduser,passwd,uptime,cat]
commandList = ["ir", "copiar", "limpiar","cpermi","mover","listar","crearDir","renombrar","addUsuario","contrasena","tiempoOn","concatenar"]
argNumber = [1,2,0,1,2,1,1,2,1,1,0,1]
#cantidad maxima de argumentos

def caller(command):
    argErrorFlag = True #Solo se activa si la cantidad de parametros es incorrecta
    out = 'ERROR: command not found or subprocess failed'
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
                argErrorFlag = False
        if argErrorFlag: print("ERROR: argument quantity mismatch")
    else:
        #print(command) 
        try:
            if command[0]=="cd":
                cd(command)
            else:
                out=subprocess.run(command) #passthrough
                print("passtrhough ok")
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
