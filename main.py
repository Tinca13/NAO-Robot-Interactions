from naoqi import ALProxy
from face import Face
from brain import Brain
from body import Body
from ears import Speech
import cv2
import time
import os
from threading import Thread
#test GitHUB

class Robot():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.name = self.set_name()
        self.face = self.init_face()
        self.body = Body(self, ALProxy("ALMotion", ip, port), ALProxy("ALAutonomousMoves", ip, port))
        self.brain = Brain(self)
        self.ears = Speech(self, "robot_behaviours.pkl", "pkl_sources/", "extra_info/audio_log.txt")
    
    #Done - untested
    def init_face(self):
        tts_proxy = ALProxy("ALTextToSpeech", self.ip, self.port)
        video_proxy = ALProxy("ALVideoDevice", self.ip, self.port)
        return Face(tts_proxy, video_proxy)
    
    #Done - untested
    def set_name(self):
        name = ""
        if ip == "169.254.65.171":
            name = "Robbie"
        # FIXME: update to correct IP when testing
        elif ip == "2":
            name = "Bert"
        else:
            name = "... Oh God... Who am I? Please help me!"
        return name
    
    def look_top(self, duration, display=True, save_dir="", overwrite=True):
        while duration != 0:
            top_img = self.face.get_image(0)
            if save_dir != "":
                self.save_img(top_img, "T", save_dir, overwrite)
            if display:
                cv2.imshow("camera_0", top_img)
                if cv2.waitKey(1) & 0xFF == 27:
                    cv2.destroyAllWindows()
                    break
            duration -= 1
            
        pass
    
    def look_bottom(self, duration, display=True, save_dir="", overwrite=True):
        while duration != 0:
            bottom_img = self.face.get_image(1)
            if save_dir != "":
                self.save_img(bottom_img, "T", save_dir, overwrite)
            if display:
                cv2.imshow("camera_1", bottom_img)
                if cv2.waitKey(1) & 0xFF == 27:
                    cv2.destroyAllWindows()
                    break
            duration -= 1
            
        pass
    
    def save_img(self, img, cam_name, save_dir, overwrite=True):
        if overwrite:
            cv2.imwrite(save_dir + "/00000000_{}.jpg".format(cam_name))
        else:
            i = 0
            while os.path.exists(save_dir + "/" + str(i).zfill(8) + "_{}.jpg".format(cam_name)):
                i += 1
            cv2.imwrite(save_dir + "/" + str(i).zfill(8) + "_{}.jpg".format(cam_name))
        pass

    def speak(self, message):
        self.face.speak(message)
        
    def listen(self):
        try:
            self.ears.rec_speech()
            return True
        except KeyboardInterrupt:
            return False
    

#Done - untested
def parse_args():
    try:
        #IP, PORT
        return "169.254.65.171", 9559
        #return sys.argv[1], sys.argv[2]
    except:
        raise ValueError("Error: Not enough arguments")


if __name__ == "__main__":
    try:
        ip, port = parse_args()
        robot = Robot(ip, port)
        #robot.face.speak("Hello there. I'm " + robot.name + " The Robot", pitch=100, speed=100)
        #robot.face.speak("Hello there. I'm " + robot.name + " The Robot. How you doin", pitch=50, speed=1, volume=75)
        #robot.face.speak("Save me Matt-chan. T, He", pitch=150, speed=70, volume=90)
        
        
        #t1 = Thread(target=robot.look_top, args=(-1, ))
        #t2 = Thread(target=robot.look_bottom, args=(-1, ))
        #t1.start()
        #t2.start()
        
        #raw_input("Main thread done")
            
        
        '''for x in range(0,50):
            img, camera_id = robot.look()
            resized_image = cv2.resize(img, (800, 600)) 
            cv2.imshow("camera_" + str(camera_id), resized_image)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        '''
        #robbie.brain.predict_age_gender()
        
        #robbie.body.toggle_awareness(hard_reset=True)
        #robbie.body.toggle_awareness()
        
        robot.body.head_turn("F")
        robot.body.head_up_down("F")
        robot.body.master_joint.stiffen("Head")
        
        
        '''
        while True:
            print("loop")
            img,_ = robot.look(False)
            cv2.imwrite("D:/RobotMaster/images/cap.jpg", img)
            names, scores, top_left, bottom_right = robot.brain.object_detection.predict()
            for name in names:
                print(name)
        '''
        
        robot.brain.predict_objects()
        #while True:
        #    robot.listen()
        #robot.brain.track_ball()
        
        #time.sleep(5)
        #robbie.body.toggle_awareness()
        
    except Exception as e:
        print("Error: " + str(e))
        raw_input("Wait")
    finally:
        robot.face.unsub()
        robot.body.posture.walk_stop()
        cv2.destroyAllWindows()
