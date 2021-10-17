def pegarseUnTiro():
    f = open("comandos.txt","r")
    a = f.readlines()
    for i in range(len(a)):
        a[i] =''.join(a[i].split())
    print(a)
    return 69







def cp(origin, destiny): #tal vez tenga que cambiar el planteamiento
    originFile = open(origin,"r")
    destinyFile = open(destiny,"a")
    destinyFile.write(str(originFile.read()))
    return 0
    
commandList = ['&', 'alias', 'apropos', 'apt', 'apt-get', 'aptitude', 'aspell', 'at', 'awk', 'basename', 'base32', 'base64', 'bash', 'bc', 'bg', 'bind', 'break', 'builtin', 'bzip2', 'cal', 'caller', 'case', 'cat', 'cd','cp', 'cfdisk', 'chattr', 'chgrp', 'chmod', 'chown', 'chpasswd', 'chroot', 'chkconfig', 'cksum', 'clear', 'cmp', 'comm', 'command', 'continue', 'cp', 'cpio', 'cron', 'crontab', 'csplit', 'curl', 'cut', 'date', 'dc', 'dd', 'ddrescue', 'declare', 'df', 'diff', 'diff3', 'dig', 'dir', 'dircolors', 'dirname', 'dirs', 'dos2unix', 'dmesg', 'dpkg', 'du', 'echo', 'egrep', 'eject', 'enable', 'env', 'ethtool', 'eval', 'exec', 'exit', 'expect', 'expand', 'export', 'expr', 'false', 'fdformat', 'fdisk', 'fg', 'fgrep', 'file', 'find', 'fmt', 'fold', 'for', 'format', 'free', 'fsck', 'ftp', 'function', 'fuser', 'gawk', 'getopts', 'grep', 'groupadd', 'groupdel', 'groupmod', 'groups', 'gzip', 'hash', 'head', 'help', 'history', 'hostname', 'htop', 'iconv', 'id', 'if', 'ifconfig', 'ifdown', 'ifup', 'import', 'install', 'iostat', 'ip', 'jobs', 'join', 'kill', 'killall', 'less', 'let', 'link', 'ln', 'local', 'locate', 'logname', 'logout', 'look', 'lpc', 'lpr', 'lprint', 'lprintd', 'lprintq', 'lprm', 'lsattr', 'lsblk', 'ls', 'lsof', 'lspci', 'make', 'man', 'mapfile', 'mkdir', 'mkfifo', 'mkfile', 'mkisofs', 'mknod', 'mktemp', 'more', 'most', 'mount', 'mtools', 'mtr', 'mv', 'mmv', 'nc', 'netstat', 'nft', 'nice', 'nl', 'nohup', 'notify-send', 'nslookup', 'open', 'op', 'passwd', 'paste', 'pathchk', 'Perf', 'ping', 'pgrep', 'pkill', 'popd', 'pr', 'printcap', 'printenv', 'printf', 'ps', 'pushd', 'pv', 'pwd', 'quota', 'quotacheck', 'ram', 'rar', 'rcp', 'read', 'readarray', 'readonly', 'reboot', 'rename', 'renice', 'remsync', 'return', 'rev', 'rm', 'rmdir', 'rsync', 'screen', 'scp', 'sdiff', 'sed', 'select', 'seq', 'set', 'sftp', 'shift', 'shopt', 'shuf', 'shutdown', 'sleep', 'slocate', 'sort', 'source', 'split', 'ss', 'ssh', 'stat', 'strace', 'su', 'sudo', 'sum', 'suspend', 'sync', 'tail', 'tar', 'tee', 'test', 'time', 'timeout', 'times', 'tmux', 'touch', 'top', 'tput', 'traceroute', 'trap', 'tr', 'true', 'tsort', 'tty', 'type', 'ulimit', 'umask', 'umount', 'unalias', 'uname', 'unexpand', 'uniq', 'units', 'unix2dos', 'unrar', 'unset', 'unshar', 'until', 'uptime', 'useradd', 'userdel', 'usermod', 'users', 'uuencode', 'uudecode', 'v', 'vdir', 'vi', 'vmstat', 'w', 'wait', 'watch', 'wc', 'whereis', 'which', 'while', 'who', 'whoami', 'wget', 'write', 'xargs', 'xdg-open', 'xz', 'yes', 'zip', '.', '!!']