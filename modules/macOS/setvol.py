#!/usr/bin/env python3

from core.badges import badges
from core.sender import sender

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.sender = sender(unicorn_handler)
        self.badges = badges()
        
        self.name = "setvol"
        self.description = "Set output sound volume."
        self.usage = "Usage: setvol [0-100]"
        self.type = "settings"
        self.args = 2
        
    def run(self, cmd_data):
        payload = "set volume output volume "+cmd_data
        self.sender.send_command("applescript", payload, False)
