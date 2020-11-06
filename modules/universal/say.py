#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()

        self.name = "say"
        self.description = "Say message on device."
        self.usage = "Usage: say <message>"
        self.type = "trolling"
        self.args = 2

    def run(self, cmd_data):
        if self.unicorn.send_command(self.name, cmd_data) == "success":
            print(self.badges.S + "Done saying message!")
        else:
            print(self.badges.E + "Failed to say message!")
