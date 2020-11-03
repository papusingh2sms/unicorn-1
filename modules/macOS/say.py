#!/usr/bin/env python3

from core.badges import badges
from core.sender import sender

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.sender = sender(unicorn_handler)
        self.badges = badges()

        self.name = "say"
        self.description = "Say message."
        self.usage = "Usage: say <message>"
        self.type = "trolling"
        self.args = 2

    def run(self, cmd_data):
        if self.sender.send_command(self.name, cmd_data) == "success":
            print(self.badges.S + "Done saying message!")
        else:
            print(self.badges.E + "Failed to say message!")