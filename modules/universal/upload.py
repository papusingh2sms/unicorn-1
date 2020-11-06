#!/usr/bin/env python3

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()

        self.name = "upload"
        self.description = "Upload local file."
        self.usage = "Usage: upload <local_file> <remote_path>"
        self.type = "managing"
        self.args = 3

    def run(self, cmd_data):
        self.unicorn.upload(cmd_data)
