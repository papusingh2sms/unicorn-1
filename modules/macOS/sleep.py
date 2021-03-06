#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()
        
        self.name = "sleep"
        self.description = "Put device into sleep mode."
        self.usage = "Usage: sleep"
        self.type = "boot"
        self.args = 1
        
    def run(self, cmd_data):
        payload = "tell application \"Finder\" to sleep"
        self.unicorn.send_command("osascript", payload, False)
