import sys
import cv2
import os

input_data = sys.argv[1]
output_data = sys.argv[2]

for img_file in os.listdir(input_data):
	if not os.path.isdir(img_file):
		img = cv2.imread(img_file)