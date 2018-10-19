"""
Author: Erik Thomas 28-09-18

TODO:
    -- Merge with updated movement refactor and test
    -- Review data structures for commands, make them more compact and easily expandable
    -- Create a small GUI to manage microphone setup and testing, as well as displaying speech output
    -- Make voice commands more robust, use in keyword more to allow for more fluid interactions
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
from audio import Audio

class Speech():
    def __init__(
                self, ip, motion_proxy, 
                bhv_file, bhv_dir, log_path, 
                ):
        self.IP = ip
        # constant for all instances of the robot
        self.PORT = 9559
        # TODO: change this to use pickle
        self.com_dict = {"speech": 
                    {"hello robbie", "fire the trebuchet", "what is the time",
                    "how are you", "where are we", "what is this department",
                    "what is your favourite pathway", "what is up dog"},
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
                "audio": 
                    {"robbie that is so sad", "it's time for a revolution"}
                } 
        self.STOP_KEYWORD = "stop"
        # checks move is a motion proxy
        self.motion_proxy = motion_proxy
        self.tts = Other(self.IP, self.PORT)
        self.audio = Audio(self.IP)
        self.bhv = Behaviour(self.motion_proxy, self.tts, bhv_file, bhv_dir)
        # setting up audio device for speech recognition
        self.mic = Microphone(log_path)
        self.mic_enabled = self.mic.mic_check()
        if not self.mic_enabled:
            print("Cannot find appropriate microphone, speech recognition disabled.")
        else:
            self.sr = self.mic.get_sr()

    def rec_speech(self):
        """
        Checks if speech was recognised to execute commands on the robot
        """
        command = ''
        
        while command != '{no-value}':
            command = self.mic.rec_audio()
            self.check_command(command)

    def check_command(self, command):
        """
        Gets the robot to perform actions based an audio input from the user

        Keyword arguments:
        command -- a string of the audio input for the robot
        """
        # all commands in the command dictionary are lower case for consistency
        command = command.lower()

        for key in self.com_dict:
            # checks whether to stop the robot first so all the other dictionary keys don't need to be checked
            if self.STOP_KEYWORD in command:
                self.motion_proxy.behaviour(behaviour_name="stop")
            elif command in self.com_dict[key]:
                self.run_command(key, command)
                break
    
    def run_command(self, key, command):
        """
        The parent method to each type of action for the robot
        all other methods that get the robot to act are called from here

        Keyword arguments:
        key -- the key of the command dictionary to check which sub-method to call
        command -- used to trigger certain actions in the sub-methods
        """
        if key == "speech":
            self.run_speech(command)
        elif key == "movement":
            self.run_mv(command)
        elif key == "behaviours":
            self.bhv.run_bhv(command)
        elif key == "dance":
            self.bhv.run_dance(command)
        elif key == "audio":
            self.run_audio(command)
    
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
            _, minute, hour, meridiem = Speech.format_time()
            self.tts.speak("The time is {}:{} {}".format(hour, minute, meridiem))
        elif command == "how are you" or command == "how are you robbie":
            self.emotion()

        elif command == "where are we":
            self.tts.speak("We are at Edge Hill University, situated in the north-western town of Ormskirk")
            
        elif command == "what is this department":
            self.tts.speak("this is the computer science department, which has a wide variety of courses!")
            
        elif command == "what is your favourite pathway":
            self.tts.speak("BSc Robotics and Artificial Intelligence of course!")

        elif command == "what is up dog":
            self.tts.speak("Nothimg much, whats up with you")

    def run_audio(self, command):
        """
        Using audio stored on the robot and an audio proxy, from the naoqi library, an audio file can be played

        Keyword arguments:
        command -- used to check what audio the robot should play

        TODO: add threading capability to allow other actions whilst playing a song
        """
        if command == "robbie that is so sad":
            self.tts.speak("Wow that is so sad... Now playing despacito by Luis Fonsi")
            self.audio.play_audio(file_name="secret_song")
        elif command == "it's time for a revolution":
            self.audio.play_audio(file_name="one_day_more")

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
            self.motion_proxy.walk_bk_set()
            
        elif command == "are you tired robbie":
            self.tts.speak("yawn... time for a lie down")
            self.motion_proxy.posture("LyingBack")
    
    @staticmethod
    def format_time(audio=''):
        """
        Acquires the current time in minutes, hours and the meridiem (am or pm)
        and formats it into a readable string output

        Returns:
        now.minute -- the current time (minutes)
        hour -- the current time (hours)
        meridiem -- a string stating whether it is currently am or pm
        """
        now = datetime.datetime.now()
        hour = now.hour

        if hour > 12:
            hour -= 12
            meridiem = 'pm'
        else:
            meridiem = 'am'

        time_str = "at {1}:{0}{2} user said: {3}".format(now.minute, hour, meridiem, audio)

        return time_str, now.minute, hour, meridiem

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

        with sr.Microphone(self.MIC) as src:
            audio = self.s_rec.listen(src, timeout=self.T_OUT, phrase_time_limit=self.T_LIMIT)
            print("--- End of phrase ---")

        try:
            audio_log = self.s_rec.recognize_google(audio)
            print(Speech.format_time(audio_log))
            data.append(audio_log)

            with open(self.log, 'a') as log_file:
                for sample in data:
                    log_file.write(Speech.format_time(sample))
        
        except sr.UnknownValueError:
            print("Audio not understood, please try again")
            audio_log = '{no-value}'

        except sr.RequestError as req_err:
            print("could not request results from google API {}".format(req_err))
            audio_log = '{no-value}'

        except LookupError:
            print("Audio timed out, ending the process...")
            audio_log = '{no-value}'
            
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
            _, dance = random.choice(self.dance_dict.keys())
            self.call_act(dance, self.DNC_LBL)    
        elif command == "show me your best dance moves":
            self.call_act("caravan palace", self.DNC_LBL)

def call_method(speech):
    try:
        speech.rec_speech()
        return True
    except KeyboardInterrupt:
        return False

if __name__ == "__main__":
    IP = "192.168.1.129"
    motion_proxy = Movement(IP, 9559)
    bhv_pkl_file = "robot_behaviours.pkl"
    # change paths when required
    bhv_dir = "G:\\Programming\\RemoteSandbox\\NAO-Robot-Interactions\\pkl_sources\\"
    log_path = "G:\\Programming\\RemoteSandbox\\NAO-Robot-Interactions\\extra_info\\audio_log.txt"
    # FIXME: properly pass motion_proxy from other files
    speech = Speech(IP, motion_proxy, bhv_pkl_file, bhv_dir, log_path)
    check_speech = True
    # while loop required to constantly run speech recognition over a long period of time
    while check_speech:
        check_speech = call_method(speech)
    
