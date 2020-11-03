#!/usr/bin/env python3

from core.badges import badges
from core.sender import sender

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.sender = sender(unicorn_handler)
        self.badges = badges()
        
        self.name = "safemode"
        self.description = "Put device into SafeMode."
        self.usage = "Usage: safemode"
        self.type = "boot"
        self.args = 1
        
    def run(self, cmd_data):
        print(self.badges.G + "Putting device into SafeMode...")
        self.sender.send_command("shell", "touch /var/mobile/Library/Preferences/com.saurik.mobilesubstrate.dat; killall SpringBoard", False)
        print(self.badges.S + "Successfully put into SafeMode!")
