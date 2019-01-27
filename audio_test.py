from naoqi import ALProxy
import time

ip = "169.254.65.171"
port = 9559

aup = ALProxy("ALAudioPlayer", ip, port)
fileId = aup.loadFile("/home/nao/test1.mp3")
time.sleep(5)
aup.play(fileId)
