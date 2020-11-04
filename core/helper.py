import socket
import random

from core.badges import badges

class helper:
    def __init__(self):
        self.badges = badges()

        self.version = "v2.0"
        self.lhost = self.getip()
        self.lport = 4444

        self.get_arch = "uname -p\n"
        self.get_system = "uname -s\n"

    def getip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("192.168.1.1", 80))
            host = s.getsockname()[0]
            s.close()
            host = host
        except:
            host = "127.0.0.1"
        return host

    def show_commands(self, universal_commands, target_commands, core_commands=['exit', 'clear', 'exec']):
        settings_commands = []
        managing_commands = []
        stealing_commands = []
        trolling_commands = []
        boot_commands = []

        commands = dict()
        commands.update(universal_commands)
        commands.update(target_commands)

        for i in commands:
            if commands[i].type == "settings": settings_commands.append(commands[i])
            if commands[i].type == "managing": managing_commands.append(commands[i])
            if commands[i].type == "stealing": stealing_commands.append(commands[i])
            if commands[i].type == "trolling": trolling_commands.append(commands[i])
            if commands[i].type == "boot": boot_commands.append(commands[i])

        if len(core_commands) > 0:
            print("")
            print("Core Commands")
            print("=============")
            print("")
            print("    Command        Description")
            print("    -------        -----------")
            for i in core_commands:
                print("    " + i + " " * (7 - len(i) + 8) + "Core command.")
            print("")

        if len(settings_commands) > 0:
            print("Settings Commands")
            print("=================")
            print("")
            print("    Command        Description")
            print("    -------        -----------")
            for i in settings_commands:
                print("    " + i.name + " " * (7 - len(i.name) + 8) + i.description)
            print("")

        if len(managing_commands) > 0:
            print("Managing Commands")
            print("=================")
            print("")
            print("    Command        Description")
            print("    -------        -----------")
            for i in managing_commands:
                print("    " + i.name + " " * (7 - len(i.name) + 8) + i.description)
            print("")

        if len(stealing_commands) > 0:
            print("Stealing Commands")
            print("=================")
            print("")
            print("    Command        Description")
            print("    -------        -----------")
            for i in stealing_commands:
                print("    " + i.name + " " * (7 - len(i.name) + 8) + i.description)
            print("")

        if len(trolling_commands) > 0:
            print("Trolling Commands")
            print("=================")
            print("")
            print("    Command        Description")
            print("    -------        -----------")
            for i in trolling_commands:
                print("    " + i.name + " " * (7 - len(i.name) + 8) + i.description)
            print("")

        if len(boot_commands) > 0:
            print("Boot Commands")
            print("=============")
            print("")
            print("    Command        Description")
            print("    -------        -----------")
            for i in boot_commands:
                print("    " + i.name + " " * (7 - len(i.name) + 8) + i.description)
            print("")

    def random_message(self):
        msgs = ['Simon’s StupidBot released at 2019?', 'Unicorn is not just a reverse shell.', 'Simon Chaykin liar?',
                'Pythons attack!', 'Unicorns attack!', 'Magic unicorns attack!', 'I can’t trust you, Mr. Robot',
                'NASA hacked!', 'Do not check Ivan’s code', 'bash -c bash -c bash', 'Ivan Nikolsky liar?',
                'Thank you 2020Vis13079846!', 'Sorry, Felix is not me!', 'rm -rf / --no-preserve-root', '<3 Alena L0v3 <3', 
                'xor simon, simon; push simon // this will not work :(', 'Do not use Objective-C for this! This is how EggShell created.']
        return self.badges.LINED + msgs[random.randint(0, len(msgs) - 1)] + self.badges.RESET
