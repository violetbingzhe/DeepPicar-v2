import numpy as np
import cv2

import csv


# # change clockwise data 
# input_raw = []

# with open('output_9_original.txt') as file:
# 	csv_reader = csv.reader(file, delimiter=',')
# 	for row in csv_reader:
# 		# print row
# 		row[1] = int(row[1]) - 1800
# 		# print row
# 		input_raw.append(row)



# with open('output.txt', mode = 'wb') as file:
# 	csv_writer = csv.writer(file, delimiter=',')
# 	for row in input_raw:
# 		csv_writer.writerow(row)

img_height = 66
img_width = 200
img_channels = 3

def preprocess(img):
    assert img_channels == 3 # for now we expect a color image
    ratio = img_height / img_width
    y1, y2 = 350, 553
    w = (y2-y1) / ratio
    padding = int(round((img.shape[1] - w) / 2))
    # img = img[y1:y2, padding:-padding]
    img = cv2.resize(img, (img_width, img_height))
    img = img / 255.
    return img





# Load an color image in grayscale
img = cv2.imread('img.jpg')



height, width = img.shape[:2]

print height, width


# crop
# crop = img[40:210, 50:50+220]


for i in range(-2,3,1):
    i *= 5

    # move along width of photo
    for j in range(-2,3,1):
        j *= 5
        crop = img[40+i:200+i, 50+j:270+j]

        # resize to 200*66
        # rsz = cv2.resize(crop, (200, 66))
        # imgs[p].append(rsz)
        # wheels[p].append(yy)
        cv2.imshow('image',crop)
        k = cv2.waitKey(0)
        # flip image and add again
        flip =  np.flip(crop,1)
        cv2.imshow('image',flip)
        k = cv2.waitKey(0)

# cv2.imshow('image',crop)
# k = cv2.waitKey(0)


# flip image
res = np.flip(img,1)
# val = -val

# cv2.imwrite('test.png',res)

# # flip image




# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('s'): # wait for 's' key to save and exit
#     cv2.imwrite('test.png',img)
#     cv2.destroyAllWindows()