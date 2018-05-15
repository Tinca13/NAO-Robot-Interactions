import speech_recognition as sr
import datetime
import sys
import naoqi
import time
import random
from movement import Movement
"""
    TODO: run choregraphe scripts from Python and add to commands
          test this script on the robot
          test accuracy with background noise
"""
#default, needs to be changed to correct one for current robot and device
ip = "192.168.1.123"
#always 9559, do not change
port = 9559

def microphone_check():
    """For testing current microphones on the device"""
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

def recognise_audio():
    """Handles the recognition of the audio to pass to the commands method"""
    #change file path to wherever the files are saved
    log_path = "E:/Erik_Thomas/speech_recognition/audio_out.txt"
    #can be used to clear the log file every time the audio is recognised
    #with open(log_path, "w") as log_file:
    #    log_file.close()

    audio_check = True
    while audio_check:
        speech_recogniser = sr.Recognizer()
        data = []

        with sr.Microphone(1) as source:
            #can change timeout and time limit to increase the delay before ending a phrase, and increasing the length of a phrase
            audio = speech_recogniser.listen(source, timeout=2, phrase_time_limit=10)
            print("end of phrase...")

        try:
            audio_log = speech_recogniser.recognize_google(audio)
            print("at {} user said {}".format(datetime.datetime.now(), audio_log))
            #passes the recorded audio through to get the robot to act based on the response
            commands(audio_log)
            #appends the response to a list to be added to the log file
            data.append(audio_log)
            #extra line to get the timestamp of when something was said
            #data.append("at {} user said: {}\n".format(datetime.datetime.now(), audio_log))
            with open(log_path, "a") as log:
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

def commands(command):
    """Gets the robot to perform actions based an audio input from the user
    :param str command: the audio_log of the user's command, taken from the recognise_audio method
    """
    #TODO: add dances when working with choregraphe scripts
    move = Movement(ip, port)
    tts = ALProxy("ALTextToSpeech", ip, port)

    command = command.lower()
    print("command is {}".format(command))
    if command == "hello robbie":
        #fix greeting list
        tts.say(random.choice(self.greeting_list))
        move.right_wave_start(4)
        move.toggle_autonomous_movement()
    elif command == "fire the trebuchet":
        tts.say("Beep beep... Target locked")
    elif command == "what is the time" or command == "what time is it":
        now = datetime.datetime.now()
        hour = now.hour
        if hour > 12:
            hour -= 12
            meridiem = 'pm'
        else:
            meridiem = 'am'
            
        tts.say("The time is {}:{} {}".format(hour, now.minute, meridiem))
    elif command == "how are you robbie" or command == "how are you":
        tts.say(random.choice(self.emotions_list))
    elif command == "where are we":
        tts.say("We are at Edge Hill University, situated in the north-western town of Ormskirk")
    elif command == "what is this department":
        tts.say("this is the computer science department, which has a wide variety of courses!")
    elif command == "what is your favourite pathway":
        tts.say("BSc Robotics and Artificial Intelligence, you will even get to program me if your final year project is suitable!")
    elif command == "can you sit down":
        tts.say("Time for a sit down!")
        move.posture("Sit")
    elif command == "stand":
        tts.say("Standing up!")
        move.posture("StandInit")
    elif command == "can you walk forwards" or command == "come over here robbie":
        tts.say("Get ready to catch me!")
        time.sleep(0.5)
        move.walk(0.5, _sleep=5)
        pass
    elif command == "can you walk backwards":
        tts.say("Get ready to catch me!")
        move.walk(-0.5, _sleep=5)
        pass
    elif command == "are you tired robbie":
        tts.say("yawn... time for a lie down")
        move.posture("LyingBack")

def call_method(x):
    try:
        for y in range(0,x):
        
            recognise_audio()
    except KeyboardInterrupt:
        sys.exit()
    except:
        print("problemerino solved")
        call_method(5)
call_method(5)
