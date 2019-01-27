#import openpose
import socket
import os
import math
from subprocess import Popen

import cv2
import numpy as np
#from keras.applications.inception_v3 import preprocess_input
#from keras.models import load_model

class Brain():
    def __init__(self, robot):
        self.robot = robot
        self.body = robot.body
        #self.pose = OpenPoseAPI()
        self.object_detection = Object_Detection()
        #self.HOI = Human_Object_Interaction(self.pose, self.object_detection)
        #self.mirror_pose = Pose_Mirroring(self.pose)
        self.age_gender = Age_Gender()
        self.football = Play_Football(self.body)
    
    def predict_age_gender(self):
        self.age_gender.start()
    
    def predict_objects(self):
        try:
            while True:
                img = self.robot.face.get_image()
                cv2.imwrite("D:/RobotMaster/images/cap.jpg", img)
                objs = self.object_detection.predict()
                if len(objs) > 0:
                    self.robot.face.speak("I can see: ", pitch=150, speed=1, volume=90)
                    self.robot.face.speak("Sports ball", pitch=150, speed=1, volume=90)
                    for obj in objs:
                        print(obj[0])
                        self.robot.face.speak(obj[0], pitch=150, speed=1, volume=90)
                print("~~~~~END OF OBJECTS~~~~~")
        except Exception as e:
            
            print(e)
            print("Server closed")
            self.object_detection.close_server()
        
    def predict_interaction(self):
        img = self.body.look()
        cv2.imwrite("D:/RobotMaster/img/cap.jpg", img)
        relations = self.HOI.calculate_HOI()
        print(relations)

    def predict_pose(self):
        img = self.body.look()
        pose = self.mirror_pose.get_pose(img)
        print(pose)
    
    def track_ball(self, im_width=800, im_height=600):
        self.football.start_walk()
        default_width = 640
        default_height = 480
        side_step_dir = ""
        should_run = True
        BALL_IN_SIGHT = False
        
        self.robot.speak("Looking for ball")
        while should_run:
            img = self.robot.face.get_image()
            secret_img, x, y = self.football.apply_mask(img)
            try:
                x = int(x)
                y = int(y)
                #Walk forward until the ball is found
                cv2.circle(secret_img,(x,y), 5, (0,0,255), -1)
                if side_step_dir != "":
                    self.football.stop_walk()
                #move to the side until the ball is centered
                if x*2 < (default_width / 2) - (default_width / 10):
                    if side_step_dir != "L":
                        print("LEFT")
                        self.robot.speak("Ball is to the left")
                        side_step_dir = "L"
                    self.football.start_walk(x_dir=0.0, y_dir=-0.5, theta=0.0, freq=0.5)
                elif x*2 > (default_width / 2) + (default_width / 10):
                    if side_step_dir != "R":
                        print("RIGHT")
                        self.robot.speak("Ball is to the right")
                        side_step_dir = "R"
                    self.football.start_walk(x_dir=0.0, y_dir=-0.5, theta=0.0, freq=0.5)
                else:
                    self.football.stop_walk()
                    self.robot.speak("Ball is dead ahead")
                    print("CENTERED")
                    BALL_IN_SIGHT = True
                    break
                    
            except ValueError as e:
                pass
            except Exception as e:
                print(str(e))
                #print("no circle")
                pass
            #cv2.imshow("average", cv2.resize(smoothed, (800, 600)))
            cv2.imshow("BALL_FINDER_V0.1", cv2.resize(secret_img, (im_width, im_height)))
            #cv2.imshow("default", cv2.resize(img, (800, 600)))
            if cv2.waitKey(1) & 0xFF == 27:
                should_run = False
        
        if BALL_IN_SIGHT:
            should_run = True
            self.football.start_walk()
        else:
            should_run = False
            
        while should_run:
            img = self.robot.face.get_image(camera=1)
            secret_img, x, y = self.football.apply_mask(img)
            try:
                x = int(x)
                y = int(y)
                cv2.circle(secret_img,(x,y), 5, (0,0,255), -1)
                    
            except ValueError as e:
                self.robot.speak("I HAVE THE BALL")
                self.body.posture.crouch()
                break
                pass
            except Exception as e:
                print(str(e))
                #print("no circle")
                pass
            #cv2.imshow("average", cv2.resize(smoothed, (800, 600)))
            cv2.imshow("BALL_FINDER_V0.1", cv2.resize(secret_img, (im_width, im_height)))
            #cv2.imshow("default", cv2.resize(img, (800, 600)))
            if cv2.waitKey(1) & 0xFF == 27:
                should_run = False
        #cv2.destroyAllWindows()
    
