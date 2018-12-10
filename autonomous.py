from __future__ import division
import socket
import time
import picamera
from picamera.array import PiRGBArray
# from evdev import InputDevice, categorize, ecodes
# from threading import Thread, Lock
import serial
import cv2
import tensorflow as tf
import params
model = __import__(params.model)
import local_common as cm



OPCODE_DRIVE = 137
OPCODE_DRIVE_STRAIGHT = 32767

LEFT_Stick_X_MAX = 60000
LEFT_Stick_X_MIN = 8500 # 8600 seems to be safe as well
LEFT_Stick_X_MID = 34250
DEADZONE_RADIUS = 2000


def ints2str(lst):
    '''
    Taking a list of notes/lengths, convert it to a string
    '''
    s = ""
    for i in lst:
        if i < 0 or i > 255:
            raise Exception
        s = s + str(chr(i))
    return s

def drive (s, velocity, radius):
    l = []

    l.append(OPCODE_DRIVE)
    l.append((velocity & 0xFFFF) >> 8)
    l.append(velocity & 0x00FF)
    l.append((radius & 0xFFFF) >> 8)
    l.append(radius & 0x00FF)

    s.write(ints2str(l))


NCPU = 2

print ("Load Model")
config = tf.ConfigProto(intra_op_parallelism_threads=NCPU,
                        inter_op_parallelism_threads=NCPU, \
                        allow_soft_placement=True,
                        device_count = {'CPU': 1})

sess = tf.InteractiveSession(config=config)
saver = tf.train.Saver()
model_load_path = cm.jn(params.save_dir, params.model_load_file)
saver.restore(sess, model_load_path)
print ("Done..")


s = serial.Serial("/dev/ttyUSB0", 57600, timeout=4)
print("sending start...")
s.write(ints2str([128]))
print("switch to full mode...")
s.write(ints2str([132]))
speed = 60

# drive(s, speed, OPCODE_DRIVE_STRAIGHT)

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        # camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(320, 240))
        # camera.framerate = 24
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)



        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            print "time: ", time.time()
            img = frame.array

            crop = img[40:200, 50:270]

            # resize to 200*66
            rsz = cv2.resize(crop, (200, 66))
            rsz = rsz / 255.

            angle = model.y.eval(feed_dict={model.x: [rsz]})[0][0]

            print "angle is ", angle


            if angle >= 1:
                angle = 1
            elif angle <= -1:
                angle = -1

            x = angle * 22000 + 32800
            print "x is ", x


            if x > LEFT_Stick_X_MID + DEADZONE_RADIUS:
                    if x > LEFT_Stick_X_MAX:
                        x = LEFT_Stick_X_MAX

                    r = -2000 + int((x - DEADZONE_RADIUS - LEFT_Stick_X_MID) / (LEFT_Stick_X_MAX - DEADZONE_RADIUS - LEFT_Stick_X_MID) * (2000 - 100))
                    
#                    print "radius: " + str(r)
                    if r > -100:
                        r = -100

                    drive(s, speed, r)

                elif x < LEFT_Stick_X_MID - DEADZONE_RADIUS:
                    if x < LEFT_Stick_X_MIN:
                        x = LEFT_Stick_X_MIN

                    r = 100 + int((x - LEFT_Stick_X_MIN) / (LEFT_Stick_X_MID - DEADZONE_RADIUS - LEFT_Stick_X_MIN) * (2000 - 100))

#                    print "radius: " + str(r)
                    if r > 2000:
                        r = 2000

                    drive(s, speed, r)
                else:
                    
                    drive(s, speed, OPCODE_DRIVE_STRAIGHT)

            print "radius is ", r
            rawCapture.truncate(0)
            
            time.sleep(0.1)

finally:
    print("finished")


