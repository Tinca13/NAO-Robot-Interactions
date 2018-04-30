# -*- coding: utf-8 -*-
"""
Created on Thu Feb 08 15:26:05 2018

@author: 23008318
"""

import yaml
import os
import cv2
import numpy as np
import time
import thread
from movement import Movement
from new_joint import Joint
from PIL import Image

#"D:/OpenPose_demo_1.0.1/OpenPose_demo_1.0.1"
#empty openpose directory dynamically
class Gestures():
    def __init__(self, openpose_dir, yml_dir, image_dir):
        #add image path
        self.openpose_dir = openpose_dir
        self.yml_dir = yml_dir
        self.image_dir = image_dir
        self.no_people = False
        self.movement = Movement("169.254.65.171", 9559)
        self.joint = Joint("Head", "169.254.65.171", 9559)
        self.current_file = ''
        #other     
        self.nose = (0,0,0)
        self.neck = (0,0,0)
        #right        
        self.r_shoulder = (0,0,0)
        self.r_elbow = (0,0,0)
        self.r_wrist = (0,0,0)
        self.r_hip = (0,0,0)
        self.r_knee = (0,0,0)
        self.r_ankle = (0,0,0)
        self.r_eye = (0,0,0)
        self.r_ear = (0,0,0)
        #left     
        self.l_shoulder = (0,0,0)
        self.l_elbow = (0,0,0)
        self.l_wrist = (0,0,0)
        self.l_hip = (0,0,0)
        self.l_knee = (0,0,0)
        self.l_ankle = (0,0,0)
        self.l_eye = (0,0,0)
        self.l_ear = (0,0,0)

        self.prev_poses = []
        self.l_arm_state = -1
        self.r_arm_state = -1
        self.l_arm_prev_state = -1
        self.r_arm_prev_state = -1
        
    def openpose(self):
        #Do not change this directory (unless on different PC)
        os.chdir(self.openpose_dir)
        #Change the directories if required
        os.system("bin\\OpenPoseDemo.exe --image_dir " + self.image_dir + " --write_keypoint " + self.yml_dir + " --no_display")        
    
    def draw_all(self, chunks, im_path):
        im_path = im_path[:len(im_path)-9] + '.jpg'
        image = cv2.imread(im_path)
        count = 0
        for joint in chunks:  
            font = cv2.FONT_HERSHEY_SIMPLEX
            x,y,score = joint
            cv2.circle(image, (int(x), int(y)), 10, (255,0,0), -1)
            cv2.putText(image,str(count),(int(x), int(y)), font, 1,(0,0,255),2,cv2.LINE_AA)
            count += 1
            
        cv2.imshow("what", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def draw_joint(self, j, im_path):
        im_path = im_path[:len(im_path)-9] + '.jpg'
        image = cv2.imread(im_path)
        prev_joint = j[0]
        for joint in j:  
            x,y,score = joint
            cv2.circle(image, (int(x), int(y)), 10, (255,0,0), -1)
            cv2.line(image, (int(prev_joint[0]),int(prev_joint[1])), (int(joint[0]),int(joint[1])), (0,0,255), 4)
            prev_joint = joint
        cv2.imshow("what", image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
    def angle_calc(self, joint1, joint2, joint3):
        x1 = joint2[0] - joint1[0]
        y1 = joint2[1] - joint1[1]
        
        x2 = joint2[0] - joint3[0]
        y2 = joint2[1] - joint3[1]

        if x1 == 0 or x2 == 0 or y1 == 0 or y2 == 0:
            return 0
        
        #length of each vector
        len_a = np.sqrt(x1**2 + y1**2)
        len_b = np.sqrt(x2**2 + y2**2)
        #dot product
        dot_product = (x1 * x2) + (y1 * y2)
        #performs the calculation: 
        #dot_product of vectors over the length of each vector multiplied together
        cos_a = dot_product / (len_a * len_b)
        #gets the true angle from the cos value...
        angle = np.arccos(cos_a)
        #... and converts it to degrees (bonus step, can be removed)
        angle = np.degrees(angle)
        return angle
    
    def get_skeleton(self):
        for root, dirs, files in os.walk(self.yml_dir):
            try:
                self.current_file = files[len(files)-1]
            except:
                return
            
        skele_path = self.yml_dir + '/' + self.current_file
        skip_lines = 2
        #Reads directory of .yml files
        with open(skele_path) as yml_obj: #skele_path is the directory for .yaml files
            for i in range(skip_lines):
                #Deletes first two lines of file
                _ = yml_obj.readline()
            #Gets remainder of file
            full_data = yaml.load(yml_obj)
        
        try:
            #Gets sizes feature (tag)
            size_data = full_data['sizes']
            #Gets how many people are in frame
            num_people = size_data[0]
            #Gets all skeleton data    
            skeles = full_data['data']
            #Gets number of values in each person's sections
            single_skeleton = int(len(skeles) / int(num_people))
            self.assign_joints(single_skeleton, skeles, num_people)
        
        except:
            print("no people in {}".format(self.current_file))
            #self.movement.tts.speak("No person found")
            self.no_people = True
            
            
    def assign_joints(self, single_skeleton, skeles, num_people):
        for person in range(1, num_people + 1):
            chunks = [skeles[x:x+3] for x in range(int(single_skeleton * (person-1)), single_skeleton * person, 3)]
            #other     
            self.nose = chunks[0]
            self.neck = chunks[1]
            #right        
            self.r_shoulder = chunks[2]
            self.r_elbow = chunks[3]
            self.r_wrist = chunks[4]
            self.r_hip = chunks[8]
            self.r_knee = chunks[9]
            self.r_ankle = chunks[10]
            self.r_eye = chunks[14]
            self.r_ear = chunks[16]
            #left     
            self.l_shoulder = chunks[5]
            self.l_elbow = chunks[6]
            self.l_wrist = chunks[7]
            self.l_hip = chunks[11]
            self.l_knee = chunks[12]
            self.l_ankle = chunks[13]
            self.l_eye = chunks[15]
            self.l_ear = chunks[17]
                
    def calc_angles(self):
        #works for right arm bent half, can be reapplied to all right arm movements
        angle_r = self.angle_calc(self.r_shoulder, self.r_elbow, self.r_wrist)
        angle_rsh = self.angle_calc(self.r_elbow, self.r_shoulder, self.r_hip)

        
        #left arm angle calculation
        angle_l = self.angle_calc(self.l_shoulder, self.l_elbow, self.l_wrist)
        angle_lsh = self.angle_calc(self.l_elbow, self.l_shoulder, self.l_hip)

        if angle_r == 0 or angle_rsh == 0:
            angle_r = 0
            angle_rsh = 0
        elif angle_l == 0 or angle_lsh == 0:
            angle_l = 0
            angle_lsh = 0
        
        return angle_r, angle_rsh, angle_l, angle_lsh
    
    def check_person_for(self):
        angle_r, angle_rsh, angle_l, angle_lsh = self.calc_angles()
        check_right = False
        check_left = False
        if angle_r != 0:
            check_right = True
            self.right_arm_state = -1
        if angle_r != 0:
            check_left = True
            self.left_arm_state = -1
        curr_gestures = []

        if check_right:
            #--------------------------------right arm checks--------------------------------
            if 75 <= angle_r <= 115 and 75 <= angle_rsh <= 105:
                #print("Right arm bent half in {}".format(self.current_file))
                #self.movement.tts.speak("Your right arm is bent half!")
                curr_gestures.append("rArm_bent_half")
                self.r_arm_state = 1
                
            elif 165 <= angle_r <= 195 and 75 <= angle_rsh <= 105:
                #print("Right arm straightened in {}".format(self.current_file))
                #self.movement.tts.speak("Your right arm is straightened!")
                curr_gestures.append("rArm_straight")
                self.r_arm_state = 0
                #self.movement.right_arm_out()
                
            elif 80 <= angle_r <= 120 and 30 <= angle_rsh <= 60:
                #print("Right hand on hip in {}".format(self.current_file))
                #self.movement.tts.speak("Your right hand is on your hip!")
                curr_gestures.append("rHand_hip")
                self.r_arm_state = 4
                #self.movement.hands_on_hips()
            
            elif 165 <= angle_r <= 195 and 0 <= angle_rsh <= 30:
                #print("Right arm straight down in {}".format(self.current_file))
                curr_gestures.append("rArm_down")
                self.r_arm_state = 2
                
            elif 165 <= angle_r <= 195 and 160 <= angle_rsh <= 200:
                #print("Right arm straight up in {}".format(self.current_file))
                curr_gestures.append("rArm_up")
                self.r_arm_state = 3
            else:
                self.r_arm_state = -1
        else:
            #print("your right arm has been chopped off")
            pass
        
        if check_left:
            #--------------------------------left arm checks--------------------------------  
            if 75 <= angle_l <= 115 and 75 <= angle_lsh <= 105:
                #print("Left arm bent half in {}".format(self.current_file))
                #self.movement.tts.speak("Your left arm is bent half!")
                curr_gestures.append("lArm_bent_half")
                self.l_arm_state = 1
                
            elif 165 <= angle_l <= 195 and 75 <= angle_lsh <= 105:
                #print("Left arm straightened in {}".format(self.current_file))
                #self.movement.tts.speak("Your left arm is straightened!")
                curr_gestures.append("lArm_straight")
                self.l_arm_state = 0
                
            elif 80 <= angle_l <= 120 and 30 <= angle_lsh <= 60:
                #print("Left hand on hip in {}".format(self.current_file))
                #self.movement.tts.speak("Your left hand is on your hip!")
                curr_gestures.append("lHand_hip")
                self.l_arm_state = 4
                #self.movement.hands_on_hips()
            
            elif 165 <= angle_l <= 195 and 0 <= angle_lsh <= 30:
                #print("Left arm straight down in {}".format(self.current_file))
                curr_gestures.append("lArm_down")
                self.l_arm_state = 2
                
            elif 165 <= angle_l <= 195 and 160 <= angle_lsh <= 200:
                #print("Left arm straight up in {}".format(self.current_file))
                curr_gestures.append("lArm_up")
                self.l_arm_state = 3
            else:
                self.l_arm_state = -1
        else:
            #print("your left arm has been chopped off")
            pass
    def arm_state_check(self):
        if self.l_arm_state == -1:
            #print("left arm dead")
            pass
        elif self.l_arm_state == self.l_arm_prev_state:
            #print("same left arm gesture")
            pass
        elif self.l_arm_state == 0:
            print("Left arm straightened in {}".format(self.current_file))
            self.movement.tts.speak("left arm straight!")
            self.l_arm_prev_state = 0
            self.movement.left_arm_out()
        elif self.l_arm_state == 1:
            print("Left arm bent half in {}".format(self.current_file))
            self.movement.tts.speak("left arm half bent!")
            self.l_arm_prev_state = 1
            self.movement.left_arm_out_bend_up()
        elif self.l_arm_state == 2:
            print("Left arm straight down in {}".format(self.current_file))
            self.movement.tts.speak("left arm straight down")
            self.l_arm_prev_state = 2
            self.movement.left_arm_down()
        elif self.l_arm_state == 3:
            print("Left arm straight up in {}".format(self.current_file))
            self.movement.tts.speak("left arm straight up")
            self.l_arm_prev_state = 3
            self.movement.left_arm_straight_up()
        elif self.l_arm_state == 4:
            print("Left hand on hip in {}".format(self.current_file))
            self.movement.tts.speak("left hand on hip")
            self.l_arm_prev_state = 4
            self.movement.left_hand_hip()
        else:
            print("how did you break me")

        
        if self.r_arm_state == -1:
            #print("right arm dead")
            pass
        elif self.r_arm_state == self.r_arm_prev_state:
            #print("same right arm gesture")
            pass
        elif self.r_arm_state == 0:
            print("Right arm straightened in {}".format(self.current_file))
            self.movement.tts.speak("right arm straight")
            self.r_arm_prev_state = 0
            self.movement.right_arm_out()
        elif self.r_arm_state == 1:
            print("Right arm bent half in {}".format(self.current_file))
            self.movement.tts.speak("right arm half bent")
            self.r_arm_prev_state = 1
            self.movement.right_arm_out_bend_up()
        elif self.r_arm_state == 2:
            print("Right arm straight down in {}".format(self.current_file))
            self.movement.tts.speak("right arm straight down")
            self.r_arm_prev_state = 2
            self.movement.right_arm_down()
        elif self.r_arm_state == 3:
            print("Right arm straight up in {}".format(self.current_file))
            self.movement.tts.speak("right arm straight up")
            self.r_arm_prev_state = 3
            self.movement.right_arm_straight_up()
        elif self.r_arm_state == 4:
            print("Right hand on hip in {}".format(self.current_file))
            self.movement.tts.speak("right hand on hip")
            self.r_arm_prev_state = 4
            self.movement.right_hand_hip()
        else:
            print("how did you break me")

            
    def folder_fill(self, _range):
        zeroes = '00000000'
        image = Image.new('RGB', (10, 10), color='black')
        for im in range(_range):
            #your directory here
            im_len = len(str(im))
            zeroes_new = zeroes[:(len(zeroes)-im_len)] + str(im)
            image.save(self.image_dir + zeroes_new + '.jpg')
            
    def clear_folder(self):
        for yml_file in os.listdir(self.yml_dir):
            file_path = os.path.join(self.yml_dir, yml_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            
            except Exception as e:
                print("The following exception was thrown in clear_folder {}".format(e))

gesture = Gestures("D:/OpenPose_demo_1.0.1/OpenPose_demo_1.0.1", "D:/OpenPose_Outputs", "D:/OpenPose_Blank")
gesture.clear_folder()
gesture.folder_fill(1000)
thread.start_new_thread(gesture.openpose, ())
gesture.joint.stiffen("Head", 0.0)
try:
    while True:
        gesture.get_skeleton()
        #thread.start_new_thread(gesture.check_person_for, ())
        gesture.check_person_for()
        gesture.arm_state_check()
        #print("loop")
        #gesture.draw_joint([gesture.r_shoulder, gesture.r_elbow, gesture.r_wrist], gesture.current_file)
        time.sleep(0.2)
except KeyboardInterrupt:
    gesture.joint.release("Head")
    print("goodbye cruel world")
