#!/usr/bin/env python3

from core.badges import badges
from core.transfer import transfer

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.unicorn = unicorn_handler
        self.transfer = transfer(self.unicorn)
        self.badges = badges()

        self.name = "screenshot"
        self.description = "Take screenshot."
        self.usage = "Usage: screenshot <output_path>"
        self.args = 2

    def run(self, cmd_data):
        print(self.badges.G + "Taking screenshot...")
        self.unicorn.send("screenshot".encode("UTF-8"))
        image = self.unicorn.recv()
        f = open(cmd_data, "wb")
        print(self.badges.G + "Saving to " + cmd_data + "...")
        f.write(image)
        f.close()
        print(self.badges.S + "Saved to " + cmd_data + "...")