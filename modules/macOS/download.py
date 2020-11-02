#!/usr/bin/env python3

from core.badges import badges
from core.transfer import transfer

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.unicorn = unicorn_handler
        self.transfer = transfer(self.unicorn)
        self.badges = badges()

        self.name = "download"
        self.description = "Download remote file."
        self.usage = "Usage: download <input_file> <output_path>"
        self.args = 3

    def run(self, cmd_data):
        input_file = cmd_data.split(" ")[0]
        output_file = cmd_data.split(" ")[1]
        self.transfer.download(input_file, output_file)