#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()
        
        self.name = "suspend"
        self.description = "Suspend current session."
        self.usage = "Usage: suspend"
        self.type = "boot"
        self.args = 1
        
    def run(self, cmd_data):
        self.unicorn.send_command("shell", "/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend", False)
