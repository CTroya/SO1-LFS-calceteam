import os
import socket
from comandos import *
from resources import bcolors
import getpass
import rlcompleter, readline
readline.parse_and_bind("tab: complete")
user = getpass.getuser()
def main():
    #foundCommand = False
    #print(f.readlines())
    

    #NUEVO MOD
    while 1:

        user = getpass.getuser()
        c = input(bcolors.OKGREEN+bcolors.BOLD+str(user)+"@"
        +socket.gethostname()+bcolors.ENDC+":"+bcolors.HEADER+str(os.getcwd())+bcolors.ENDC+"$ ")
        #print(c) #Debug
        c = c.split(" ")
        caller(c)

        
    return 0

# la idea es usar un diccionario asi no tengo que usar estos if-elif xD
#tambien tenemos que evitar que nuestros comandos borren nuestros scripts uwu

if __name__ == "__main__":
    main()