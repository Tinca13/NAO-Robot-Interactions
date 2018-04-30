#from naoqi import ALProxy
import os
import sys
import yaml
import cv2
import math
import numpy as np
from PIL import Image
from movement import Movement
from joint import Joint
import thread
import time

#method to start openpose
def openpose():
    #Change these directories if not running on the Windows 7 machine
    os.chdir('D:\\Zach_Wharton\\OpenPose_demo_1.0.1\\OpenPose_demo_1.0.1')
    os.system("bin\\OpenPoseDemo.exe --image_dir D:\\Erik_Thomas\\Robot\\openpose_blank --write_keypoint D:\\Erik_Thomas\\Robot\\openpose_outputs --no_display")
    pass

#Method to split the .yml file into x and y joint coordinates
def break_data(data):
    #split the data into 3s (x,y,score)
    chunks = [data[x:x+3] for x in range(0, len(data), 3)]
    #split the data into their x, y, and score values
    pose_x = []
    pose_y = []
    for point in chunks:
        x, y, score = str(point).split(",")
        x = x[1:]
        pose_x.append(int(round(float(x))))
        pose_y.append(int(round(float(y))))
    return pose_x, pose_y
    pass

#Method to open and read the .yml files
def get_joints():
    skip_lines = 2

    yml_dir = "D:/Erik_Thomas/Robot/openpose_outputs"
    
    #get all written .yml files
    for root, dirs, files in os.walk(yml_dir):
        #try to get the latest file written so the latest frame can be checked for a pose
        try:
            current_file = files[len(files)-1]
            print("looking at :" + current_file)
        #Stop checking if there is no .yml file to open
        except:
            return

    skele_path = yml_dir + '/' + current_file

    #Load the data attribute from the .yml file
    with open(skele_path) as infile:
        for i in range(skip_lines):
            _ = infile.readline()
        data = yaml.load(infile)

    pose_x, pose_y = break_data(data['data'])
    return (pose_x, pose_y)
    pass

