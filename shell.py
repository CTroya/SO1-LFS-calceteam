from os import close
from os import system
from comandos import *

def main():
    foundCommand = False
    #print(f.readlines())
    while 1:
        a = input("~$ ")
        tokens  = a.split()
        argQuant = len(tokens)
        #print(a.split())
        for i in commandList: #esto en principio detecta si el usuario ingresa un comando de linux
            if(tokens[0] == i):
                foundCommand = True
        if foundCommand == True:
            system(a)
        else:
            if a == "exit":
                break
            elif tokens[0] == 'calcecp':
                try:
                    cp(tokens[1],tokens[2])
                except:
                    print("calcecp: bobito no sabes usar tu comando")
            else:
                print("\""+str(a)+"\" : command not found")
    return 0

# la idea es usar un diccionario asi no tengo que usar estos if-elif xD
#tambien tenemos que evitar que nuestros comandos borren nuestros scripts uwu

if __name__ == "__main__":
    main()