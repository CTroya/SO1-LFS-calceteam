from genericpath import isdir, isfile
from pathlib import Path
import os
from posix import listdir
import subprocess
import shutil
import shell
import getpass
import hashlib
import psutil
from time import *
import sys
import resources
import getpass
from ftplib import FTP

def password(command):
    if os.getuid() != 0: return 1
    paths = ["/etc/shadow","/etc/passwd"]
    userName = input("keusuariokerescambiarXDDD: ")
    userColumnShadow = 0
    userColumnPasswd = 0
    #0:shadow 1:passwd
    fileStrings = [0,0]
    fileAttributes = [0,0]
    #0:readlines 1:processedTexts
    #print(fileStrings[0])
    shutil.copy(paths[0],os.getcwd())
    shutil.copy(paths[1],os.getcwd())
    for i in range(2):
        fileStrings[i] = resources.readFile(paths[i])
        fileAttributes[i] = resources.processText(fileStrings[i])
    for i in range(len(fileAttributes[0])):
        if fileAttributes[0][i][0] == userName:
            userColumnShadow = i
    for i in range(len(fileAttributes[1])):
        #print(fileTexts[1][1][i][0])
        if fileAttributes[1][i][0] == userName:
            userColumnPasswd = i
    if userColumnShadow == 0 or userColumnPasswd == 0:
        print("kp no existis :v")
        return 1
    userPassword = getpass.getpass()
    newHash = f"$6${hashlib.sha512(str(userPassword).encode('utf-8')).hexdigest()}"
    fileStrings[0][userColumnShadow] = f"{userName}:{newHash}:{fileAttributes[0][userColumnShadow][2]}:{fileAttributes[0][userColumnShadow][3]}:{fileAttributes[0][userColumnShadow][4]}:{fileAttributes[0][userColumnShadow][5]}:::"
    fileStrings[1][userColumnPasswd] = f"{userName}:x:{fileAttributes[1][userColumnPasswd][2]}:{fileAttributes[1][userColumnPasswd][3]}:{fileAttributes[1][userColumnPasswd][4]}:{fileAttributes[1][userColumnPasswd][5]}:{fileAttributes[1][userColumnPasswd][6]}"
    #print(fileTexts[0][1][userColumnShadow][1])
    for i in range(len(fileStrings[0])):
        print(fileStrings[0][i])
    print("===================================================")
    for i in range(len(fileAttributes[1])):
        print(fileStrings[1][i])
    #print(newHash)
    passwdFalso = open("passwdFake","w+")
    for i in range(len(fileStrings[1])):
        passwdFalso.write(fileStrings[1][i])
        passwdFalso.write("\n")
    shadowFalso = open("shadowFake","w+")

    for i in range(len(fileStrings[0])):    
        shadowFalso.write(fileStrings[0][i])
        shadowFalso.write("\n")
    return 0

def adduser(command):
    if getpass.getuser() != 'root': 
        print("ERROR: You dont posses the required permissions to execute this command")
        return 1    
    if len(command) != 2:
        print("ERROR: argument quantity mismatch")
        return 1

    userName = command[1]
    paths = ["/etc/shadow","/etc/passwd","/etc/group"]
    files = []
    for i in paths:
        files.append(resources.readFile(i))
    for i in range(3):
        files[i] = resources.processText(files[i])
    #Verificacion de usuario ya existente
    for i in range(len(files[2])):
        print(files[2][i])
        if files[2][i][0] == userName:
            print(f"{userName} already exists. Exiting...")
            return 1
    userID = resources.getNewUserID()
    groupID = resources.getNewGroupID()
    homePath = f"/home/{userName}"
    if(os.path.exists(homePath) == False):
        os.mkdir(homePath,int('755',8))
    for i in range(3):
        files[i] = open(paths[i],"a+")
    files[0].write(f"{userName}:!:{int(time()/86400)}:0:99999:7:::\n")
    files[1].write(f"{userName}:!:{userID}:{groupID}:xd,,,:{homePath}:/bin/bash\n")
    files[2].write(f"{userName}:x:{groupID}:\n")
    print(f"Se añadio el usuario {userName} al sistema")
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
def clear(command):
    print("\033[H\033[J", end="")
    return 0    
