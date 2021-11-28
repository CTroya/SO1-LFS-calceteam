import os
from time import sleep
import socket
from comandos import *
from resources import bcolors
import getpass
import rlcompleter, readline
readline.parse_and_bind("tab: complete")
def main():
        while 1:
            user = getpass.getuser()
            c = input(bcolors.OKGREEN+bcolors.BOLD+str(user)+"@"
            +socket.gethostname()+bcolors.ENDC+":"+bcolors.HEADER+str(os.getcwd())+bcolors.ENDC+"$ ")
            #print(c) #Debug
            c = c.split(" ")
            caller(c)
        return 0
if __name__ == "__main__":
    main()