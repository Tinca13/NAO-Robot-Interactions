import almath
import time
from naoqi import ALProxy
from joint import Joint
from additional import Other

#Main class for controlling each joint of the robot
#This class contains most of the possible joint movements for the head and arms of the robot which can be adjusted using parameters
class Movement():
    def __init__(self, IP, port):
        self.IP = IP
        self.port = port
        self.tts = Other(self.IP, self.port)
        self.is_autonomous = True
        self.amproxy = ALProxy("ALAutonomousMoves", IP, port)
        #toggle the autonomous movement once to ensure the joints are put back to the resting position
        self.toggle_autonomous_movement(hard_reset=True)
        #toggle the autonomous movement again to allow the joints to be controlled by the classes methods
        self.toggle_autonomous_movement()
        pass

    #method to turn on or off the robots joint control
    #has hard reset option to ensure all joints are definetly in their resting position
    def toggle_autonomous_movement(self, hard_reset=False):
        if hard_reset:
            self.is_autonomous = False
            
        if self.is_autonomous:
            self.amproxy.setBackgroundStrategy("none")
            print("disabling autonomous movement")
            self.is_autonomous = False
        else:
            self.amproxy.setBackgroundStrategy("backToNeutral")
            self.is_autonomous = True
            print("re-enabling autonomous movement")

# --------------------------------Predefined movement code--------------------------------
    #Each of the following methods have the ability to contorl how fast the joints move (betwen 0.1 and 0.9 inclusive)    

    def right_arm_straight_up(self, speed=0.6):
        joint = Joint("RShoulder", self.IP, self.port)
        joint.pitch(-0.3,speed)

    def left_arm_straight_up(self, speed=0.6):
        joint = Joint("LShoulder", self.IP, self.port)
        joint.pitch(-0.3,speed)

    def right_arm_half_up(self, speed=0.6):
        joint = Joint("RShoulder", self.IP, self.port)
        joint.pitch(-0.5, speed)

    def left_arm_half_up(self, speed=0.6):
        joint = Joint("LShoulder", self.IP, self.port)
        joint.pitch(0.5, speed)

    def right_arm_out(self, speed=0.6):
        joint = Joint("RShoulder", self.IP, self.port)
        joint.roll(-1.2, speed)

    def left_arm_out(self, speed=0.6):
        joint = Joint("LShoulder", self.IP, self.port)
        joint.roll(1.2, speed)

    def right_elbow_straighten(self, speed=0.6):
        joint = Joint("RElbow", self.IP, self.port)
        joint.roll(-1.0, speed)

    def left_elbow_straighten(self, speed=0.6):
        joint = Joint("LElbow", self.IP, self.port)
        joint.roll(1.0, speed)

    def right_arm_out_bend_up(self):
        self.right_arm_straight_up()
        self.right_arm_out()
        time.sleep(1)
        self.right_elbow_roll(angle=1.5)

    def left_arm_out_bend_up(self):
        self.left_arm_straight_up()
        self.left_arm_out()
        time.sleep(1)
        self.left_elbow_roll(angle=-1.5)

    def right_wave_start(self, num):
        self.right_arm_out_bend_up()
        for i in range(num):
            self.right_elbow_straighten()
            time.sleep(0.5)
            self.right_elbow_roll(angle=1.5)
            time.sleep(0.5)

    def left_wave_start(self, num):
        self.left_arm_out_bend_up()
        for i in range(num):
            self.left_elbow_straighten()
            time.sleep(0.5)
            self.left_elbow_roll(angle=-1.5)
            time.sleep(0.5)

    def right_arm_down(self, speed=0.6):
        joint = Joint("RShoulder", self.IP, self.port)
        joint.pitch(1.6, speed)

    def left_arm_down(self, speed=0.6):
        joint = Joint("LShoulder", self.IP, self.port)
        joint.pitch(1.6, speed)

    def right_arm_straight_forward(self, speed=0.6):
        joint = Joint("RShoulder", self.IP, self.port)
        joint.roll(1.0, speed)
        joint.pitch(0.5, speed)

    def left_arm_straight_forward(self, speed=0.6):
        joint = Joint("LShoulder", self.IP, self.port)
        joint.roll(-1.0, speed)
        joint.pitch(0.5, speed)