def cd(command):
    path = command[1]
    try:
        print(os.path.abspath(path))
        os.chdir(os.path.abspath(path))
    except:
        print("ERROR: Not a valid path")
    return 0

#NUEVO MOD    
def cp(command):
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
def ftp(command):
    conectado=False
    ftp = FTP()
    usuario=input("Usuario:")
    contrase=input("Pass:")
    #Se espera cmd iphost user password
    try:
        ftp.connect("127.0.0.1",21)
        print("conect")
        ftp.login(usuario,contrase)
        print(ftp.getwelcome())
        conectado=True
    except Exception as er:
        print(er)
    while conectado:
        cmd=input("ftp> ")
        if cmd == "listar":
            ftp.dir()
        elif cmd == "salir":
            conectado=False
        elif cmd == "limpiar":
            print("\033[H\033[J", end="")
        elif cmd == "directorio":
            print(ftp.pwd())
        elif "descargar " in cmd:
            cmd = cmd[10:]
            try:
                archivos=ftp.nlst()
            except Exception as er:
                print(er)
                break
            if cmd in archivos:
                #descargar archivo
                print("Descargando el archivo "+cmd)
                try:
                    ftp.retrbinary("RETR " + cmd ,open(cmd, 'wb').write)
                except:
                    print("Error al descargar el archivo")
            else:
                print("Error no se encuentra el archivo")
        else:
            print("Error: "+cmd+" no valido")
    try:
        ftp.quit()
    except Exception as er1:
        print(er1)
def chown(command):
    #formato cmd user file
    archivo=Path(command[2])
    #COmprobar si existe el archivo o directorio
    try:
        #Verificar si existe el usuario que se pasa
       shutil.chown(archivo,command[1],command[1])
    except Exception as er:       
        print(er)
    return 0
          
def root(command):
    #es una herramienta que usaremos mas tarde V:
    #args = ['sudo', sys.executable] + sys.argv + [os.environ]
    file_path = os.path.dirname(__file__)
    #print(file_path)
    proc = subprocess.call(['sudo',sys.executable,file_path+"/shell.py"])
    return 0
def exitT(command):
    sys.exit()
    return 0
def daemon(command):
    pidFilePath = "/home/ctroya/Documents/SO1-LFS-calceteam/pidDaemon"
    if len(command) - 1 == 0:
        pidFile = resources.readFile(pidFilePath)
        print(*pidFile,sep="\n")
        return 1
    graciasmathiuwu = ' '.join(command)
    os.system("sudo python3 daemon.py " + graciasmathiuwu)
    return 0
commandFunction = [cd,cp,clear,pmod,mv,ls,mkdir,rename,adduser,password,uptime,cat,daemon,ftp,chown,root,exitT]
commandList = ["ir", "copiar", "limpiar","permisos","mover","listar","crearDir","renombrar","addUsuario","contrasena","tiempoOn","concatenar","controlSys","clientFtp","propietario","super","salir"]
argNumber = [[1],[2],[0],[1],[2],[1,0],[1],[2],[1],[0],[0],[1],[x for x in range(100)],[0],[2],[0],[0]]
#cantidad maxima de argumentos
def caller(command):
    argErrorFlag = True #Solo se activa si la cantidad de parametros es incorrecta
    out = resources.bcolors.FAIL+'ERROR:'+resources.bcolors.WARNING+'command not found or subprocess failed'+resources.bcolors.ENDC
    foundCommand = False
    argc = len(command) - 1
    commandCounter = len(commandFunction)
    #print(f"commandFunctionLen: {len(commandFunction)}") #PARA DEBUG
    #print(f"commandListLen: {len(commandList)}")
    #print(f"argNumberLen: {len(argNumber)}")
    #print(f"argc: {argc}")
    for i in commandList:
            if(command[0] == i):
                foundCommand = True
    if(foundCommand):
        for i in range(commandCounter):
                for j in range(len(argNumber[i])):
                    if(command[0] == commandList[i] and argc == argNumber[i][j]):
                        commandFunction[i](command)
                        argErrorFlag = False
        if argErrorFlag: print(resources.bcolors.FAIL+"ERROR: argument quantity mismatch"+resources.bcolors.ENDC)
    else:
        #print(command) 
        try:
            if command[0]=="cd":
                cd(command)
            else:
                out=subprocess.run(command) #passthrough
        except:
            print(out)
    return 0
