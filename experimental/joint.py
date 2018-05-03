from naoqi import ALProxy
import time

#Class to control the joints directions. Used by the movement class
class Joint:
    
    def __init__(self, joint_name, IP, port):
        self.type = joint_name
        self.motion_proxy = ALProxy("ALMotion", IP, port)

    #Pitch, yaw and roll methods that set the angle of any joints as absolute positions
    def pitch(self, angle, speed=0.5, t=1):
        self.motion_proxy.post.setAngles(self.type + "Pitch", angle, speed)
        #time.sleep(t)
        pass
    
    def yaw(self, angle, speed=0.5, t=1):
        print("joint angle: ", angle)
        self.motion_proxy.post.setAngles(self.type + "Yaw", angle, speed)
        #time.sleep(t)
        print("done")
        pass
    
    def roll(self, angle, speed=0.5, t=1):
        self.motion_proxy.post.setAngles(self.type + "Roll", angle, speed)
        #time.sleep(t)
        pass
    
    #pitch, yaw and roll methods that set the angle relative to its current angle, then returns to the previous position
    def pitch_reset(self, angle, time, is_absolute=False):
        self.motion_proxy.post.angleInterpolation([self.type + "Pitch"], [angle], [time], is_absolute)
        pass
    
    def yaw_reset(self, angle, time, is_absolute=False):
        self.motion_proxy.post.angleInterpolation([self.type + "Yaw"], [angle], [time], is_absolute)
        pass
    
    def roll_reset(self, angle, time, is_absolute=False):
        self.motion_proxy.post.angleInterpolation([self.type + "Roll"], [angle], [time], is_absolute)
        pass

    #method to stiffen the given joint type (either body or head)
    def stiffen(self, joint_type, stiffness=0.0):
        self.motion_proxy.setStiffnesses(joint_type, stiffness)
        pass
    
    #method to release the given joint type
    def release(self, joint_type, stiffness=1.0):
        self.motion_proxy.setStiffnesses(joint_type, stiffness)
        pass
