# calceshell: a Linux shell in Python

A command-line shell for Linux, written in Python with `cmd2`. The commands have Spanish names. The shell logs each command that a user types.

Course project for Operating Systems 1 at Universidad Católica (UCA). Team: Fernando Caballero, Carlos Troya and Alain Vega.

## Features

- Command history and tab completion.
- User management: add a user, change a password, log in as root.
- File management: copy, move, list, change permissions and change the owner.
- Daemon control: start, stop, restart and list daemons.
- FTP client.
- Logs in `/var/log/shell/`: user commands, system errors and FTP transfers.

## Commands

| Command | Use | Action |
|---|---|---|
| `ir` | `ir [dst]` | Change the working directory. |
| `listar` | `listar [dir]` | List a directory. |
| `copiar` | `copiar src dst` | Copy a file or a directory. |
| `mover` | `mover src dst` | Move a file. |
| `creadir` | `creadir dir` | Make a directory. |
| `permiso` | `permiso mode file` | Change the permissions of a file. |
| `dueno` | `dueno file usr` | Change the owner of a file. |
| `usuario` | `usuario usr` | Add a user. |
| `clave` | `clave usr` | Change the password of a user. |
| `super` | `super` | Log in as root. |
| `controlsys` | `controlsys cmd [daemon ...]` | Start, stop, restart or list daemons. |
| `miftp` | `miftp ip [port]` | Connect to an FTP server. |
| `tiempoEncendido` | `tiempoEncendido` | Show the system uptime. |
| `limpiar` | `limpiar` | Clear the screen. |
| `salir` | `salir` | Close the shell. |

## Stack

Python, `cmd2`, `psutil`, `readline`, `ftplib`, `logging`.

## Run it

The shell writes logs to `/var/log/shell/`. Make this directory before you start the shell.

```sh
sudo mkdir -p /var/log/shell
pip install -r requirements.txt
sudo python3 calceshell.py
```
