## Implementacion de shell para Linux mediante Python
### Integrantes
- 🙋‍♂️ Fernando Caballero
- 🙋‍♂️ Carlos Troya
- 🙋‍♂️ Alain Vega
## Features
 - Iconos
 - Historial de Comandos
 - Autocompletado

### Herramientas utilizadas
<img align="left" alt="Visual Studio Code" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/visual-studio-code/visual-studio-code.png" />
<img align="left" alt="Git" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/git/git.png" />
<img align="left" alt="GitHub" width="26px" src="https://raw.githubusercontent.com/github/explore/78df643247d429f6cc873026c0622819ad797942/topics/github/github.png" />
<img align="left" alt="Terminal" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/terminal/terminal.png" />
<img align="left" alt="Terminal" width="26px" src="https://i.pinimg.com/736x/2f/9c/11/2f9c11f9e55efbf1791f12c06d60729b.jpg" />
<br />
<br />

# Documentación
## ir
Usage: ir [dst] <br />

positional arguments: <br />
  dst         Directorio al cual se quiere ir, para subir un ..

### listar
Usage: listar [dir] <br />

positional arguments: <br />
  dir         Ruta al directorio

## mover
Usage: mover src dst <br />

positional arguments: <br /> 
  src         Archivo que se quiere mover <br />
  dst         Directorio al cual se quiere mover

## Salir 
Usage: salir <br />
Cierra la shell

## tiempoEncendido
Usage: tiempoEncendido <br />
Displays amount of time passed since the system was turned on

### clave
Usage: clave usr <br />

positional arguments: <br />
  usr         Nombre del usuario al cual cambiar la contraseña

### copiar
Usage: copiar src dst <br />

positional arguments: <br />
  src         El archivo o directorio fuente <br />
  dst         El archivo o directorio destino

## dueno
Usage: dueno file usr <br />

positional arguments: <br />
  file        Ruta al archivo o directorio que se quiere cambiar de dueño <br />
  usr         Nombre de usuario del nuevo dueño

## limpiar
Clears the terminal output <br /> <br />
Usage: permiso mode file <br />

## super 
Log-in to root mode

### usuario
Usage: usuario usr

positional arguments: <br />
  usr         Nombre del usuario a añadir

### controlsys
Usage: controlsys  cmd [daemon [...]]

positional arguments:
  cmd         Ingrese la accion a realizar sobre los demonios start|stop|restart|list <br />
  daemon      Ingrese el nombre del programa que quiere demonizar! debe estar marcado como 
  
### miftp
Usage: miftp ip [port]

positional arguments: <br />
  ip          Introduzca la IP del servidor FTP al cual se quiere conectar <br />
  port        Introduzca el puerto que utiliza el servidor por defecto 2

### permiso
Usage: permiso mode file

positional arguments: <br />
  mode        Permisos que se asignaran <br />
  file        Archivo o directorio al cual se le quiere modificar los permisos

### super
Usage: super <br />
Log-in al usuario root 

### usuario
Usage: usuario  usr <br />

positional arguments: <br />
  usr         nombre del usuario
