#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()

        self.name = "openurl"
        self.description = "Open URL."
        self.usage = "Usage: openurl <url>"
        self.type = "managing"
        self.args = 2

    def run(self, cmd_data):
        if not cmd_data.startswith(("http://", "https://")):
            cmd_data = "http://" + cmd_data

        self.unicorn.send_command(self.name, cmd_data, False)