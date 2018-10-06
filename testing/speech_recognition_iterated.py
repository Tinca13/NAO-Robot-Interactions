"""
Author: Erik Thomas 28-09-18

TODO: 
    -- Somehow compact the if statements
    -- Separate robot's actions into behaviour class
"""
import time
import random
import datetime
import sys

import speech_recognition as sr
from naoqi import ALProxy

import pickle_lists as pl
from movement import Movement
from additional import Other

class Speech():
    def __init__(
                self, ip, motion_proxy, 
                bhv_file, bhv_dir, log_dir, 
                com_file, com_dir
                ):
        self.IP = ip
        # constant for all instances of the robot
        self.PORT = 9559
        # TODO: change this to use pickle
        self.com_dict = {"speech": 
                    {"hello robbie", "fire the trebuchet", "what is the time",
                    "how are you", "where are we", "what is this department",
                    "what is your favourite pathway"},
                "movement": 
                    {"can you sit down", "stand", "can you walk forward",
                    "come over here robbie", "can you walk backwards", 
                    "are you tired robbie"},
                "behaviours": 
                    {"can you play the guitar", "why don't you do some exercise",
                    "bless you"},
                "dance": 
                    {"do you feel like dancing", "show me your best dance moves",
                    "do you know thriller"},
                "stop": {"it is time to stop", "can you please stop that movement"} 
                } 
        # checks move is a motion proxy
        if type(motion_proxy) is ALProxy:
            self.motion_proxy = motion_proxy
            raise Exception("DEBUG -- motion proxy not set when passed to Speech class") 
        self.tts = Other(self.IP, self.PORT)
        self.bhv = Behaviour(self.motion_proxy, self.tts, bhv_file, bhv_dir)
        # setting up audio device for speech recognition
        self.mic = Microphone(log_dir)
        self.mic_enabled = self.mic.mic_check()
        if not self.mic_enabled:
            print("Cannot find appropriate microphone, speech recognition disabled")
        else:
            self.sr = self.mic.get_sr()

    def rec_speech(self):
        """
        Method to call to run speech recognition
        """
        command = ''
        
        while command != None:
            command = self.mic.rec_audio()
            self.check_command(command)

    def check_command(self, command):
        """
        Gets the robot to perform actions based an audio input from the user

        Keyword arguments:
        command -- a string of the audio input for the robot
        """
        command = command.lower()

        for key in self.com_dict:
            if command in self.com_dict[key]:
                self.run_command(key, command)
            else:
                self.tts.speak("I don't recognise that command!")
    
    def run_command(self, key, command):
        """
        The parent method to each type of action for the robot
        all other methods that get the robot to act are called from here

        Keyword arguments:
        key -- the key of the command dictionary to check which sub-method to call
        command -- used to trigger certain actions in the sub-methods
        """
        # checks whether to stop first for efficiency (doesn't have to check other dictionary keys)
        if key == "stop":
            self.motion_proxy.behaviour(behaviour_name="stop")
        elif key == "speech":
            self.run_speech(command)
        elif key == "movement":
            self.run_mv(command)
        elif key == "behaviours":
            self.bhv.run_bhv(command)
        elif key == "dance":
            self.bhv.run_dance(command)  
    
    def greeting(self):
        self.tts.speak(random.choice(self.bhv.greeting_list))

    def emotion(self):
        self.tts.speak(random.choice(self.bhv.emotions_list))

    def run_speech(self, command):
        """
        Runs methods that only require the robot to speak

        Keyword arguments:
        command -- used to check what the robot should say
        """
        if command == "hello" or command == "hello robbie":
            self.greeting()
        elif command == "what is the time" or command == "what time is it":
            # formats the current time into a speakable format for the robot
            now = datetime.datetime.now()
            hour = now.hour
            if hour > 12:
                hour -= 12
                meridiem = 'pm'
            else:
                meridiem = 'am'
            self.tts.speak("The time is {}:{} {}".format(hour, now.minute, meridiem))
        elif command == "how are you" or command == "how are you robbie":
            self.emotion()

        elif command == "where are we":
            self.tts.speak("We are at Edge Hill University, situated in the north-western town of Ormskirk")
            
        elif command == "what is this department":
            self.tts.speak("this is the computer science department, which has a wide variety of courses!")
            
        elif command == "what is your favourite pathway":
            self.tts.speak("BSc Robotics and Artificial Intelligence of course!")

    def run_mv(self, command):
        """
        Runs primitive movement related methods for the robot

        Keyword arguments:
        command -- determines what movement the robot will perform
        """
        if command == "can you sit down":
            self.tts.speak("Time for a sit down!")
            self.motion_proxy.posture("Sit")
            
        elif command == "stand":
            self.tts.speak("Standing up!")
            self.motion_proxy.posture("StandInit")
            
        elif command == "can you walk forwards" or command == "come over here robbie":
            self.tts.speak("Get ready to catch me!")
            self.motion_proxy.walk_fw_set()
            
        elif command == "can you walk backwards":
            self.tts.speak("Get ready to catch me!")
            self.movmotion_proxye.walk_bk_set()
            
        elif command == "are you tired robbie":
            self.tts.speak("yawn... time for a lie down")
            self.motion_proxy.posture("LyingBack") 

