#!/usr/bin/env python3

import os

from core.badges import badges
from core.fsmanip import fsmanip

class transfer:
    def __init__(self, handler):
        self.handler = handler
        self.badges = badges()
        self.fsmanip = fsmanip()

    def upload(self, input_file, output_path):
        if os.path.exists(input_file):
            if file(input_file):
                sended_upload = []
                sended_upload.append("upload")
                sended_upload.append(output_file)

                self.handler.send(str(sended_upload).encode("UTF-8"))
                print(self.badges.G + "Uploading {}...".format(input_file))
                with open(input_file, "rb") as wf:
                    for data in iter(lambda: wf.read(4100), b""):
                        try:
                            self.handler.send(data)
                        except (KeyboardInterrupt, EOFError):
                            wf.close()
                            self.handler.send("fail".encode("UTF-8"))
                            print(self.badges.E + "Failed to upload!")
                            return
                self.handler.send("success".encode("UTF-8"))
                print(self.badges.G + "Saving to " + output_file + "...")
                print(self.badges.S + "Saved to " + output_file + "!")
            else:
                print(self.badges.E + "Local file: " + input_file + ": does not exist!")

    def download(self, input_file, output_file):
        exists, path_type = self.fsmanip.exists_directory(output_file)
        if exists:
            if path_type != "file":
                if output_file[-1] == "/":
                    output_file = output_file + os.path.split(input_file)[1]
                else:
                    output_file = output_file + "/" + os.path.split(input_file)[1]
                    
            sended_download = []
            sended_download.append("download")
            sended_download.append(input_file)

            self.handler.send(str(sended_download).encode("UTF-8"))
            down = self.handler.recv().decode("UTF-8", "ignore")
            if down == "true":
                print(self.badges.G + "Downloading {}...".format(output_file))
                wf = open(output_file, "wb")
                while True:
                    data = self.handler.recv()
                    if data == b"success":
                        break
                    elif data == b"fail":
                        wf.close()
                        os.remove(output_file)
                        print(self.badges.E + "Failed to download!")
                        return
                    wf.write(data)
                print(self.badges.G + "Saving to {}...".format(output_file))
                wf.close()
                print(self.badges.S + "Saved to {}!".format(output_file))
            else:
                print(down)
