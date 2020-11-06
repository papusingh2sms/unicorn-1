#!/usr/bin/env python3

from core.badges import badges
from core.fsmanip import fsmanip

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()
        self.fsmanip = fsmanip()

        self.name = "screenshot"
        self.description = "Take screenshot."
        self.usage = "Usage: screenshot <local_path>"
        self.type = "managing"
        self.args = 2

    def run(self, cmd_data):
        print(self.badges.G + "Taking screenshot...")
        image = self.unicorn.send_command(self.name, cmd_data, True, False)
        exists, path_type = self.fsmanip.exists_directory(cmd_data)
        if exists:
            if path_type != "file":
                if cmd_data[-1] == "/":
                    cmd_data = cmd_data + "screenshot.png"
                else:
                    cmd_data = cmd_data + "/screenshot.png"
        f = open(cmd_data, "wb")
        print(self.badges.G + "Saving to " + cmd_data + "...")
        f.write(image)
        f.close()
        print(self.badges.S + "Saved to " + cmd_data + "...")
