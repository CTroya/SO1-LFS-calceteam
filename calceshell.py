import cmd
from re import S, split
import cmd2 
from cmd2 import (
Bg,
Fg,
style,
)
from cmd2 import Cmd2ArgumentParser, with_argparser
from os.path import isdir, isfile
from pathlib import Path
import subprocess
import sys
import readline
import getpass
import os
import socket
import time
import shutil
import hashlib
import psutil
from ftplib import FTP
from time import *
import argparse
import resources
import calceDaemon
import pwd
import socket 

readline.parse_and_bind("tab: complete")


class calceshell(cmd2.Cmd):

    def __init__(self):
        super().__init__(multiline_commands=['orate'],allow_redirection=True)
        #SE PUEDE METER ESTOS DOS PARA TENER ARCHIVO DE HISTORIA Y SCRIPT PARA CONFIGURAR TIPO calceshell.rc
        #persistent_history_file='cmd2_history.dat',startup_script='scripts/startup.txt'
        self.default_to_shell = True
        self.intro = style('calceShell 2021 para SO1!', fg=Fg.RED, bg=Bg.BLACK, bold=True) + ' 😀📁📂🗃🗎🖻🖹🖿🗀🗁'
        self.prompt=prompt = getpass.getuser()+"@"+socket.gethostname()+":"+str(os.getcwd())+"$ \n>"
        

    def postcmd(self, stop: bool, line: str) -> bool: #FUNCION QUE SE EJECUTA LUEGO DE CADA COMANDO AQUI SE PUEDE HOOKEAR EL CAMBIO DE PROMPT!!!!!
        #wd=getpass.getuser()+"@"+socket.gethostname()+":"+str(os.getcwd())+"$ \n"
        #self.prompt = style('{!r} $ '.format(wd), fg = Fg.DARK_GRAY, bg = Bg.BLUE,bold=True) #para dejarle chururu
        self.prompt = getpass.getuser()+"@"+socket.gethostname()+":"+str(os.getcwd())+"$ \n>"       
        return stop


    claveParser = Cmd2ArgumentParser()
    claveParser.add_argument('usr',nargs=1,help="Nombre del usuario al cual cambiar la contraseña")
    def do_clave(self,opt):
        if os.getuid() != 0: 
            self.perror("No se tienen los permisos para realizar la operación")
            return
        paths = ["/etc/shadow","/etc/passwd"]
        userName = opt.usr[0]
        userColumnShadow = 0
        userColumnPasswd = 0
        #0:shadow 1:passwd
        fileStrings = [0,0]
        fileAttributes = [0,0]
        #0:readlines 1:processedTexts
        #print(fileStrings[0])
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
            self.poutput("No se encuentra el usuario especificado")
            return 
        userPassword = getpass.getpass()
        newHash = resources.hash512(userPassword)
        fileStrings[0][userColumnShadow] = f"{userName}:{newHash}:{fileAttributes[0][userColumnShadow][2]}:{fileAttributes[0][userColumnShadow][3]}:{fileAttributes[0][userColumnShadow][4]}:{fileAttributes[0][userColumnShadow][5]}:::"
        fileStrings[1][userColumnPasswd] = f"{userName}:x:{fileAttributes[1][userColumnPasswd][2]}:{fileAttributes[1][userColumnPasswd][3]}:{fileAttributes[1][userColumnPasswd][4]}:{fileAttributes[1][userColumnPasswd][5]}:{fileAttributes[1][userColumnPasswd][6]}"
        #print(fileTexts[0][1][userColumnShadow][1])
        #print(newHash)
        passwdFalso = open("/etc/passwd","w+")
        for i in range(len(fileStrings[1])):
            passwdFalso.write(fileStrings[1][i])
            passwdFalso.write("\n")

        shadowFalso = open("/etc/shadow","w+")
        for i in range(len(fileStrings[0])):    
            shadowFalso.write(fileStrings[0][i])
            shadowFalso.write("\n")
        self.poutput("Se actualizo la contraseña satisfactoriamente")
        return 


    usuarioParser=Cmd2ArgumentParser()
    usuarioParser.add_argument('usr',nargs=1,help='nombre del usuario')
    @with_argparser(usuarioParser)
    def do_usuario(self, opt):
        if getpass.getuser() != 'root': 
            self.perror("No posees los permisos necesarios para añadir usuarios")
            return    
        
        userName = opt.usr[0]
        paths = ["/etc/shadow","/etc/passwd","/etc/group"]
        files = []
        for i in paths:
            files.append(resources.readFile(i))
        for i in range(3):
            files[i] = resources.processText(files[i])
        #Verificacion de usuario ya existente
        for i in range(len(files[2])):
            #print(files[2][i])
            if files[2][i][0] == userName:
                self.perror(f"{userName} ya existe. Saliendo....")
                return
        #se obtienen los ID de usuario y grupo nuevos
        userID = resources.getNewUserID()
        groupID = resources.getNewGroupID()
        #Se crea el directorio HOME para el nuevo usuario
        homePath = f"/home/{userName}" 
        if(os.path.exists(homePath) == False):
            os.mkdir(homePath,int('755',8))
        #guardar datos personales
        self.poutput("Ingresa los valores:\n")
        fullname=input("Nombre Completo []: ")
        roomname=input("Numero de Habitación []: ")
        workphone=input("Teléfono del Trabajo []:")
        homephone=input("Teléfono de casa []: ")
        inihour=input("Horario de entrada HH:MM: ")
        inihour=inihour.replace(":","")
        finhour=input("Horario de salida HH:MM: ")
        finhour=finhour.replace(":","")
        for i in range(3):
            files[i] = open(paths[i],"a+")

        files[0].write(f"{userName}:!:{int(time()/86400)}:0:99999:7:::\n")
        files[1].write(f"{userName}:!:{userID}:{groupID}:{fullname} {roomname} {workphone} {homephone},{inihour},{finhour}:{homePath}:/bin/bash\n")
        files[2].write(f"{userName}:x:{groupID}:\n")

        #cerrar?
        self.poutput(f"Se añadio el usuario {userName} al sistema")
        return 

    permisoParser = Cmd2ArgumentParser()
    permisoParser.add_argument('mode',nargs=1,type=int,help='Permisos que se asignaran')
    permisoParser.add_argument('file',nargs=1,help="Archivo o directorio al cual se le quiere modificar los permisos")
    
    @with_argparser(permisoParser)
    def do_permiso(self, opt): 

        opt.file=os.path.abspath(os.path.expanduser(opt.file[0]))       
        try:
            os.chmod(opt.file,int(str(opt.mode[0]),base=8))
            self.poutput(f"Se actualizaron los permisos de {opt.file}")
        except Exception as er:
            self.perror(er)
        return 0

    def complete_permiso(self, text, line, begidx, endidx):
        return self.path_complete(text, line, begidx, endidx)



    creadirParser = Cmd2ArgumentParser()
    creadirParser.add_argument('dir',nargs=1,type=str,help='ruta en la cual crear el directorio nuevo')
    @with_argparser(creadirParser)
    def do_creadir(self, opt):
        direccion=os.path.abspath(os.path.expanduser(opt.dir[0]))        

        if os.path.exists(direccion):
            print(f"crearDir: cannot create directory ‘{direccion}’: File exists")
        else:
            os.mkdir(direccion)
        return 

    def complete_creadir(self, text, line, begidx, endidx):
        return self.path_complete(text, line, begidx, endidx)


    propietarioParser = Cmd2ArgumentParser()
    propietarioParser.add_argument('file',nargs=1,type=str,help='ruta al archivo o directorio que se quiere cambiar de dueño')
    propietarioParser.add_argument('usr',nargs=1,type=str,help='nombre de usuario del nuevo dueño')
    @with_argparser(propietarioParser)
    def do_dueno(self,opt):
        #formato cmd user file
        archivo=os.path.abspath(os.path.expanduser(opt.file[0]))
        
        usuario=opt.usr[0]
        #COmprobar si existe el archivo o directorio
        try:
            #Verificar si existe el usuario que se pasa
            shutil.chown(archivo,usuario,usuario)   #nombre del archivo, usuario , grupo
        except Exception as er:       
            self.perror(er)
        return 0
            

    def do_miftp(self,opt):
        conectado=False
        ftp = FTP()
        usuario=input("Usuario:")
        contrase=input("Pass:")
        #Se espera cmd ipdelhost user password
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
            elif "cargar " in cmd:
                cmd = cmd[7:]
                if isfile(cmd):#comprobamos si es un archivo
                    try:
                        archivo=open(cmd,'rb')
                        nombreArchivo=input("Ingrese nombre para guardar el archivo: ")#falta comprobar que no tenga espacios etc
                        ftp.storbinary('STOR '+nombreArchivo, archivo)#cargar el archivo
                        archivo.close()                    
                    except:
                        print("Error al abrir el archivo")
                        break
                else:
                    print("Error no es un archivo")
                    return 0
                
            else:
                print("Error: "+cmd+" no valido")
        try:
            ftp.quit()
        except Exception as er1:
            print(er1)



    moverParser = Cmd2ArgumentParser()
    moverParser.add_argument('src',nargs=1,help='Archivo que se quiere mover')
    moverParser.add_argument('dst',nargs=1,help='Directorio al cual se quiere mover')

    @with_argparser(moverParser)
    def do_mover(self, opt):
        #Se normalizan las direcciones antes de trabajar
        origin = os.path.abspath(os.path.expanduser(opt.src[0]))
        destiny = os.path.abspath(os.path.expanduser(opt.dst[0]))
        if not isdir(destiny):
            self.perror(f"{destiny} no es un directorio válido para mover el archivo")
            return
        elif not os.access(destiny,os.R_OK):
            self.perror(f"No se tiene los permisos necesarios para acceder a {destiny}")
            return 
        else:           
            try:
                shutil.move(origin,destiny)
                self.poutput(f"Se movio {opt.src[0]} a {opt.dst[0]}")
            except Exception as er:
                self.perror(er)
        return 

    def complete_mover(self, text, line, begidx, endidx):
        return self.path_complete(text, line, begidx, endidx)

    irParser = Cmd2ArgumentParser()
    irParser.add_argument('dst', nargs='?', default=" ",help='Directorio al cual se quiere ir, para subir un ..')
    @with_argparser(irParser)
    def do_ir(self,dest): 
        #print(dest.dst[0])
       
        #si se pone sin argumentos
        if dest.dst == " ":            
            os.chdir(os.path.expanduser("~")) #ir al directorio $HOME del usuario
        else:
            
            dest.dst=os.path.abspath(os.path.expanduser(dest.dst))
            #print(dest.dst)
            if not isdir(dest.dst):
                self.perror("No es un directorio valido")
                return
                
            elif not os.access(dest.dst,  os.R_OK):
                self.perror("No se tiene acceso de lectura al directorio")
                return

            else:
                try:
                    os.chdir(dest.dst)
                except Exception as ex:
                    self.perror(ex)
            
        return

    # Enable tab completion for cd command
    def complete_ir(self, text, line, begidx, endidx):
        return self.path_complete(text, line, begidx, endidx)



    def do_limpiar(self, line):
        #print("\033[H\033[J", end="")
        self.poutput("\033[H\033[J", end="")


    def do_salir(self, line):        
        self.poutput("Bye")
        return True

    def do_super(self, line):
        #es una herramienta que usaremos mas tarde V:        
        file_path = os.path.dirname(__file__)
        self.poutput(sys.executable)
        proc = subprocess.call(['sudo',sys.executable,file_path+"/calceshell.py"])
        return 0

    do_cd=do_ir  #cd es interno de la shell y un proceso no puede cambiar el cwd de otro proceso

    listarParser = Cmd2ArgumentParser()
    listarParser.add_argument('dir', nargs='?',default=" ", help='ruta al directorio')

    @with_argparser(listarParser)
    def do_listar(self, opt):
        #fix por si se meta la virgula :V
        opt.dir=os.path.expanduser(opt.dir) 
        #print(os.path.abspath(opt.dir))
        if opt.dir==" ":            
            archivos = os.listdir(os.getcwd())
            for f in archivos:
                if isdir(f):
                    self.stdout.write('📂 '+f)
                else:
                    self.stdout.write('🗃 '+f)
                self.stdout.write("    ")
        else:
            if isfile(opt.dir):
                self.perror("La ruta especificada no es un directorio válido o el directorio no existe")
                return
        #lista los archivos y directorios correspondientes a la ruta especificada           
            archivos = os.listdir(os.path.abspath(opt.dir))
            for f in archivos:
                #print(os.path.abspath(opt.dir))                
                if isdir((os.path.abspath(opt.dir))+"/"+f): 
                    self.stdout.write('📂 '+f)
                else:
                    self.stdout.write('🗃 '+f)
                self.stdout.write("    ")  
                  
        self.stdout.write("\n")    
        return

    def complete_listar(self, text, line, begidx, endidx):
        return self.path_complete(text, line, begidx, endidx)

    def do_tiempoEncendido(self, line):       
        tiempo=strftime("%H:%M:%S", gmtime())
        tiempoon=strftime("%Hh%Mm", gmtime(round(time()-psutil.boot_time())))
        usuariosOn=len(psutil.users())
        load1, load5, load15 = os.getloadavg()
        self.poutput(f"{tiempo} up {tiempoon}, {usuariosOn} usuarios, carga promedio: {load1}, {load5}, {load15}")

        return



    copiarparser = Cmd2ArgumentParser()
    #copiarparser.add_argument('files', nargs=2, help='copiar $src $dst, copiar el archivo/directorio src al directorio dst')
    copiarparser.add_argument('src',nargs=1,type=str,help='El archivo o directorio fuente')
    copiarparser.add_argument('dst',nargs=1,type=str,help='El archivo o directorio destino')
    @with_argparser(copiarparser)
    def do_copiar(self, opt):
        
        #if isdir(str(opt.src)):
        opt.src=os.path.abspath(os.path.expanduser(opt.src[0]))
        #if isdir(str(opt.dst)):
        opt.dst=os.path.abspath(os.path.expanduser(opt.dst[0]))
        #opt.dst=os.path.abspath(os.path.expanduser(opt.dst))
        print(opt.src)
        print(opt.dst)

        if not os.path.exists(opt.src):
            self.perror("ALV no se puede copiar algo que no existe :V")
                
        # origin = os.path.join(os.getcwd(),command[1])
        # destiny = os.path.join(os.getcwd(),command[2])
        #try:
        if isdir(opt.src):
            shutil.copytree(opt.src,opt.dst,dirs_exist_ok=True)
            self.poutput(f"Se copio el directorio {os.path.basename(opt.src)} a {opt.dst}")
        else:        
            shutil.copy(opt.src,opt.dst)
            self.poutput(f"Se copio el archivo {os.path.basename(opt.src)} a {opt.dst}")
        #except:
            #self.perror("No se pudo realizar la copia")
        return
    def complete_copiar(self, text, line, begidx, endidx):
        return self.path_complete(text, line, begidx, endidx)

    controlsysParser=Cmd2ArgumentParser()
    controlsysParser.add_argument('cmd',nargs=1,type=str, help='llala') #corroborar que sea comando:V
    controlsysParser.add_argument('daemon',nargs=1, help='llalaa') #opcional revisar
    @with_argparser(controlsysParser)
    def do_controlsys(self,opt):
        command=opt.cmd[0]        
        demonio=opt.daemon[0]
        if command == 'start':
            os.system("python3 calceDaemon.py start "+demonio)
            
        elif command == 'stop': 
            os.system("python3 calceDaemon.py stop "+demonio)           
            
        elif command == 'restart':  
            os.system("python3 calceDaemon.py restart "+demonio)          
            
        else:
            print("Comando no reconocido")
            return
         

if __name__ == '__main__':
    
    hostname = socket.gethostname()    
    IPAddr = socket.gethostbyname(hostname)    
    print(IPAddr)
    #Se carga los datos de los campos GECOS del usuario actual que loguea
    entry = pwd.getpwuid(os.getuid())
    usergecos=entry.pw_gecos
    print(usergecos)
    usergecos=usergecos.split(",")
    #Se comprueba que existan al menos 3 valores cargados 1 estandar 2 opcionales correspondientes a VAL,hora de inicio laboral, hora de salida laboral
    if len(usergecos)==3:
        mintime=int(usergecos[1])
        maxtime=int(usergecos[2])
        print(mintime,maxtime)
        actual=int(strftime("%H%M", gmtime()))
        if (actual>=mintime and actual<=maxtime): #se comprueba que el horario de login este en regla con el horario de trabajo
            print("OK hora normal de trabajo")
        else:
            print("Se reportará login fuera del horario")#sino se reporta (mandar a un log)
    else:
        print("Hora de trabajo no definida")

    
    shell=calceshell()
    sys.exit(shell.cmdloop())
    