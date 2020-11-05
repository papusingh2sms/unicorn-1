#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()

        self.name = "sysinfo"
        self.description = "Show system information."
        self.usage = "Usage: sysinfo"
        self.type = "managing"
        self.args = 1

    def run(self, cmd_data):
        print(self.unicorn.send_command(self.name))