#--------------------------------General movement code--------------------------------
    #The following methods are used to set more specific angles for each of the joints to give more control
    
    def right_shoulder_pitch(self, angle=0.0, speed=0.6):
        joint = Joint("RShoulder", self.IP, self.port)
        joint.pitch(angle, speed)

    def left_shoulder_pitch(self, angle=0.0, speed=0.6):
        joint = Joint("LShoulder", self.IP, self.port)
        joint.pitch(angle, speed)

    def right_shoulder_roll(self, angle=0.0, speed=0.6):
        joint = Joint("RShoulder", self.IP, self.port)
        joint.roll(angle, speed)

    def left_shoulder_roll(self, angle=0.0, speed=0.6):
        joint = Joint("LShoulder", self.IP, self.port)
        joint.roll(angle, speed)
        
    def right_elbow_roll(self, angle=0.0, speed=0.6):
        joint = Joint("RElbow", self.IP, self.port)
        joint.roll(angle,speed)

    def left_elbow_roll(self, angle=0.0, speed=0.6):
        joint = Joint("LElbow", self.IP, self.port)
        joint.roll(angle, speed)

    def right_elbow_yaw(self, angle=0.0, speed=0.6):
        joint = Joint("RElbow", self.IP, self.port)
        joint.yaw(angle, speed)

    def left_elbow_yaw(self, angle=0.0, speed=0.6):
        joint = Joint("LElbow", self.IP, self.port)
        joint.yaw(angle, speed)

    def right_wrist_yaw(self, angle=0.0, speed=0.6):
        joint = Joint("RWrist", self.IP, self.port)
        joint.yaw(angle, speed)

    def left_wrist_yaw(self, angle=0.0, speed=0.6):
        joint = Joint("LWrist", self.IP, self.port)
        joint.yaw(angle, speed)
        
#-------------------------------------Walking code-------------------------------------
    def stiffness_on(self, proxy):
        p_names = "Body"
        p_stiffness_lists = 1.0
        p_time_lists = 1.0
        proxy.stiffnessInterpolation(p_names, p_stiffness_lists, p_time_lists)
        
    def walk(self, x, y=0.0, theta=0.0, freq=0.0, _sleep=1.0):
        """Manages the walking of the robot, giving direction, speed and length of walking"""
        #positive x = forwards, negative x = backwards
        #frequency determines speed
        if _sleep > 20:
            #stops the robot from moving for too long
            self.tts.speak("I cannot walk for that long! Lowering time value")
            _sleep=20
        
        motion_proxy = ALProxy("ALMotion", self.IP, self.port)
        posture_proxy = ALProxy("ALRobotPosture", self.IP, self.port)
        self.stiffness_on(motion_proxy)
        #Initialises the posture so the robot is not crouching
        posture_proxy.goToPosture("StandInit", 0.5)
        #Initialises the relevant settings for safe walking
        motion_proxy.setWalkArmsEnabled(True, True)
        motion_proxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
        #Runs the walk command using the given parameters
        motion_proxy.setWalkTargetVelocity(x, y, theta, freq)
        #Sleep value determines how long the robot walks for
        time.sleep(_sleep)
        #These given parameters stop the robot since it has no x-direction to move in
        motion_proxy.setWalkTargetVelocity(0, 0, 0, 1)

#-------------------------------------Head movement-------------------------------------
    def head_swivel(self, angle=1.0, speed=0.6):
        motion_proxy = ALProxy("ALMotion", self.IP, self.port)
        joint = Joint("Head", self.IP, self.port)
        self.toggle_autonomous_movement()
        joint.yaw(angle, speed)
        self.toggle_autonomous_movement()

    def head_up_down(self, angle=1.0, speed=0.6):
        joint = Joint("Head", self.IP, self.port)
        #self.toggle_autonomous_movement()
        joint.pitch(angle, speed)
        #self.toggle_autonomous_movement()

