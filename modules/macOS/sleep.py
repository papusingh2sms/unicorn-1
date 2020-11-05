#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, sender):
        self.sender = sender
        self.badges = badges()
        
        self.name = "sleep"
        self.description = "Put device into SleepMode."
        self.usage = "Usage: sleep"
        self.type = "boot"
        self.args = 1
        
    def run(self, cmd_data):
        payload = "tell application \"Finder\" to sleep"
        self.sender.send_command("osascript", payload, False)
