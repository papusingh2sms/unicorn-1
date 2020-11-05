#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, sender):
        self.sender = sender
        self.badges = badges()

        self.name = "download"
        self.description = "Download remote file."
        self.usage = "Usage: download <input_file> <output_path>"
        self.type = "stealing"
        self.args = 3

    def run(self, cmd_data):
        self.sender.download(cmd_data)