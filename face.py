from naoqi import ALProxy
import vision_definitions as vd
import numpy as np
import string
import random


class Face():
    
    def __init__(self, tts_proxy, video_proxy, camera_resolution=vd.kQVGA, camera_colour=vd.kBGRColorSpace, camera_fps=24):
        self.camera_resolution = camera_resolution
        self.camera_colour = camera_colour
        self.camera_fps = camera_fps
        self.video_proxy = video_proxy
        self.top_camera_id = self.subscribe_to_camera(0)
        self.bottom_camera_id = self.subscribe_to_camera(1)
        self.mouth_proxy = tts_proxy
        
    #Done - untested
    def speak(self, message, language="English", pitch=100, speed=100, volume=60):
        if language != "English":
            self.mouth_proxy.setLanguage(language)
        self.mouth_proxy.say("\\vct={}\\\\rspd={}\\\\vol={}\\{}".format(pitch, speed, volume, message))
    
    def eye_colour(self):
        pass
    
    
    #Done - untested
    def subscribe_to_camera(self, camera=None):
        print("camera: " + str(camera))
        if camera != None:
            self.camera = camera
        else:
            print("camera not accepted")
            return
        
        if camera == 0:
            try:
                self.video_proxy.unsubscribe(self.top_camera_id)
            except:
                print("Error unsubbing from top camera")
                pass
            print("Subscribed to camera " + str(camera))
            return self.video_proxy.subscribeCamera(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100)), 0, self.camera_resolution, self.camera_colour, self.camera_fps)
        elif camera == 1:
            try:
                self.video_proxy.unsubscribe(self.bottom_camera_id)
            except:
                print("Error unsubbing from bottom camera")
                pass
            print("Subscribed to camera " + str(camera))
            return self.video_proxy.subscribeCamera(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100)), 1, self.camera_resolution, self.camera_colour, self.camera_fps)
        else:
            raise ValueError("Camera value not valid")
        
          
    #Done - untested
    def get_image(self, camera=0):
        if camera == 0:
            result = self.video_proxy.getImageRemote(self.top_camera_id)
            img = self.remake_img(result)
        if camera == 1:
            result = self.video_proxy.getImageRemote(self.bottom_camera_id)
            img = self.remake_img(result)
        return img
    
    def remake_img(self, result):
        if result == None:
            return np.zeros((360,240,3), dtype=np.uint8)
        
        width = result[0]
        height = result[1]
        image = np.zeros((height, width, 3), np.uint8)
        
        values = map(ord, list(result[6]))
        i = 0
        for y in range(0, height):
            for x in range(0, width):
                image.itemset((y, x, 0), values[i + 0])
                image.itemset((y, x, 1), values[i + 1])
                image.itemset((y, x, 2), values[i + 2])
                i += 3
        return image

    def unsub(self):
        try:
            self.video_proxy.unsubscribe(self.top_camera_id)
        except:
            pass
        try:
            self.video_proxy.unsubscribe(self.bottom_camera_id)
        except:
            pass