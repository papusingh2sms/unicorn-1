#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, sender):
        self.sender = sender
        self.badges = badges()

        self.name = "rickroll"
        self.description = "Rickroll."
        self.usage = "Usage: rickroll"
        self.type = "trolling"
        self.args = 1

    def run(self, cmd_data):
        self.sender.send_command("openurl", "https://www.youtube.com/watch?v=oHg5SJYRHA0", False)
        print(self.badges.S + "Target has been rickrolled!")