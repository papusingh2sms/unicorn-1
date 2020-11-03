import os

from core.badges import badges

class sender:
    def __init__(self, unicorn_handler):
        self.unicorn = unicorn_handler
        self.badges = badges()
        
    def send_command(self, command, cmd_data):
        template = []
        template.append(command)
        template.append(cmd_data)
        
        self.unicorn.send(str(template).encode("UTF-8"))
        return self.unicorn.recv().split().decode("UTF-8", "ignore")
