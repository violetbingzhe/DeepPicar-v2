from __future__ import division
import socket
import time
import picamera
# from evdev import InputDevice, categorize, ecodes
# from threading import Thread, Lock
import serial
import cv2
import tensorflow as tf
model = __import__(params.model)
import local_common as cm



OPCODE_DRIVE = 137
OPCODE_DRIVE_STRAIGHT = 32767

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
        # camera.framerate = 24
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)


        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            img = frame.array

            crop = img[40:200, 50:270]

            # resize to 200*66
            rsz = cv2.resize(crop, (200, 66))
            rsz = rsz / 255.

            angle = model.y.eval(feed_dict={model.x: [img]})[0][0]

            print "angle is ", angle

            time.sleep(0.1)

finally:
    print("finished")


