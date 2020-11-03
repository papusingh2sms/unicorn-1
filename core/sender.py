class sender:
    def __init__(self):
        self.init = 1
        
    def send_command(self, command, cmd_data):
        template = []
        template.append(command)
        template.append(cmd_data)
        
        return template
