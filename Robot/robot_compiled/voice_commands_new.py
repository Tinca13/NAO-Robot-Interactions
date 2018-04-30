import speech_recognition as sr
import time
import datetime
import thread
import os
import random
import shutil
from naoqi import ALProxy, ALModule, ALBroker
from ftplib import FTP
from movement import Movement

class ReactToTouch(ALModule):
    def __init__(self, module_name, ip, port, it):
        ALModule.__init__(self, module_name)
        self.memory = ALProxy("ALMemory")
        self.audio = None
        self.record_check = False
        self.counter = 0
        self.inter_type = it

        print("audio init")
        for root, dirs, files in os.walk('D:/Erik_Thomas/Robot/robot_audio/'):
            for _file in files:
                os.remove(root + _file)
        
        try:
            print("sub")
            self.memory.subscribeToEvent("FrontTactilTouched", "ReactToTouch", "onTouched")
        except:
            print("unsub")
            self.memory.unsubscribeToEvent("FrontTactilTouched", "ReactToTouch")
            time.sleep(1)
            print("sub2")
            self.memory.subscribeToEvent("FrontTactilTouched", "ReactToTouch", "onTouched")
        print("hello")
        #global memory     

    def onTouched(self, strVarName, value):
        self.audio = Audio(ip, port)
        self.counter += 1
        
        print("unsub2")
        self.memory.unsubscribeToEvent("FrontTactilTouched", "ReactToTouch")
        if self.counter % 3 == 0:
            print("save me")     
            self.memory.subscribeToEvent("FrontTactilTouched", "ReactToTouch", "onTouched")
            pass

        else:
            print("resub")      
            self.memory.subscribeToEvent("FrontTactilTouched", "ReactToTouch", "onTouched")
            if not self.record_check:
                print("record check false")
                self.record_check = True
                self.audio.start_record()
            
            elif self.record_check:
                print("record check true")
                self.record_check = False
                self.audio.stop_record()     
                self.audio.get_file()
                self.audio.speech_rec(self.inter_type)
        #print("resub")      
        #self.memory.subscribeToEvent("FrontTactilTouched", "ReactToTouch", "onTouched")
        
