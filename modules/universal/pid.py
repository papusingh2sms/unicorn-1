#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, sender):
        self.sender = sender
        self.badges = badges()

        self.name = "pid"
        self.description = "Show magic_unicorn payload PID."
        self.usage = "Usage: pid"
        self.type = "managing"
        self.args = 1

    def run(self, cmd_data):
        print(self.sender.send_command(self.name))