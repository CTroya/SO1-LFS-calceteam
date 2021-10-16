from os import close
from comandos import *

def main():
    #print(f.readlines())
    while 1:
        a = input("~$ ")
        tokens  = a.split()
        argQuant = len(tokens)
        #print(a.split())
        if a == "exit":
            break
        elif tokens[0] == 'cp':
            try:
                cp(tokens[1],tokens[2])
            except:
                print("cp: bobito no sabes usar tu comando")
        else:
            print("\""+str(a)+"\" : command not found")
    return 0

# la idea es usar un diccionario asi no tengo que usar estos if-elif xD
#tambien tenemos que evitar que nuestros comandos borren nuestros scripts uwu

if __name__ == "__main__":
    main()