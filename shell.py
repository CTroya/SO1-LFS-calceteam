import os
import socket
from comandos import *
from resources import bcolors
import getpass

def main():
    #foundCommand = False
    #print(f.readlines())
    try:
        user = getpass.getuser()
        password = getpass.getpass()
    except Exception as error:
        print('ERROR', error)
    while 1:
        c = input(bcolors.OKGREEN+bcolors.BOLD+str(user)+"@"
        +socket.gethostname()+bcolors.ENDC+":"+bcolors.HEADER+str(os.getcwd())+bcolors.ENDC+"$ ")
        c = c.split()
        caller(c)
                
        
    return 0

# la idea es usar un diccionario asi no tengo que usar estos if-elif xD
#tambien tenemos que evitar que nuestros comandos borren nuestros scripts uwu

if __name__ == "__main__":
    main()