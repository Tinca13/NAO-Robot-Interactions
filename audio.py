import time
from naoqi import ALProxy

class Audio():
    def __init__(self, ip):
        self.ip = ip
        self.port = 9559
        self.aup = ALProxy("ALAudioPlayer", self.ip, self.port)

    def play_audio(self, file_name, ext='.mp3'):
        file_id = self.aup.loadFile("/home/nao/{0}{1}".format(file_name, ext))
        #time.sleep(1)
        self.aup.play(file_id)

    def upload_audio(self):
        pass
