#!/usr/bin/env python3

from core.badges import badges
from core.sender import sender

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.sender = sender(unicorn_handler)
        self.badges = badges()

        self.name = "pwd"
        self.description = "Show current working directory."
        self.usage = "Usage: pwd"
        self.type = "managing"
        self.args = 1

    def run(self, cmd_data):
        print(self.sender.send_command(self.name))