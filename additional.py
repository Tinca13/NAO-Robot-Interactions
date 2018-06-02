from naoqi import ALProxy

#Class to use the other features not covered by the Movement and Joint classes such as TTS and changing eye colour
class Other():
    
    #Set the IP and Port values of the robot
    def __init__(self, IP, port):
        self.IP = IP
        self.port = port
        self.tts = ALProxy("ALTextToSpeech", self.IP, self.port)
        pass
    
    #method to take a string input which the robot will then speak
    def speak(self, message):
        self.tts.say(message)

    #method to change the eye colour of the robot (NOT COMPLETE)
    def eye_colour(self):
        led = ALProxy("ALLeds", self.IP, self.port)
        name = 'FaceLeds'
        led.randomEyes(10)
