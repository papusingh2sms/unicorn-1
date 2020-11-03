import os

from core.badges import badges
from core.transfer import transfer

class sender:
    def __init__(self, unicorn_handler):
        self.unicorn = unicorn_handler
        self.transfer = transfer(self.unicorn)
        self.badges = badges()

    def send_request(self, request, ask_for_response=True, decode=True):
        self.unicorn.send(request.encode("UTF-8"))
        if ask_for_response:
            if decode:
                return self.unicorn.recv().strip().decode("UTF-8", "ignore")
            else:
                return self.unicorn.recv()

    def send_command(self, command, cmd_data=None, ask_for_response=True, decode=True):
        template = []
        template.append(command)

        if cmd_data != None:
            template.append(cmd_data)

        self.unicorn.send(str(template).encode("UTF-8"))

        if ask_for_response:
            if decode:
                return self.unicorn.recv().strip().decode("UTF-8", "ignore")
            else:
                return self.unicorn.recv()

    def download(self, cmd_data):
        input_file = cmd_data.split(" ")[0]
        output_file = cmd_data.split(" ")[1]
        self.transfer.download(input_file, output_file)

    def upload(self, cmd_data):
        input_file = cmd_data.split(" ")[0]
        output_file = cmd_data.split(" ")[1]
        self.transfer.upload(input_file, output_file)