class Microphone():
    def __init__(self, audio_log):
        self.s_rec = sr.Recognizer()
        self.log = audio_log
        # default values, can change depending on factors for each constant
        self.MIC = 1
        self.T_OUT = 5
        self.T_LIMIT = 10

    def mic_check(self):
        """
        Checks if there are any microphones enabled on the computer
        For use in the Speech class to ensure that speech can be recognised

        Returns:
        mic_status -- boolean that is True if there are available microphones
        """
        mics = []
        mic_status = False

        for _, name in enumerate(sr.Microphone.list_microphone_names()):
            mics.append(name)
        # if any microphones are found then this will be true
        if len(mics) != 0:
            mic_status = True

        return mic_status

    def get_sr(self):
        """
        Returns an instance of a speech recognition object to be used
        by any speech recognition methods
        
        Returns:
        s_rec -- an instance of the Python speech recognition object
        """
        return self.s_rec

    def rec_audio(self):
        """
        Recognises audio input baed on microphone input

        Returns:
        audio_log -- the most recent sentence that has been detected as a string
        """
        data = []
        t_now = time.time()
        t_struct = time.localtime(t_now)

        with sr.Microphone(self.MIC) as src:
            audio = self.s_rec.listen(src, timeout=self.T_OUT, phrase_time_limit=self.T_LIMIT)
            print("--- End of phrase ---")

        try:
            audio_log = self.s_rec.recognize_google(audio)
            print("at {} user said {}".format(time.asctime(t_struct), audio_log))
            data.append(audio_log)

            with open(self.log, 'a') as f:
                for sample in data:
                    f.write(sample + '\n')
        
        except sr.UnknownValueError:
            print("Audio not understood, please try again")

        except sr.RequestError as req_err:
            print("could not request results from google API {}".format(req_err))

        except sr.WaitTimeoutError:
            print("Audio timed out, ending the process...")
            audio_log = None

        return audio_log

class Behaviour():
    def __init__(self, motion_proxy, tts, f_name, _dir = ''):
        self.BHV_LBL = "behaviour"
        self.DNC_LBL = "dance"
        self.motion_proxy = motion_proxy
        self.tts = tts

        self.bhvs = self.deserialise_behaviours(f_name, _dir)
        self.greeting_list = next(self.bhvs)
        self.emotions_list = next(self.bhvs)
        self.dance_dict = next(self.bhvs)
        self.bhv_dict = next(self.bhvs)

    def deserialise_behaviours(self, f_name, _dir):
        """
        Unpickles a given .pkl file and stores the containers in a generator

        Returns:
        items -- a generator containing dictionaries and lists related to behaviours
        """
        items = pl.get_list(f_name, _dir)
        return items

    def call_act(self, action, act_type=''):
        """
        Calls the motion_proxy's behaviour method using a given action

        Keyword arguments:
        action -- key of the respective dictionary that contains the path to the behaviour on the robot
        act_type -- either behaviour or dance, depending on the action to be performed
        """
        if act_type == "behaviour":
            self.motion_proxy.behaviour(behaviour_name=self.bhv_dict[action])
        elif act_type == "dance":
            self.motion_proxy.behaviour(behaviour_name=self.dance_dict[action])

    def run_bhv(self, command):
        """
        Gets the robot to run one of its installed behaviours

        Keyword arguments:
        command -- the behaviour for the robot to perform
        """
        if command == "can you play the guitar":
            self.call_act("air guitar", self.BHV_LBL)
        elif command == "why don't you do some exercise" or command == "can you do push-ups":
            self.call_act("pushups", self.BHV_LBL)
        elif command == "bless you":
            self.call_act("sneeze", self.BHV_LBL)

    def run_dance(self, command):
        """
        Makes the robot peform various dances

        Keyword arguments:
        command -- the dance for the robot to perform
        tts_proxy -- the text to speech proxy to allow the robot to speak
        """
        if command == "do you know thriller":
            self.tts.speak("perhaps I do...")
            # robbie needs a little break to psyche himself up...
            time.sleep(1)
            self.call_act("thriller", self.DNC_LBL)
        elif command == "do you feel like dancing":
            _, dance = random.choice(self.bhv.dance_dict.keys())
            self.call_act(dance, self.DNC_LBL)    
        elif command == "show me your best dance moves":
            self.call_act("caravan palace", self.DNC_LBL)