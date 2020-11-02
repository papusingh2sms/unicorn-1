#!/usr/bin/env python3

from core.badges import badges
from core.transfer import transfer

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.unicorn = unicorn_handler
        self.transfer = transfer(self.unicorn)
        self.badges = badges()

        self.name = "chdir"
        self.description = "Change current working directory."
        self.usage = "Usage: chdir <remote_path>"
        self.type = "managing"
        self.args = 2

    def run(self, cmd_data):
        sended_command = []
        sended_command.append("chdir")
        sended_command.append(cmd_data)

        self.unicorn.send(str(sended_command).encode("UTF-8"))
        print(self.unicorn.recv().strip().decode("UTF-8", "ignore"))