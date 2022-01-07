#!/usr/bin/python3
import os
from time import sleep
import socket
from comandos import *
from resources import bcolors
import getpass
import rlcompleter, readline
import logging
import pwd
import socket 

def setup_logger(name, log_file, toStdout, level=logging.INFO):
    #Se crean los controladores del formato
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')   
    formatterstd = logging.Formatter('%(message)s')
    #los manejadores de los archivos
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    #instanciacion del logger y se asigna el level a partir del cual loguean los mensajes por default INFO
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if toStdout: #si se activa la bandera para printear en el std.out
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(formatterstd)
        logger.addHandler(consoleHandler)
    logger.addHandler(handler)        
    return logger

readline.parse_and_bind("tab: complete")
def main():
    #Creacion del logger para entrada y salida de usuarios con el control de horario
    userLogger=setup_logger('usrLog', os.path.expanduser('/var/log/shell/usuario_horarios.log'), False)

    #IP del host
    hostname = socket.gethostname()    
    IPAddr = socket.gethostbyname(hostname)   
    #se obtienen los valores del GECOS
    entry = pwd.getpwuid(os.getuid())
    usergecos=entry.pw_gecos
    print(usergecos)
    #se separa la hora de inicio y fin y se almacena en una lista
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
            userLogger.warning(f"El usuario {getpass.getuser()} realiza loggin fuera de su horario normal desde la IP:{IPAddr}")
            print("Se reportará login fuera del horario")#sino se reporta (mandar a un log)
    else:
        userLogger.info(f"El usuario {getpass.getuser()} realiza loggin, sin horario de trabajo definido, desde la IP:{IPAddr}")
        print("Hora de trabajo no establecida")


    #CREACION DEL LOGGER DE MOVIMIENTOS DEL USUARIO
    movimientoLogger = setup_logger('cmdLog', os.path.expanduser('/var/log/shell/movimientos_usuarios.log'), False)
    while 1:
        user = getpass.getuser()
        c = input(bcolors.OKGREEN+bcolors.BOLD+str(user)+"@"
        +socket.gethostname()+bcolors.ENDC+":"+bcolors.HEADER+str(os.getcwd())+bcolors.ENDC+"$ ")
        #print(c) #Debug
        c = c.split(" ")
        #Se loguea cada comando que ejecuta el usuario
        movimientoLogger.info(c)
        #se envia los comandos para ejecución
        try:
            caller(c)
        except:
            print("caller error")
            
    #se realiza el loggin de salida del usuario
    #userLogger.info(f"El usuario {getpass.getuser()} ha finalizado sesion desde la IP:{IPAddr}")
    return 0

if __name__ == "__main__":

    #CREACION DE LOS ARCHIVOS Y CARPETAS NECESARIOAS PARA LOG Y DAEMONS
    if not os.path.exists('/var/log/shell'):
        print("Se requieren premisos para crear archivos de log de la shell:")
        os.system('sudo mkdir /var/log/shell')
        os.system('sudo touch /var/log/shell/usuario_horarios.log')
        os.system('sudo touch /var/log/shell/shell_transferencias.log')
        os.system('sudo touch /var/log/shell/movimientos_usuarios.log')
        os.system('sudo touch /var/log/shell/sistema_error.log')
        #Sacrilegio mode on:
        os.system('sudo chmod 774 -R /var/log/shell') #crear grupo y añadir usuarios  que necesiten usar la shell 755

    if not os.path.exists('/tmp/calcedaemon'):    
        os.system('sudo mkdir /tmp/calcedaemon')
        os.system('sudo chown root:calceshell -R /tmp/calcedaemon')
        os.system('sudo chmod 774 -R /tmp/calcedaemon')

    main()