#-------------------------------------Hand movement-------------------------------------
    #hand open and close will attempt to do so until resistance is met, as such, the robot cannot hold objects using these
    def hand_open(self, hand):
        motion_proxy = ALProxy("ALMotion", self.IP, self.port)
        if hand == 'LHand' or hand == 'RHand':
            motion_proxy.openHand(hand)
        else:
            self.tts.speak("Why didn't you give me a valid hand? Please try again")

    def hand_close(self, hand):
        motion_proxy = ALProxy("ALMotion", self.IP, self.port)
        if hand == 'LHand' or hand == 'RHand':
            motion_proxy.closeHand(hand)
        else:
            self.tts.speak("Why didn't you give me a valid hand? Please try again")

    #Fine control over the finger, the angles can be set so that objects can be gripped
    def right_hand_move(self, angle=0.0, speed=0.6):
        motion_proxy = ALProxy("ALMotion", self.IP, self.port)
        motion_proxy.setStiffnesses("RHand", 1.0)
        motion_proxy.setAngles("RHand", angle, speed)

    def left_hand_move(self, angle=0.0, speed=0.6):
        joint = Joint("LHand", self.IP, self.port)
        joint.motion_proxy.setAngles("LHand", angle, speed)

#-------------------------------------Detailed gestures-------------------------------------
    def left_hand_hip(self):
        self.left_shoulder_roll(50.0*almath.TO_RAD, speed=0.5)
        self.left_elbow_roll(-110*almath.TO_RAD, speed=0.5)
        self.left_elbow_yaw(10.5*almath.TO_RAD, speed=0.5)
        
    def right_hand_hip(self):
        self.right_shoulder_roll(-50.0*almath.TO_RAD, speed=0.5)
        self.right_elbow_roll(110*almath.TO_RAD, speed=0.5)
        self.right_elbow_yaw(-10.5*almath.TO_RAD, speed=0.5)

    #A list of possible pre-set movements made by SoftBank, usable by giving it the array index found in the method
    def posture(self, gesture, t=1.0):
        posture_proxy = ALProxy("ALRobotPosture", self.IP, self.port)
        gestures = ["StandInit", "SitRelax", "StandZero", "LyingBelly", "LyingBack", "Stand", "Crouch", "Sit"]
        if gesture in gestures:
           posture_proxy.goToPosture(gesture, t)
        else:
            self.tts.speak("Not a valid gesture, please try again!")
            print("The following are valid gestures:")
            for gst in gestures:
                print("* {}".format(gst))

#-------------------------------------Other-------------------------------------
    #Comedic method which looked like the robot was doing a little dance. DO NOT USE FOR OTHER PURPOSES
    def dancing_queen(self, joint_name):
        joint = Joint(joint_name, self.IP, self.port)
        try:
            joint.yaw(0, 0.5)
        except:
            print("Invalid yaw")
            pass
        try:
            joint.pitch(0, 0.5)
        except:
            print("Invalid pitch")
            pass
        try:
            joint.roll(0, 0.5)
        except:
            print("Invalid roll")
            pass

    #method to put the robots shoulder back to its resting state without affecting the whole robot toggling autonomous movement
    def reset_shoulder(self, side):
        joint = Joint(side, self.IP, self.port)
        joint.pitch(1.6, 0.5)
        joint.roll(0, 0.5)
        time.sleep(1)
        pass
    
    #method to put the robots elbow back to its resting state without affecting the whole robot toggling autonomous movement
    def reset_elbow(self, side):
        joint = Joint(side, self.IP, self.port)
        joint.yaw(0, 0.5)
        joint.roll(0, 0.5)
        time.sleep(1)
        pass