class OpenPoseAPI():
    def __init__(self):
        self.pose_dectection = self.init_openpose()
        self.joint_names = ['nose','neck','rshoulder','relbow','rwrist','lshoulder','leblow','lwrist','midhip','rhip','rknee','rankle','lhip','lknee','reye','leye', 'rear', 'lear', 'lbigtoe', 'lsmalltoe', 'lheel', 'rbigtoe', 'rsmalltoe', 'rheel', 'background']
        pass
    
    #Done - untested
    def init_openpose(self):
        params = dict()
        params["logging_level"] = 3
        params["output_resolution"] = "-1x-1"
        params["net_resolution"] = "-1x368"
        params["model_pose"] = "BODY_25"
        params["alpha_pose"] = 0.6
        params["scale_gap"] = 0.3
        params["scale_number"] = 1
        params["render_threshold"] = 0.05
        params["num_gpu_start"] = 0
        params["disable_blending"] = False
        params["default_model_folder"] = "../../../models/"
        return OpenPose(params)
    
    #Done - untested
    def get_pose(self, image):
        image = cv2.imread("D:/RobotMaster/images/cap.jpg")
        keypoints = self.pose_dectection.forward(image, False)
        return keypoints
    
    #Done - untested
    def keypoints_to_joint_names(self, keypoints):
        joints = []
        try:
            for i in range(0, len(keypoints)):
                print(i)
                joints.append([self.joint_names[i], keypoints[i]])
            
            return joints
        except:
            #If there are no joints in the frame, return an empty joint list for 1 person
            joints = []
            print("No Joints")
            for i in range(0, 25):
                joints.append([self.joint_names[i], [0,0,0]])
            return joints
    
    #Done - untested
    def get_keypoint_by_name(self, keypoints, joint_name):
        joints = self.keypoints_to_joint_names(keypoints)
        for name in joints:
            if name[0] == joint_name:
                return name[1]
        print("JOINT NOT FOUND")
        return False

class Object_Detection():
    def __init__(self, model_name="faster_rcnn_resnet101_coco_11_06_2017", class_file_name="D:/RobotMaster/res/classDictionary.txt"):
        self.server, self.object_detection_client = self.init_remote_model()
        self.class_file = open(class_file_name, "r")
        pass
    
    #Done - untested
    def get_name_from_index(self, class_id):
        objects = self.class_file.read().splitlines()
        return objects[class_id]
    
    #Done - untested
    def init_remote_model(self):
        server_name = 'localhost'
        server_port = 33605
        
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((server_name, server_port))
        serverSocket.listen(1)
        print("Opening server")
        try:
            while True:
                client, _ = serverSocket.accept()
                break
        except:
            print("Trying server")                
        
        print("Connection made")
        return serverSocket, client

    #Done - untested
    def predict(self):
        print("Telling obj to start")
        self.object_detection_client.send("GO".encode(encoding="utf-8"))
        objects_found = self.object_detection_client.recv(1024).decode()
        print("Objects found: {}".format(objects_found))
        
        obj_list = []
        for i in range(int(objects_found)):
            obj_list.append(str(self.object_detection_client.recv(1024).decode()))
            print(obj_list)
        print("Got all items")
        names = []
        scores = []
        top_left = []
        bottom_right = []
        for obj in obj_list:
            data = obj.split(",")
            names.append(data[0])
            scores.append(data[1])
            top_left.append("{},{}".format(data[2], data[3]))
            bottom_right.append("{},{}".format(data[4], data[5]))
        
        self.object_detection_client.send("ALL RECIEVED".encode(encoding="utf-8"))
        
        return list(zip(names, scores, top_left, bottom_right))
    
    def close_server(self):
        self.server.close()
        pass
    
    
