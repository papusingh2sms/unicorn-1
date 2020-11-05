import os

from core.badges import badges
from core.transfer import transfer

class unicorn:
    def __init__(self, handler):
        self.handler = handler
        self.transfer = transfer(self.handler)
        self.badges = badges()

    def send_request(self, request, ask_for_response=True, decode=True):
        self.handler.send(request.encode("UTF-8"))

        try:
            response = self.handler.recv()
        except:
            ask_for_response = False

        if ask_for_response:
            if decode:
                return response.strip().decode("UTF-8", "ignore")
            else:
                return response

    def send_command(self, command, cmd_data=None, ask_for_response=True, decode=True):
        template = []
        template.append(command)

        if cmd_data != None:
            template.append(cmd_data)

        self.handler.send(str(template).encode("UTF-8"))

        try:
            response = self.handler.recv()
        except:
            ask_for_response = False

        if ask_for_response:
            if decode:
                return response.strip().decode("UTF-8", "ignore")
            else:
                return response

    def download(self, cmd_data):
        input_file = cmd_data.split(" ")[0]
        output_file = cmd_data.split(" ")[1]
        self.transfer.download(input_file, output_file)

    def upload(self, cmd_data):
        input_file = cmd_data.split(" ")[0]
        output_file = cmd_data.split(" ")[1]
        self.transfer.upload(input_file, output_file)