#Debug method to draw where openpose finds the key joints
def draw_joint(a, b, c, p1, p2, p3):
    im_path = "D://openpose_images//hoh.jpg"
    image = cv2.imread(im_path)
    cv2.line(image, (a[0],a[1]), (b[0],b[1]), (255,255,0), 5)
    cv2.line(image, (b[0], b[1]), (c[0],c[1]), (255,255,0), 5)
    cv2.line(image, (a[0], a[1]), (c[0],c[1]), (255,255,0), 5)
    
    cv2.imshow("frame", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    pass

#manager method to call each of the state validators
def joint_check(rhip, rshoulder, relbow, rwrist, lhip, lshoulder, lelbow, lwrist, robot, right_arm_state, left_arm_state):
    print("checking joints")
    right_arm_states(np.array([rhip[0], rhip[1]]), np.array([rshoulder[0], rshoulder[1]]), np.array([relbow[0], relbow[1]]), np.array([rwrist[0], rwrist[1]]), robot, right_arm_state)
    left_arm_states(np.array([lhip[0], lhip[1]]), np.array([lshoulder[0], lshoulder[1]]), np.array([lelbow[0], lelbow[1]]), np.array([lwrist[0], lwrist[1]]), robot, left_arm_state)
    head_states() #NOT IMPLEMENTED DUE TO AWKWARDNESS OF RESETING THE ROBOT HEAD EACH TICK
    pass

#Method to look for each of the possible arm states
def right_arm_states(hip, shoulder, elbow, wrist, robot, right_arm_state):
    #Get angle of hip, shoulder and wrist from vectors
    v1 = np.array(hip) - np.array(shoulder)
    v2 = np.array(elbow) - np.array(shoulder)
    angle = np.math.atan2(np.linalg.det([v1,v2]), np.dot(v1,v2))
    angle = np.degrees(angle)
    #print("right arm angle: ", angle)
    
    #arm down
    if angle >= 0 and angle <= 30:
        if right_arm_state != 1:
            robot.reset_shoulder("RShoulder")
            robot.reset_elbow("RElbow")
            print("right arm down")
            robot.right_arm_down()
            right_arm_state = 1
    
    #arm straight up
    elif angle >= 150 and angle <= 180:
        if right_arm_state != 2:
            robot.reset_shoulder("RShoulder")
            robot.reset_elbow("RElbow")
            print("right arm up")
            robot.right_arm_straight_up()
            right_arm_state = 2
    
    #check if arm is out to the side
    elif angle >= 70 and angle <= 110:
        #Get angle of shoulder, elbow and wrist from vectors
        v1 = np.array(wrist) - np.array(elbow)
        v2 = np.array(shoulder) - np.array(elbow)
        angle = np.math.atan2(np.linalg.det([v1,v2]), np.dot(v1,v2))
        angle = np.degrees(angle)
        
        #arm side out
        if angle >= 150 and angle <= 180:
            if right_arm_state != 3:
                robot.reset_shoulder("RShoulder")
                robot.reset_elbow("RElbow")
                print("right arm out side")
                robot.right_arm_out()
                right_arm_state = 3
        #arm half bent up
        elif angle >= 70 and angle <= 110:
            if right_arm_state != 4:
                robot.reset_shoulder("RShoulder")
                robot.reset_elbow("RElbow")
                print("right arm half bent up")
                robot.right_arm_out_bend_up()
                right_arm_state = 4

    #check for other poses (hands on hips, arm infront)
    elif angle >= 30 and angle <= 60:
        #Get angle of hip, shoulder and wrist from vectors
        v1 = np.array(wrist) - np.array(elbow)
        v2 = np.array(shoulder) - np.array(elbow)
        angle = np.math.atan2(np.linalg.det([v1,v2]), np.dot(v1,v2))
        angle = np.degrees(angle)
        
        #check wrist is in general area of shoudler indicating that the arm is infront of the shoulder
        if wrist[0] >= shoulder[0] - 20 and wrist[0] <= shoulder[0] + 20 and wrist[1] >= shoulder[1] - 50 and wrist[1] <= shoulder[1] + 50:
            if right_arm_state != 5:
                robot.reset_shoulder("RShoulder")
                robot.reset_elbow("RElbow")
                print("right arm in front")
                robot.right_arm_half_up()
                right_arm_state = 5
        #Check if arm is on hip
        elif angle <= -70 and angle >= -110:
            if right_arm_state != 6:
                robot.reset_shoulder("RShoulder")
                robot.reset_elbow("RElbow")
                print("right arm on hip")
                robot.right_hand_hip()
                right_arm_state = 6
    pass

#Same as right_arm_states method above but for left arm values
def left_arm_states(hip, shoulder, elbow, wrist, robot, left_arm_state):
    #hip, shoulder and wrist angle
    v1 = np.array(hip) - np.array(shoulder)
    v2 = np.array(elbow) - np.array(shoulder)
    angle = np.math.atan2(np.linalg.det([v1,v2]), np.dot(v1,v2))
    angle = np.degrees(angle) * -1
    
    #arm down
    if angle >= 0 and angle <= 30:
        if left_arm_state != 1:
            robot.reset_shoulder("LShoulder")
            robot.reset_elbow("LElbow")
            print("left arm down")
            robot.left_arm_down()
            left_arm_state = 1
    
    #arm straight up
    elif angle >= 150 and angle <= 180:
        if left_arm_state != 2:
            robot.reset_shoulder("LShoulder")
            robot.reset_elbow("LElbow")
            print("left arm up")
            robot.left_arm_straight_up()
            left_arm_state = 2
    
    #check if arm is out to the side
    elif angle >= 70 and angle <= 110:
        v1 = np.array(wrist) - np.array(elbow)
        v2 = np.array(shoulder) - np.array(elbow)
        angle = np.math.atan2(np.linalg.det([v1,v2]), np.dot(v1,v2))
        angle = np.degrees(angle) * -1

        #arm side out
        if angle >= 150 and angle <= 180:
            if left_arm_state != 3:
                robot.reset_shoulder("LShoulder")
                robot.reset_elbow("LElbow")
                print("left arm out side")
                robot.left_arm_out()
                left_arm_state = 3
        #arm half bent up
        elif angle >= 70 and angle <= 110:
            if left_arm_state != 4:
                robot.reset_shoulder("LShoulder")
                robot.reset_elbow("LElbow")
                print("left arm half bent up")
                robot.left_arm_out_bend_up()
                left_arm_state = 4

    #check for other poses (hands on hips)
    elif angle >= 30 and angle <= 60:
        v1 = np.array(wrist) - np.array(elbow)
        v2 = np.array(shoulder) - np.array(elbow)
        angle = np.math.atan2(np.linalg.det([v1,v2]), np.dot(v1,v2))
        angle = np.degrees(angle)
        
        #check wrist is in general area of shoulder
        if wrist[0] >= shoulder[0] - 20 and wrist[0] <= shoulder[0] + 20 and wrist[1] >= shoulder[1] - 50 and wrist[1] <= shoulder[1] + 50:
            if left_arm_state != 5:
                robot.reset_shoulder("LShoulder")
                robot.reset_elbow("LElbow")
                print("left arm in front")
                robot.left_arm_half_up()
                left_arm_state = 5
        elif angle >= 70 and angle <= 110:
            if left_arm_state != 6:
                robot.reset_shoulder("LShoulder")
                robot.reset_elbow("LElbow")
                print("left arm on hip")
                robot.left_hand_hip()
                left_arm_state = 6
        pass
    pass

#NOT IMPLEMENTED DUE TO AWKWARDNESS OF RESETING THE ROBOT HEAD EACH TICK
def head_states():
    #remember to reset the robots head position after a delay to resume the camera
    pass

#Main method to call the above methods in the right order
def mirror_movement(robot, right_arm_state, left_arm_state):
    
    #Try except for when there is no person in the .yml file
    try:
        #read joint yml
        (all_x, all_y) = get_joints()
    
        #Save each joint to an array of the relevant name
        nose = [all_x[0], all_y[0]]
        neck = [all_x[1], all_y[1]]
        rshoulder = [all_x[2], all_y[2]]
        relbow = [all_x[3], all_y[3]]
        rwrist = [all_x[4], all_y[4]]
        lshoulder = [all_x[5], all_y[5]]
        lelbow = [all_x[6], all_y[6]]
        lwrist = [all_x[7], all_y[7]]
        rhip = [all_x[8], all_y[8]]
        rknee = [all_x[9], all_y[9]]
        rankle = [all_x[10], all_y[10]]
        lhip = [all_x[11], all_y[11]]
        lknee = [all_x[12], all_y[12]]
        lankle = [all_x[13], all_y[13]]
        reye = [all_x[14], all_y[14]]
        leye = [all_x[15], all_y[15]]
        rear = [all_x[16], all_y[16]]
        lear = [all_x[17], all_y[17]]

        '''#DEBUG FOR DRAWING JOINTS
        #use rhip, rshoulder, rwrist to compute arm angle
        x1 = relbow[0]
        y1 = relbow[1]
        lineA = [x1, y1]
        #print(x1, y1)

        x2 = rshoulder[0]
        y2 = rshoulder[1]
        lineB = [x2, y2]
        #print(x2, y2)

        x3 = rwrist[0]
        y3 = rwrist[1]
        lineC = [x3, y3]
        #print(x3, y3)

        draw_joint(lineA, lineB, lineC, np.array([x1,y1]), np.array([x2,y2]), np.array([x3,y3]))
        '''
        #Call the method to check each of the states
        joint_check(rhip, rshoulder, relbow, rwrist, lhip, lshoulder, lelbow, lwrist, robot, right_arm_state, left_arm_state)
    except:
        print("NO HUMAN IN YML")
        pass
    pass

#Method to fill a folder with 10x10 black images so that openpose has images to read
#(this had to be done to keep openpose open as it gets a list of all images to read on startup so adding new images will have no effect)
#(Also the robot camera cannot be used as a webcam for openpose either so this was not an option)
def folder_fill(_range):
    #Format the image names so they wil remain in the same order
    zeroes = '00000000'
    image = Image.new('RGB', (10, 10), color='black')
    for im in range(_range):
        # your directory here
        image_dir = "D:/Erik_Thomas/Robot/openpose_blank/"
        im_len = len(str(im))
        zeroes_new = zeroes[:(len(zeroes) - im_len)] + str(im)
        image.save(image_dir + zeroes_new + '.jpg')
    pass

#method to empty the outputs folder so that it can be run again without any issues
def clear_folder():
    yml_dir = "D:/Erik_Thomas/Robot/openpose_outputs/"
    for yml_file in os.listdir(yml_dir):
        file_path = os.path.join(yml_dir, yml_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)

        except Exception as e:
            print("The following exception was thrown in clear_folder {}".format(e))
    pass

#Instance the Joint and Movement classes in different scripts
joint = Joint("Head", "169.254.65.171", 9559)
move = Movement("169.254.65.171", 9559)
joint.release("Head")
move.head_up_down(angle=0.3)
time.sleep(2)
#Stiffen the head so the camera is stables
joint.stiffen("Head")


#set the starting joint states
right_arm_state = -1
left_arm_state = -1
right_leg_state = -1
left_leg_state = -1
head_state = -1

#Call the methods that will prepare the openpose directories
clear_folder()
folder_fill(1000)

#Try catch to prevent the robot being shutdown improperly
try:
    #Create a new thread so that openpose does not halt rest of the program
    thread.start_new_thread(openpose, ())
    #while true loop to keep checking for a new state to copy
    while True:
        mirror_movement(move, right_arm_state, left_arm_state)
except KeyboardInterrupt:
    #Release the head on crash so the robot can resume moving
    joint.release("Head")
    print("Program stopped by keyboard interupt")
finally:
    #Finally statement used to ensure the head is released regardless of if it crashed or not
    joint.release("Head")
