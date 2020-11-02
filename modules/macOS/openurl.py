#!/usr/bin/env python3

from core.badges import badges
from core.transfer import transfer

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.unicorn = unicorn_handler
        self.transfer = transfer(self.unicorn)
        self.badges = badges()

        self.name = "openurl"
        self.description = "Open URL."
        self.usage = "Usage: openurl <url>"
        self.args = 2

    def run(self, cmd_data):
        if not cmd_data.startswith(("http://", "https://")):
            cmd_data = "http://" + cmd_data

        sended_url = []
        sended_url.append("openurl")
        sended_url.append(cmd_data)

        self.unicorn.send(list(sended_url).encode("UTF-8"))