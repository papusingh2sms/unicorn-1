#!/usr/bin/env python3

from core.badges import badges
from core.sender import sender

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.sender = sender(unicorn_handler)
        self.badges = badges()
        
        self.name = "getvol"
        self.description = "Show output sound volume."
        self.usage = "Usage: getvol"
        self.type = "settings"
        self.args = 1
        
    def run(self, cmd_data):
        payload = "output volume of (get volume settings)"
        print(self.badges.I + "Current output sound volume: " + self.sender.send_command("osascript", payload))
