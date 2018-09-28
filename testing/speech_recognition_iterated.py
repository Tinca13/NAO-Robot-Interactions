"""
Author: Erik Thomas 28-09-18

TODO: 
    -- Store commands in .csv file with three columns:
        - Type: greeting, behaviour etc.
        - Command: the speech command related to each action
        - Action: speech output or behaviour to perform, call relevant method
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
        self.com_dict = pl.get_list(com_file, com_dir)
        # checks move is a motion proxy
        if type(motion_proxy) is ALProxy:
            self.motion_proxy = motion_proxy
            raise Exception("DEBUG -- motion proxy not set when passed to Speech class") 
        self.tts = Other(self.IP, self.PORT)
        self.bhv = Behaviour(bhv_file, bhv_dir)
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
            command = self.mic.audio_log()
            self.commands(command)

    def check_command(self, command):
        """
        Gets the robot to perform actions based an audio input from the user

        Keyword arguments:
        command -- a string of the audio input for the robot
        """
        # FIXME: needs to read based on command's category, and have an output string
        command = command.lower()

        for key in self.com_dict:
            if command in self.com_dict[key]:
                self.run_command(key)
            else:
                self.tts.speak("I don't recognise that command!")
    
    def run_command(self, key):
        # FIXME: to be used with check_command, requires update
        pass
        
    def greeting(self, command):
        self.tts.speak(random.choice(self.bhv.greeting_list))
        self.run_bhv(action=command)
    
    def emotion(self, command):
        self.tts.speak(random.choice(self.bhv.emotions_list))

    def run_bhv(self, action):
        self.motion_proxy.behaviour(behaviour_name=self.bhv.bhv_dict[action])

class Microphone():
    def __init__(self, audio_log):
        self.s_rec = sr.Recognizer()
        self.audio_log = audio_log
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
        curr_time = time.time()
        time_struct = time.localtime(curr_time)

        with sr.Microphone(self.MIC) as src:
            audio = self.s_rec.listen(src, timeout=self.T_OUT, phrase_time_limit=self.T_LIMIT)
            print("--- End of phrase ---")

        try:
            audio_log = self.s_rec.recognize_google(audio)
            print("at {} user said {}".format(time.asctime(time_struct), audio_log))
            data.append(audio_log)

            with open(self.audio_log, 'a') as log:
                for sample in data:
                    log.write(sample + '\n')
        
        except self.s_rec.UnknownValueError:
            print("Audio not understood, please try again")

        except self.s_rec.RequestError as req_err:
            print("could not request results from google API {}".format(req_err))

        except self.s_rec.WaitTimeoutError:
            print("Audio timed out, ending the process...")
            audio_log = None

        return audio_log

class Behaviour():
    def __init__(self, f_name, _dir = ''):
        self.bhvs = self.deserialise_behaviours(f_name, _dir)
        self.greeting_list = next(self.bhvs)
        self.emotions_list = next(self.bhvs)
        self.dance_dict = next(self.bhvs)
        self.bhv_dict = next(self.bhvs)

    def deserialise_behaviours(self, f_name, _dir):
        items = pl.get_list(f_name, _dir)
        return items