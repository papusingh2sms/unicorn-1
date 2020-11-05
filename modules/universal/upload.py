#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, sender):
        self.sender = sender
        self.badges = badges()

        self.name = "upload"
        self.description = "Upload local file."
        self.usage = "Usage: download <input_file> <output_path>"
        self.type = "managing"
        self.args = 3

    def run(self, cmd_data):
        self.sender.upload(cmd_data)