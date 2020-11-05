#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()
        
        self.name = "alert"
        self.description = "Make alert show up on device."
        self.usage = "Usage: alert <title> <message> <icon> <application> <first_button> <second_button>"
        self.type = "managing"
        self.args = 7

    def run(self, cmd_data):
        title = cmd_data.split(" ")[0]
        message = cmd_data.split(" ")[1]
        icon = cmd_data.split(" ")[2]
        application = cmd_data.split(" ")[3]
        first_button = cmd_data.split(" ")[4]
        second_button = cmd_data.split(" ")[5]
        
        delim = '"'
        
        payload = """
        tell application """+delim+""""""+application+""""""+delim+"""
            activate
                try
                    display dialog """+delim+""""""+message+""""""+delim+""" with title """+delim+""""""+title+""""""+delim+""" buttons {"""+delim+""""""+first_button+""""""+delim+""", """+delim+""""""+second_button+""""""+delim+"""} default button """+delim+""""""+first_button+""""""+delim+""" cancel button """+delim+""""""+second_button+""""""+delim+""" with icon path to resource """+delim+""""""+icon+""".icns"""+delim+""" in bundle "/System/Library/CoreServices/CoreTypes.bundle"
                end try 
        end tell        
        """
        
        self.unicorn.send_command("osascript", payload, False)
