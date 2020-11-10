#!/usr/bin/env python3

from core.badges import badges
from core.keyboard import keyboard

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()
        
        self.keyboard = keyboard()
        
        self.name = "pasteboard"
        self.description = "Control device pasteboard."
        self.usage = "Usage: pasteboard [read|write <value>]"
        self.type = "managing"
        self.args = 2
        
    def run(self, cmd_data):
        if cmd_data == "read":
            print(self.unicorn.send_command("shell", "pbpaste"))
        else if cmd_data == "write":
            if len(cmd_data.split(" ")) < 2:
                print(self.usage)
            else:
                self.unicorn.send_command("shell", "echo \""+cmd_data.split("write")[1].strip()+"\" | pbcopy", False)
        else:
            print(self.usage)