class Human_Object_Interaction():
    
    def __init__(self, pose, _object):
        self.pose = pose
        self.object = _object
        self.relations = []
        self.hand_actions = [{"verb": "typing on a ", "joint": [5,8], "objects": ["keyboard", "laptop"]},
               {"verb": "reading a ", "joint": [5,8], "objects": ["book"]},
               {"verb": "holding a ", "joint": [5,8], "objects": ["cell phone","bird","dog","cat","umbrella","backpack","tie","bottle","cup","orange","apple","mouse","remote","scissors","teddy bear","hair drier","toothbrush", "spoon", "fork"]}]
        self.face_actions = [{"verb": "talking on a", "joint": [1], "face": [1], "objects": ["cell phone"]},
               {"verb": "eating a ", "joint": [13], "objects": ["apple", "banana","sandwich","carrot", "orange"]},
               {"verb": "drinking from a ", "joint": [13], "objects": ["cup", "bottle"]}]
        self.misc_actions = [{"verb": "wearing a ", "joint": [3,6], "objects": ["backpack, tie"]}]
    
    #Done - untested
    def check_for_person(self, keypoints, min_joints=2):
        #Require at least x joints to be considered valid
        for joint in keypoints:
            if int(round(joint[0])) != 0:
                min_joints -= 1
                if min_joints == 0:
                    return True
        return False
    
    def check_for_hand_interactions(self, object_data, joints):
        left_hand_area = self.extend_joint_area(self.pose.get_keypoint_by_name(joints, "lwrist"))
        right_hand_area = self.extend_joint_area(self.pose.get_keypoint_by_name(joints, "rwrist"))
        
        left_hand_occupied = False
        right_hand_occupied = False
        
        for obj in object_data:
            obj_name = obj[0]
            for action in self.hand_actions:
                for applicable_object in action['objects']:
                    if obj_name == applicable_object:
                        if not left_hand_occupied:
                            if self.intersects(list(zip(obj[2], obj[3], obj[4], obj[5])), left_hand_area):
                                object_data.remove(obj)
                                left_hand_occupied = True
                                self.relations.append("You are " + action['verb'] + " " + obj_name + " in your left hand")
                                print("LEFT HAND INTERSECTS WITH " + obj_name)
                        if not right_hand_occupied:
                            if self.intersects(list(zip(obj[2], obj[3], obj[4], obj[5])), right_hand_area):
                                right_hand_occupied = True
                                self.relations.append("You are " + action['verb'] + " " + obj_name + " in your right hand")
                                print("LEFT HAND INTERSECTS WITH " + obj_name)
                        
                        if left_hand_occupied and right_hand_occupied:
                            print("BOTH HANDS BUSY, GIVING UP SEARCH")
                            return object_data
        return object_data
    
    def check_for_face_interactions(self, object_data, joints):
        face_area = self.extend_joint_area(self.pose.get_keypoint_by_name(joints, "nose"))
        
        for obj in object_data:
            obj_name = obj[0]
            for action in self.face_actions:
                for applicable_object in action['objects']:
                    if obj_name == applicable_object:
                        if self.intersects(list(zip(obj[2], obj[3], obj[4], obj[5])), face_area):
                            object_data.remove(obj)
                            self.relations.append("You are " + action['verb'] + " " + obj_name)
                            print("FACE INTERSECTS WITH " + obj_name)
        return object_data
    
    def check_for_misc_interactions(self, object_data, joints):
        #How Do?
        for action in self.misc_actions:
            for joint in action['joint']:
                current_joint_area = self.extend_joint_area(joints[joint])
                for obj in object_data:
                    obj_name = obj[0]
                    for applicable_object in action['objects']:
                        if obj_name == applicable_object:
                            if self.intersects(list(zip(obj[2], obj[3], obj[4], obj[5])), current_joint_area):
                                object_data.remove(obj)
                                self.relations.append("You are " + action['verb'] + " " + obj_name)
                                print(str(joint) + " INTERSECTS WITH " + obj_name)
        return object_data
    
    def intersects(self, obj_area, joint_area):
        #make new area to decide if it intersects
        #joint - left, top, right, bottom
        #object - left, right, top, bottom
        if joint_area[0] > obj_area[0] or joint_area[2] < obj_area[1]:
            x_intersect = True
        if joint_area[1] > obj_area[3] or joint_area[3] < obj_area[2]:
            y_intersect = True
        return x_intersect and y_intersect
    
    def extend_joint_area(self, joint, radius=65):
        x = int(round(joint[0]))
        y = int(round(joint[1]))
        
        left = x - radius
        top = y - radius
        right = x + radius
        bottom = y + radius
        #cropped_img = image[y-radius:y+radius, x-radius:x+radius]
        return list(zip(left, top, right, bottom))
    
    def calculate_HOI(self):
        self.relations = []
        
        joints = self.pose.get_pose()
        
        if not self.check_for_person(joints):
            print("No person found")
        
        object_data = self.object.predict() #Image should be saved elsewhere
        
        #Each check returns the object list any objects that were found removed from the next check (stops items being held and eaten at the same time)
        object_data = self.check_for_face_interactions(object_data, joints)
        object_data = self.check_for_hand_interactions(object_data, joints)
        object_data = self.check_for_misc_interactions(object_data, joints)
        
        print("Unused objects: " + object_data)
        
        return self.relations

