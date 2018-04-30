import numpy as np
import cv2
from naoqi import ALProxy
import vision_definitions as vd
import thread
import time
import Image
import sys
import os

ip_addr = "169.254.65.171"
port_num = 9559

# get NAOqi module proxy
videoDevice = ALProxy('ALVideoDevice', ip_addr, port_num)

#http://doc.aldebaran.com/1-14/dev/python/examples/vision/get_image.html
AL_kTopCamera = 0
resolution = 2
colour = 11
captureDevice = videoDevice.subscribeCamera(
    "test", AL_kTopCamera, resolution, colour, 24)

def thread_me(counter2, img2):
    zeroes = '00000000'
    #get last openpose file saved
    for root, dirs, files in os.walk("D:/Erik_Thomas/Robot/openpose_outputs/"):
        pass
    try:
        last_image_read = files[len(files)-1]
        last_image_read = int(last_image_read.split("_")[0]) + 5
    except:
        last_image_read = 1
    counter_len = len(str(last_image_read))
    zeroes_new = zeroes[:(len(zeroes)-counter_len)] + str(last_image_read)
    
    img2.save("D:/Erik_Thomas/Robot/openpose_blank/" + zeroes_new + ".jpg", "JPEG")

def show_me(res, count):
    if res == None:
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~cannot capture.'
    elif res[6] == None:
        print '###################################################no image data string.'
    else:
        imageWidth = res[0]
        imageHeight = res[1]
        imageArray = res[6]

        im = Image.fromstring("RGB", (imageWidth, imageHeight), imageArray)
    thread.start_new_thread(thread_me, (count, im))
    pass

counter = 1
frame_counter= 0
t0 = time.time()
try:
    while True:
        # get image
        result = videoDevice.getImageRemote(captureDevice)
        thread.start_new_thread(show_me, (result, counter))

        
        counter = counter+ 1
        frame_counter = frame_counter + 1
        t1 = time.time()
        if t1 - t0 >= 1:
            t0 = time.time()
            print ("Taken " + str(frame_counter) + "frames per second")
            frame_counter = 0
        time.sleep(0.28)
except KeyboardInterrupt:
    videoDevice.unsubscribe(captureDevice)
    sys.exit()
