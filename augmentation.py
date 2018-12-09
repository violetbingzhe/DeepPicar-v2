import numpy as np
import cv2

import csv


# # change clockwise data 
input_raw = []

with open('/home/chenjiyang/irobot_lab_example/data/validation_data/output.txt') as file:
	csv_reader = csv.reader(file, delimiter=',')
	for row in csv_reader:
		input_raw.append(row)


input_raw.pop(0)

output_txt = []

for row in input_raw:
    img = cv2.imread('/home/chenjiyang/irobot_lab_example/data/validation_data/'+row[0])

    # move along height of photo
    # for i in range(-2,3,1):
    count = 0
    for i in range(1):
        i *= 2

        # move along width of photo
        for j in range(-1,2,1):
        # for j in range(1):
            j *= 2
            crop = img[40+i:200+i, 50+j:270+j]

            # resize to 200*66
            rsz = cv2.resize(crop, (200, 66))

            img_new_name = row[0][:-4] + '_' + str(count) + '.jpg'# len('.jpg') = -4
            
            cv2.imwrite('./data4/' + img_new_name, rsz)
            output_txt.append([img_new_name, row[1]])

            count += 1
            # flip image and add again
            flip =  np.flip(rsz,1)

            img_new_name = row[0][:-4] + '_' + str(count) + '.jpg'# len('.jpg') = -4

            cv2.imwrite('./data4/' + img_new_name, flip)
            output_txt.append([img_new_name, row[1]])
            count += 1


with open('./data4/output.txt', mode = 'wb') as file:
  csv_writer = csv.writer(file, delimiter=',')
  csv_writer.writerow(["img","wheel"])
  for row in output_txt:
      csv_writer.writerow(row)




# img_height = 66
# img_width = 200
# img_channels = 3

# def preprocess(img):
#     assert img_channels == 3 # for now we expect a color image
#     ratio = img_height / img_width
#     y1, y2 = 350, 553
#     w = (y2-y1) / ratio
#     padding = int(round((img.shape[1] - w) / 2))
#     # img = img[y1:y2, padding:-padding]
#     img = cv2.resize(img, (img_width, img_height))
#     img = img / 255.
#     return img





# Load an color image in grayscale
# img = cv2.imread('img.jpg')



# height, width = img.shape[:2]

# print height, width


# crop
# crop = img[40:210, 50:50+220]


# for i in range(-2,3,1):
#     i *= 5

#     # move along width of photo
#     for j in range(-2,3,1):
#         j *= 5
#         crop = img[40+i:200+i, 50+j:270+j]

#         # resize to 200*66
#         # rsz = cv2.resize(crop, (200, 66))
#         # imgs[p].append(rsz)
#         # wheels[p].append(yy)
#         cv2.imshow('image',crop)
#         k = cv2.waitKey(0)
#         # flip image and add again
#         flip =  np.flip(crop,1)
#         cv2.imshow('image',flip)
#         k = cv2.waitKey(0)

# cv2.imshow('image',crop)
# k = cv2.waitKey(0)


# flip image
# res = np.flip(img,1)
# val = -val

# cv2.imwrite('test.png',res)

# # flip image

# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('s'): # wait for 's' key to save and exit
#     cv2.imwrite('test.png',img)
#     cv2.destroyAllWindows()