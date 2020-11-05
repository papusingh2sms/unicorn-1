#!/usr/bin/env python3

from core.badges import badges

try:
    from msvcrt import getch
except ImportError:
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

class MagicUnicorn:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.badges = badges()
        
        self.name = "keyboard"
        self.description = "Control targets keyboard."
        self.usage = "Usage: keyboard"
        self.type = "managing"
        self.args = 1
        
    def run(self, cmd_data):
        print(self.badges.G + "Connecting to keyboard...")
        print(self.badges.I + "Press Ctrl-C to stop.")
        while True:
            key = getch()
            if key != chr(03):
                payload = """
                tell application "System Events"
                    keystroke \""""+key+"""\"
                end tell
                """
                self.unicorn.send_command("osascript", payload, False)
            else:
                return
