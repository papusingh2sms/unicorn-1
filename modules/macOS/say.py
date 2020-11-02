#!/usr/bin/env python3

from core.badges import badges
from core.transfer import transfer

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.unicorn = unicorn_handler
        self.transfer = transfer(self.unicorn)
        self.badges = badges()

        self.name = "say"
        self.description = "Say message."
        self.usage = "Usage: say <message>"
        self.args = 2

    def run(self, cmd_data):
        sended_message = []
        sended_message.append("say")
        sended_message.append(cmd_data)

        self.unicorn.send(str(sended_message).encode("UTF-8"))
        status = self.unicorn.recv()
        if status == b"success":
            print(self.badges.S + "Done saying message!")
        else:
            print(self.badges.E + "Failed to say message!")