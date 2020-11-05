#!/usr/bin/env python3

class keyboard:
    def __init__(self):
        self.keyboard_init = 1
        
    def get_char(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
            
    def send_char(self, char):
        payload = """
        tell application "System Events"
            keystroke \""""+char+"""\"
        end tell
        """
        
        return payload
