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
        if self.fsmanip.file(input_file):
            files = input_file + " " + output_path
            
            sended_upload = []
            sended_upload.append("upload")
            sended_upload.append(files)

            self.handler.send(str(sended_upload).encode("UTF-8"))
            error = self.handler.recv()
            if error == b"success":
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
                print(self.handler.recv().strip().decode("UTF-8", "ignore"))
            else:
                print(error.strip().decode("UTF-8"))

    def download(self, input_file, output_path):
        exists, path_type = self.fsmanip.exists_directory(output_path)
        if exists:
            if path_type != "file":
                if output_path[-1] == "/":
                    output_path = output_path + os.path.split(input_file)[1]
                else:
                    output_path = output_path + "/" + os.path.split(input_file)[1]
                    
            sended_download = []
            sended_download.append("download")
            sended_download.append(input_file)

            self.handler.send(str(sended_download).encode("UTF-8"))
            error = self.handler.recv()
            if error == b"success":
                print(self.badges.G + "Downloading {}...".format(input_file))
                wf = open(output_path, "wb")
                while True:
                    data = self.handler.recv()
                    if data == b"success":
                        break
                    elif data == b"fail":
                        wf.close()
                        os.remove(output_path)
                        print(self.badges.E + "Failed to download!")
                        return
                    wf.write(data)
                print(self.badges.G + "Saving to {}...".format(output_path))
                wf.close()
                print(self.badges.S + "Saved to {}!".format(output_path))
            else:
                print(error.strip().decode("UTF-8", "ignore"))