class Pose_Mirroring():

    def __init__(self, pose, model_dir="D:/RobotMaster/Models", model_name="InceptionV3.hdf5"):
        self.pose = pose
        self.model = self.init_custom_pose_model(model_dir, model_name)
        self.part_pairs = [1,2,   1,5,   2,3,   3,4,   5,6,   6,7,   1,0,   0,15,   15,17]
        self.colours = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0], [0, 255, 0], \
          [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], \
          [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85]]
        pass
    
    #Done - untested
    def init_custom_pose_model(self, dir, name):
        try:
            #model = load_model(os.path.join(dir, name))
            return model
        except:
            raise Exception("Model not found")

    def get_pose(self, frame):
        keypoints = self.pose.get_pose(frame)
        num_people = len(keypoints)
        if num_people == 0:
            print("No people found")
            return None
        
        #Only run on the first skeleton found, not multiple people
        frame = self.draw_person(frame, keypoints[0])
        label = self.predict(frame)
        label = self.label_to_name("D:/RobotMaster/res/legend.txt", label)
        
        return label
    
    def label_to_name(self, legend, label_val):
        # TODO: create legend file as a .csv
        with open(legend, 'r') as f:
            lines = f.readlines()
            return lines[int(label_val.split(",")[1])]
    
    def predict(self, img, img_target_size=299):
        img = cv2.resize(img, (img_target_size, img_target_size))
        x = np.expand_dims(img, axis=0)
        #x = preprocess_input(x.astype(float))
        pred = self.model.predict(x)
        pred = pred.tolist()
        pred = pred[0]
        return pred.index(max(pred))
    
    def draw_person(self, img, person):
        partial_joints = [0, 1, 2, 3, 4, 5, 6, 7, 15, 16, 17, 18]
        upper_skeleton_img = np.zeros((img.shape[0], img.shape[1], 3), np.unit8)
        counter = 0
        
        for data in person:
            x, y, score = data
            if x > 0 and y > 0:
                if counter in partial_joints:
                    cv2.cricle(upper_skeleton_img, (round(x), round(y)), 7, (0, 0, 255), -1)
                    
            counter += 1
        
        upper_skeleton_img = self.visualise_person(upper_skeleton_img, person)
        cropped_img = self.crop_person(upper_skeleton_img, person, partial_joints)
        return cropped_img
    
    def crop_person(self, img, person, upper_indexs):
        minx = 99999
        miny = 99999
        maxx = 0
        maxy = 0
        counter = 0
        
        for joint in person:
            x, y, score = joint
            if counter in upper_indexs:
                if x > 0:
                    if round(x) > maxx:
                        maxx = x + 10
                    if round(x) < minx:
                        minx = x - 10
                    if round(y) > maxy:
                        maxy = y + 10
                    if round(y) < miny:
                        miny = y - 10
            counter += 1
        cropped = img[int(round(miny)):int(round(maxy)), int(round(minx)):int(round(maxx))]
        return cropped
    
    def visualise_person(self, img, person):
        pairs = self.part_pairs
        stickwidth = 4
        cur_img = img.copy()
        counter = 0;
        for i in range(0, len(pairs),2):   
            if person[pairs[i],0] > 0 and person[pairs[i+1],0] > 0:
                Y = [person[pairs[i],0], person[pairs[i+1],0]]
                X = [person[pairs[i],1], person[pairs[i+1],1]]
                mX = np.mean(X)
                mY = np.mean(Y)
                length = ((X[0] - X[1]) ** 2 + (Y[0] - Y[1]) ** 2) ** 0.5
                angle = math.degrees(math.atan2(X[0] - X[1], Y[0] - Y[1]))
                polygon = cv2.ellipse2Poly((int(mY),int(mX)), (int(length/2), stickwidth), int(angle), 0, 360, 1)
                cv2.fillConvexPoly(cur_img, polygon, self.colours[counter])
                counter = counter + 1
        
        img = cv2.addWeighted(img, 0.4, cur_img, 0.6, 0)
        return img
    
