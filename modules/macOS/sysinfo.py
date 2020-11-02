#!/usr/bin/env python3

from core.badges import badges
from core.transfer import transfer

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.unicorn = unicorn_handler
        self.transfer = transfer(self.unicorn)
        self.badges = badges()

        self.name = "sysinfo"
        self.description = "Show system information."
        self.usage = "Usage: sysinfo"
        self.type = "managing"
        self.args = 1

    def run(self, cmd_data):
        sended_command = []
        sended_command.append("sysinfo")

        self.unicorn.send(str(sended_command).encode("UTF-8"))
        print(self.unicorn.recv().strip().decode("UTF-8", "ignore"))