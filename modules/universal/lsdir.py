#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()

        self.name = "lsdir"
        self.description = "List contents of directory."
        self.usage = "Usage: lsdir <remote_path>"
        self.type = "managing"
        self.args = 1

    def run(self, cmd_data):
        if cmd_data == "":
            print(self.unicorn.send_command(self.name, "."))
        else:
            print(self.unicorn.send_command(self.name, cmd_data))
