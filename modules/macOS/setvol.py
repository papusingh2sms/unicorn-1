#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()
        
        self.name = "setvol"
        self.description = "Set output sound volume."
        self.usage = "Usage: setvol [0-100]"
        self.type = "settings"
        self.args = 2
        
    def run(self, cmd_data):
        payload = "set volume output volume "+cmd_data
        self.unicorn.send_command("osascript", payload)
