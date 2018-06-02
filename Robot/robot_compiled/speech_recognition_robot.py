import speech_recognition as sr
import datetime
import sys
import naoqi
import time
import random
from movement import Movement
from additional import Other
"""
    TODO: run choregraphe scripts from Python and add to commands
          test this script on the robot
          test accuracy with background noise
"""

class Speech():
    def __init__(self, ip, port, audio_log_path):
        self.ip = ip
        self.port = port
        self.log_path = audio_log_path
        self.move = Movement(ip, port)
        self.tts = Other(self.ip, self.port)
        self.greeting_list = ["Hi, I am Robbie the robot, how are you?",
                              "Greetings traveller, and well met!",
                              "Hello there, and welcome to Edge Hill Computer Science Department. I am Robbie the robot"]
        self.emotions_list = ["I am feeling okay, thank you. And you?",
                              "I am feeling well, you?",
                              "I am doing well thanks",
                              "Installing emotional protocols beep boop... I am feeling what would be defined as 'well'. And you?"]
        self.dance_dict = {"thriller": "new_thriller-40424e/new_thriller",
                           "disco": "disco-dd565c/disco",
                           "arm dance": "arm_dance-074ba5/arm_dance",
                           "tai chi": "taichi-cd9975/GangnamStyle",
                           "gangnam style": "gangnam_style-2b4c5b/GangnamStyle (1)"}
        self.behaviour_dict = {"sneeze": "sneezes-4c12b5/Sneezes",
                               "pushups": "pushupsz-cc23cb/pushups",
                               "hello": "hello-bde0d2/blow_kisses",
                               "blow kiss": "blow_kisses-b60c2b/blow_kisses",
                               "air guitar": "air_guitar-f1b1e7/air_guitar"}

    def microphone_check(self):
        """For testing current microphones on the device"""
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

    def recognise_audio(self):
        """Handles the recognition of the audio to pass to the commands method"""
        #can be used to clear the log file every time the audio is recognised
        #with open(log_path, "w") as log_file:
        #    log_file.close()

        audio_check = True
        while audio_check:
            speech_recogniser = sr.Recognizer()
            data = []

            with sr.Microphone(1) as source:
                #can change timeout and time limit to increase the delay before ending a phrase, and increasing the length of a phrase
                audio = speech_recogniser.listen(source, timeout=5, phrase_time_limit=10)
                print("end of phrase...")

            try:
                audio_log = speech_recogniser.recognize_google(audio)
                print("at {} user said {}".format(datetime.datetime.now(), audio_log))
                #passes the recorded audio through to get the robot to act based on the response
                self.commands(audio_log)
                #appends the response to a list to be added to the log file
                data.append(audio_log)
                #extra line to get the timestamp of when something was said
                #data.append("at {} user said: {}\n".format(datetime.datetime.now(), audio_log))
                with open(self.log_path, "a") as log:
                    for sample in data:
                        #separates new samples onto a new line to denote that they are separate phrases
                        log.write(sample + "\n")

            except sr.UnknownValueError:
                print("Audio not understood, please try again")

            except sr.RequestError as req_err:
                print("could not request results from google API {}".format(req_err))

            except sr.WaitTimeoutError:
                print("Audio timed out, ending the process...")
                audio_check = False

    def get_time(self):
        """Gets the current time and splits based on whether it is am or pm

        :return: returns the current time split into hours, minutes and meridiem (am or pm)
        """
        now = datetime.datetime.now()
        hour = now.hour
        if hour > 12:
            hour -= 12
            meridiem = 'pm'
        else:
            meridiem = 'am'

        return hour, now.minute, meridiem

    def commands(self, command):
        """Gets the robot to perform actions based an audio input from the user
        :param str command: the audio_log of the user's command, taken from the recognise_audio method
        """
        # TODO: add dances when working with choregraphe scripts

        command = command.lower()
        print("command is {}".format(command))
        if command == "hello robbie":
            self.tts.speak(random.choice(self.greeting_list))
            self.move.behaviour(behaviour_name=self.behaviour_dict['hello'])
            # self.move.toggle_autonomous_movement()
        elif command == "fire the trebuchet":
            self.tts.speak("Beep beep... Target locked")
        elif command == "what is the time" or command == "what time is it":
            hour, minute, meridiem = self.get_time()
            self.tts.speak("The time is {}:{} {}".format(hour, minute, meridiem))
        elif command == "how are you robbie" or command == "how are you":
            self.tts.speak(random.choice(self.emotions_list))
        elif command == "where are we":
            self.tts.speak("We are at Edge Hill University, situated in the north-western town of Ormskirk")
        elif command == "what is this department":
            self.tts.speak("this is the computer science department, which has a wide variety of courses!")
        elif command == "what is your favourite pathway":
            self.tts.speak("BSc Robotics and Artificial Intelligence, you will even get to program me if your final year project is suitable!")
        elif command == "can you sit down":
            self.tts.speak("Time for a sit down!")
            self.move.posture("Sit")
        elif command == "stand":
            self.tts.speak("Standing up!")
            self.move.posture("StandInit")
        elif command == "can you walk forwards" or command == "come over here robbie":
            self.tts.speak("Get ready to catch me!")
            time.sleep(0.5)
            self.move.walk(0.5, _sleep=5)
            pass
        elif command == "can you walk backwards":
            self.tts.speak("Get ready to catch me!")
            self.move.walk(-0.5, _sleep=5)
            pass
        elif command == "are you tired robbie":
            self.tts.speak("yawn... time for a lie down")
            self.move.posture("LyingBack")
        elif command == "do you feel like dancing":
            # TODO: add behaviour code for dancing
            index, current_dance = random.choice(self.dance_dict.items())
            print("current dance: {}".format(current_dance))
            self.move.behaviour(behaviour_name=current_dance)
        elif command == "show me your best dance moves":
            self.move.behaviour(behaviour_name="canavanplacemusic-16a6c1/CanavanPlace music")
        elif command == "can you play the guitar":
            self.move.behaviour(behaviour_name=self.behaviour_dict['air guitar'])
        elif command == "why don't you do some exercise" or command == "can you do push-ups":
            self.move.behaviour(behaviour_name=self.behaviour_dict['pushups'])
        elif command == "bless you":
            self.move.behaviour(behaviour_name=self.behaviour_dict['sneeze'])
        elif command == "it is time to stop" or command == "can you please stop that movement":
            self.move.behaviour(behaviour_name="stop")
        else:
            return

    def call_method(self):
        try:
            self.recognise_audio()
        except KeyboardInterrupt:
            sys.exit()
        except:
            print("problemerino solved")
            self.call_method()


#default, needs to be changed to correct one for current robot and device
ip = "192.168.1.120"
#always 9559, do not change
port = 9559
#change file path to wherever the files are saved
log_path = "D:/Erik_Thomas/Robot/robot_audio/audio_out.txt"
speech_rec = Speech(ip, port, log_path)

speech_rec.call_method()