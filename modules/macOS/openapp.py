#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()
        
        self.name = "openapp"
        self.description = "Open application on device."
        self.usage = "Usage: openapp <application>"
        self.type = "managing"
        self.args = 2
        
    def run(self, cmd_data):
        payload = "tell application \""+cmd_data+"\" to activate"
        self.unicorn.send_command("osascript", payload, False)
