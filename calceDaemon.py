import os
import sys
import time
import atexit
from signal import SIGTERM
import subprocess
import pathlib

def init_daemon_env():
    os.chdir('/')
    os.setsid()
    os.umask(0)


def exit_err(msg, status=1):
    print(msg)
    sys.exit(status)


def get_pid(pidfile, default=None):
    try:
        with open(pidfile) as pf:
            return int(pf.read().strip())
    except IOError:
        return default 

class Demonio(object):
    #pidfile va a ser el path al programa que se quiere hacer daemon puede ser scrip`t`
    def __init__(self, filename ,pidfile, arg,
                 stdin='/dev/null',
                 stdout='/dev/null',
                 stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.arg = arg
        self.filename = filename

    def daemonize(self):    
        #FORK 1
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            exit_err("fork #1 failed: %d (%s)" % (e.errnp, e.strerror))

        #DESACOPLE
        init_daemon_env()

        #FORK2
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            exit_err("fork #2 failed: %d (%s)" % (e.errnp, e.strerror))

        #REDIRECCIÓN
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        #ESCRIBIR EL ARCHIVO PID
        #atexit.register(self.delpid)
        pid = str(os.getpid())

        with open("/tmp/"+self.filename+".pid", 'w+') as f:
            f.write(pid)
        print(pid)

    def delpid(self):
        os.remove(self.filename)

    def start(self):
        #ANTES DE INICIAR CORROBORA SI YA EXISTE EL ARCHIVO PID PARA SABER SI EL DEMONIO YA ESTA CORRIENDO
        
        if get_pid("/tmp/"+self.filename+".pid"):
            msg = "El archivo pid %s ya existe. El demonio ya está corriendo"
            exit_err(msg % self.pidfile)

        self.daemonize()
        self.run()

    def stop(self):
        pid = get_pid("/tmp/"+self.filename+".pid")
        if not pid:
            msg = "El archivo pid %s no existe. El demonio no está corriendo"
            print(msg % self.pidfile)
            return    # not an error in a restart

        try:
            while True:
                os.kill(pid, SIGTERM) #se envia la señal de terminación del proceso
                time.sleep(0.1)
        except OSError as e:
            error = e.strerror  
            if 'No such process' in error:                                          #si no se encuentra el archivo pide del proceso activo
                if os.path.exists("/tmp/"+self.filename+".pid"):   #se verifica si el archivo .pid existe
                    os.remove("/tmp/"+self.filename+".pid")        #y se elimina
            else:
                exit_err(error)             #log del error

    def restart(self):
        self.stop()
        self.start()         

    #función principal del demonio se agrega lo que se desea que el demonio realice
    def run(self):        
        raise NotImplementedError

class midemonio(Demonio):
    def run(self):
        try:
            #cmd=[self.pidfile,self.pidfile]
            cmd=[self.pidfile]+self.arg
            os.execvp(cmd[0],cmd)
        except OSError as e:
            print(e)
        
         
if __name__ == '__main__':

    #print(sys.argv)
    if len(sys.argv) >= 3:        #calcedaemon.py start path arg1 arg2 arg3        
        filepath=os.path.abspath(os.path.expanduser(sys.argv[2]))
        print(filepath) 
        filename=pathlib.Path(filepath).name
        print(filename)       
        print(sys.argv[3:])
        daemon = midemonio(filename,filepath,sys.argv[3:])
        if 'start' == sys.argv[1]:             
            daemon.start()
        elif 'stop' == sys.argv[1]:           
            daemon.stop()
        elif 'restart' == sys.argv[1]:            
            daemon.restart()
        else:
            print("Comando desconocido")
            sys.exit(2)
        #sys.exit(0)
    else:
        print("modo de uso: %s start|stop|restart nombre_del_demonio" % sys.argv[0])
        #sys.exit(2)