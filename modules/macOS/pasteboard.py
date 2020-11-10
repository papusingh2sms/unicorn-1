#!/usr/bin/env python3

from core.badges import badges
from core.keyboard import keyboard

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()
        
        self.keyboard = keyboard()
        
        self.name = "pasteboard"
        self.description = "Control device pasteboard."
        self.usage = "Usage: pasteboard [read|write <value>]"
        self.type = "managing"
        self.args = 1
        
    def run(self, cmd_data):
        pass
