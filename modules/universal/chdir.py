#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()

        self.name = "chdir"
        self.description = "Change current working directory."
        self.usage = "Usage: chdir <remote_path>"
        self.type = "managing"
        self.args = 2

    def run(self, cmd_data):
        print(self.unicorn.send_command(self.name, cmd_data))