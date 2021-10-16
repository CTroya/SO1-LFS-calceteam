def cp(origin, destiny):
    originFile = open(origin,"r")
    destinyFile = open(destiny,"a")
    destinyFile.write(str(originFile.read()))
    return 0