class Age_Gender():
    def __init__(self, _dir="D:/NAORobot/Ross_Project/"):
        self.bat_file_dir = _dir
        pass
    
    def start(self):
        Popen(os.path.join(self.bat_file_dir, "Open_gui.bat"))

class Play_Football():
    def __init__(self, body):
        self.body = body
        self.upper_blue = np.array([170,235,255])
        self.lower_blue = np.array([100,110, 0])
        pass
    
    def start_walk(self, x_dir=0.5, y_dir=0.0, theta=0.0, freq=0.5):
        print("STARTING WALK")
        self.body.posture.walk_start(x_dir, y_dir, theta, freq)
        pass
    
    def stop_walk(self):
        self.body.posture.walk_stop()
        pass
    
    def apply_mask(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        threshold = cv2.inRange(hsv, self.lower_blue, self.upper_blue)
        res = cv2.bitwise_and(img,img, mask=threshold)
        
        kernel = np.ones((15,15),np.float32)/225
        smoothed = cv2.filter2D(res,-1,kernel)
        
        _, secret = cv2.threshold(smoothed, 30, 255, cv2.THRESH_BINARY)
        
        xs = np.where(secret != 0)[1]
        ys = np.where(secret != 0)[0]
    
        xstd = np.std(xs)
        ystd = np.std(ys)
    
        x_init_avg = np.mean(xs)
        y_init_avg = np.mean(ys)
    
        xs = [x for x in xs if x <= x_init_avg+xstd or x >= x_init_avg-xstd]
        ys = [y for y in ys if y <= y_init_avg+ystd or y >= y_init_avg-ystd]
        xavg = np.mean(xs)
        yavg = np.mean(ys)
        
        return secret, xavg, yavg
    
    def reposition(self):
        
        pass
