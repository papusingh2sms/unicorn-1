#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, sender):
        self.sender = sender
        self.badges = badges()

        self.name = "screenshot"
        self.description = "Take screenshot."
        self.usage = "Usage: screenshot <output_path>"
        self.type = "managing"
        self.args = 2

    def run(self, cmd_data):
        print(self.badges.G + "Taking screenshot...")
        
        image = self.sender.send_command(self.name, cmd_data, True, False)
        f = open(cmd_data, "wb")
        print(self.badges.G + "Saving to " + cmd_data + "...")
        f.write(image)
        f.close()
        print(self.badges.S + "Saved to " + cmd_data + "...")
