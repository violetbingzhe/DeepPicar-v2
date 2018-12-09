import numpy as np
import csv
import random
import os



# used to randomly split data into training and valiation, ratio 3:1

input_raw = []

with open('output.txt') as file:
    csv_reader = csv.reader(file, delimiter=',')
    for row in csv_reader:
        input_raw.append(row)

input_raw.pop(0)
n = len(input_raw)
validation_list = random.sample(xrange(n), n/4)

validation_list.sort(reverse=True)

valid_output = []
for i in validation_list:
    row = input_raw.pop(i)
    valid_output.append(row)
    os.rename(row[0],"./validation/"+row[0])


with open('./validation/output_valid.txt', mode = 'wb') as file:
    csv_writer = csv.writer(file, delimiter=',')
    csv_writer.writerow(["img","wheel"])
    for row in valid_output:
        csv_writer.writerow(row)


with open('output_train.txt', mode = 'wb') as file:
    csv_writer = csv.writer(file, delimiter=',')
    csv_writer.writerow(["img","wheel"])
    for row in input_raw:
        csv_writer.writerow(row)




