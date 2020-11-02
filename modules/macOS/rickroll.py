#!/usr/bin/env python3

from core.badges import badges
from core.transfer import transfer

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.unicorn = unicorn_handler
        self.transfer = transfer(self.unicorn)
        self.badges = badges()

        self.name = "rickroll"
        self.description = "Rickroll."
        self.usage = "Usage: rickroll"
        self.type = "trolling"
        self.args = 1

    def run(self, cmd_data):
        sended_url = []
        sended_url.append("openurl")
        sended_url.append("https://www.youtube.com/watch?v=oHg5SJYRHA0")

        self.unicorn.send(str(sended_url).encode("UTF-8"))
        print(self.badges.S + "Target has been rickrolled!")