class Audio():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.recogniser = sr.Recognizer()
        self.audio_counter = 0
        self.full_data = []
        self.write_data = []
        self.tts = ALProxy("ALTextToSpeech", self.ip, self.port)
        self.audio = ALProxy("ALAudioDevice", self.ip, self.port)
        self.record = ALProxy("ALAudioRecorder", self.ip, self.port)
        self.aup = ALProxy("ALAudioPlayer", self.ip, self.port)
        self.move = Movement(self.ip, self.port)
        self.greeting_list = ["Hi, I am Robbie the robot, how are you?", "Greetings traveller, and well met!", "Hello there, and welcome to Edge Hill Computer Science Department. I am Robbie the robot"]
        self.emotions_list = ["I am feeling okay, thank you. And you?", "I am feeling well, you?", "I am doing well thanks", "Installing emotional protocols beep boop... I am feeling what would be defined as 'well'. And you?"]
        
    def check_microphones(self):
        '''Checks for microphones currently active on the device'''
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

    def command_manager(self):
        with open('D:/Erik_Thomas/Robot/robot_compiled/commands.txt', 'r') as commands:
            _commands = commands.read()
            commands.close()
        self.command_list = _commands.split(",")
        print(self.command_list)
        print("looking for: " + str(self.audio_counter))
        
        audio_file_name = 'D:/Erik_Thomas/Robot/robot_audio/000001.wav'
        with sr.AudioFile(audio_file_name) as source:
            audio = self.recogniser.listen(source)
        try:
            #tries to print the word
            print("you said {}".format(self.recogniser.recognize_google(audio)))
            audio_log = self.recogniser.recognize_google(audio)
            self.write_data.append("at {} user said: {}\n".format(datetime.datetime.now(), audio_log))
            #self.tts.say("You said {}".format(audio_log))
            audio_log = audio_log.lower()
            if audio_log in self.command_list:
                print("command recognised, command is {}".format(audio_log.lower()))
                self.commands(audio_log)

            else:
                print("not a command")
                
            with open('D:/Erik_Thomas/Robot/robot_audio/audio_log.txt', 'w+') as log_file:
                for sample in self.write_data:
                    log_file.write(sample + "\n")

        except sr.UnknownValueError:
            print("Audio not understood, please try again")

        except sr.RequestError as req_err:
            print("could not request results from google API {}".format(req_err))
        pass


    def chatbot(self):
        #NOT FINISHED
        pass
    
    #interaction_type = chatbot or commands
    def speech_rec(self, interaction_type):
        
        if interaction_type == 'commands':
            self.command_manager()
        elif interaction_type == 'chatbot':
            self.chatbot()
        

    def commands(self, command):
        command = command.lower()
        print("command is {}".format(command))
        if command == "hello robbie":
            self.tts.say(random.choice(self.greeting_list))
            self.move.right_wave_start(4)
            self.move.toggle_autonomous_movement()
        elif command == "fire the trebuchet":
            self.tts.say("Beep beep... Target locked")
            #add trebuchet method here
        elif command == "what is the time" or command == "what time is it":
            now = datetime.datetime.now()
            hour = now.hour
            if hour > 12:
                hour -= 12
                meridiem = 'pm'
            else:
                meridiem = 'am'
            
            self.tts.say("The time is {}:{} {}".format(hour, now.minute, meridiem))
        elif command == "how are you robbie" or command == "how are you":
            self.tts.say(random.choice(self.emotions_list))
        elif command == "where are we":
            self.tts.say("We are at Edge Hill University, situated in the north-western town of Ormskirk")
        elif command == "what is this department":
            self.tts.say("this is the computer science department, which has a wide variety of courses!")
        elif command == "what is your favourite pathway":
            self.tts.say("BSc Robotics and Artificial Intelligence, you will even get to program me if your final year project is suitable!")
        elif command == "can you sit down":
            self.tts.say("Time for a sit down!")
            self.move.posture("Sit")
        elif command == "stand":
            self.tts.say("Standing up!")
            self.move.posture("StandInit")
        elif command == "can you walk forwards" or command == "come over here robbie":
            self.tts.say("Get ready to catch me!")
            time.sleep(0.5)
            self.move.walk(0.5, _sleep=5)
            pass
        elif command == "can you walk backwards":
            self.tts.say("Get ready to catch me!")
            self.move.walk(-0.5, _sleep=5)
            pass
        elif command == "are you tired robbie":
            self.tts.say("yawn... time for a lie down")
            self.move.posture("LyingBack")
    
    def content(self, n):
        self.full_data.append(n)

    def get_file(self):
        self.audio_counter += 1
        #used for if a new directory is created where the file does not exist yet, prevents errors
        try:
            pass
            #os.remove('D:/Erik_Thomas/Robot/robot_audio/test.wav')
        except:
            pass
        print("getting the file")
        ftp = FTP(self.ip)
        print("ftp start")
        ftp.login('nao', 'nao')
        print("ftp login")
        ftp.retrlines('LIST')
        ftp.retrbinary('RETR ssq.wav', self.content)
        print("opening file")
        audio_file_name = 'D:/Erik_Thomas/Robot/robot_audio/00000' + str(self.audio_counter) + '.wav'
        print("saving: " + str(self.audio_counter))
        with open(audio_file_name, 'wb+') as source:
            for tmp in self.full_data:
                source.write(tmp)     

    def start_record(self):
        self.tts.say("beep boop")
        print("starting recording")
        record_path = '/home/nao/ssq.wav'
        #can change tuple parameter for each mic
        #front, back, left, right

        #add tactile sensor event here
        self.record.startMicrophonesRecording(record_path, 'wav', 16000, (1,0,0,0))

    def stop_record(self):
        #check tactile sensor event to stop
        self.record.stopMicrophonesRecording()
        print("Recording stopped")

if __name__ == '__main__':
    ip = '169.254.65.171'
    port = 9559
    myBroker = ALBroker("myBroker", '0.0.0.0', 0, ip, port)
    ReactToTouch = ReactToTouch("ReactToTouch", ip, port, "commands")
    try:
        while True:
            #time.sleep(1)
            pass

    except:
        print("stopping")
        myBroker.shutdown()
    
