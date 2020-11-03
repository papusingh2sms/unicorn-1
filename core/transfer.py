import os

from core.badges import badges

class transfer:
    def __init__(self, unicorn_handler):
        self.unicorn = unicorn_handler
        self.badges = badges()

    def upload(self, input_file, output_file):
        if not os.path.isfile(input_file):
            print(self.badges.E + "Local file: " + output_file + ": does not exist!")
        else:
            sended_upload = []
            sended_upload.append("upload")
            sended_upload.append(output_file)

            self.unicorn.send(str(sended_upload).encode("UTF-8"))
            print(self.badges.G + "Uploading {}...".format(input_file))
            with open(input_file, "rb") as wf:
                for data in iter(lambda: wf.read(4100), b""):
                    try:
                        self.unicorn.send(data)
                    except(KeyboardInterrupt, EOFError):
                        wf.close()
                        self.unicorn.send("fail".encode("UTF-8"))
                        print(self.badges.E + "Failed to upload!")
                        return
            self.unicorn.send("success".encode("UTF-8"))
            print(self.badges.G + "Saving to " + output_file + "...")
            print(self.badges.S + "Saved to " + output_file + "!")

    def download(self, input_file, output_file):
        sended_download = []
        sended_download.append("download")
        sended_download.append(input_file)

        self.unicorn.send(str(sended_download).encode("UTF-8"))
        down = self.unicorn.recv().decode("UTF-8", "ignore")
        if down == "true":
            print(self.badges.G + "Downloading {}...".format(output_file))
            wf = open(output_file, "wb")
            while True:
                data = self.unicorn.recv()
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
