import socket
import random

from core.badges import badges

class helper:
    def __init__(self):
        self.badges = badges()

        self.version = "v2.0"
        self.lhost = self.getip()
        self.lport = 4444

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

    def random_message(self):
        msgs = ['Simon’s StupidBot released at 2019?', 'Unicorn is not just a reverse shell.', 'Simon Chaykin liar?',
                'Pythons attack!', 'Unicorns attack!', 'Magic unicorns attack!', 'I can’t trust you, Mr. Robot',
                'NASA hacked!', 'Do not check Ivan’s code', 'bash -c bash -c bash', 'Simon Chaykin or Semuon Chaykin?',
                'Thank you 2020Vis13079846!', 'Sorry, Felix is not me!', 'rm -rf / --no-preserve-root']
        return self.badges.LINED + msgs[random.randint(0, len(msgs) - 1)] + self.badges.RESET