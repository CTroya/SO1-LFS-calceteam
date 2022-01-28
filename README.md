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
Modo de uso: ir [dst] <br />

Argumentos: <br />
  dst          Ruta al nuevo directorio de trabajo

### listar
Modo de uso: listar [dir] <br />

Argumentos: <br />
  dir         Ruta al directorio a listar

## mover
Modo de uso: mover src dst <br />

Argumentos: <br /> 
  src         Archivo que se quiere mover <br />
  dst         Ruta al directorio al cual se quiere mover

## Salir 
Modo de uso: salir <br />
Cierra la shell

## tiempoEncendido
Modo de uso: tiempoEncendido <br />
Imprime en pantalla el tiempo que el sistema estuvo encendido

### clave
Modo de uso: clave usr <br />

Argumentos: <br />
  usr         Nombre del usuario al cual cambiar la contraseña

### copiar
Modo de uso: copiar src dst <br />

Argumentos: <br />
  src         El archivo o directorio fuente <br />
  dst         El archivo o directorio destino

## dueno
Modo de uso: dueno file usr <br />

Argumentos: <br />
  file        Ruta al archivo o directorio que se quiere cambiar de dueño <br />
  usr         Nombre de usuario del nuevo dueño

## limpiar
Limpia los caracteres de salida de la terminal <br /> <br />
Modo de uso: limpiar <br />

## super 
Accede al modo root

### usuario
Modo de uso: usuario usr

Argumentos: <br />
  usr         Nombre del usuario a añadir

### controlsys
Modo de uso: controlsys  cmd [daemon [...]]

Argumentos:
  cmd         Ingrese la accion a realizar sobre los demonios start|stop|restart|list <br />
  daemon      Ingrese el nombre del programa que quiere demonizar! debe estar marcado como 
  
### miftp
Modo de uso: miftp ip [port]

Argumentos: <br />
  ip          Introduzca la IP del servidor FTP al cual se quiere conectar <br />
  port        Introduzca el puerto que utiliza el servidor por defecto 2

### permiso
Modo de uso: permiso mode file

Argumentos: <br />
  mode        Permisos que se asignaran <br />
  file        Archivo o directorio al cual se le quiere modificar los permisos

### super
Modo de uso: super <br />
Log-in al usuario root 

### usuario
Modo de uso: usuario  usr <br />

Argumentos: <br />
  usr         nombre del usuario
