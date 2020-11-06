#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()

        self.name = "download"
        self.description = "Download remote file."
        self.usage = "Usage: download <remote_file> <local_path>"
        self.type = "stealing"
        self.args = 3

    def run(self, cmd_data):
        self.unicorn.download(cmd_data)
