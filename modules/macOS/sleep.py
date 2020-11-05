#!/usr/bin/env python3

from core.badges import badges
from core.sender import sender

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.sender = sender(unicorn_handler)
        self.badges = badges()
        
        self.name = "sleep"
        self.description = "Put device into SleepMode."
        self.usage = "Usage: sleep"
        self.type = "boot"
        self.args = 1
        
    def run(self, cmd_data):
        pass
