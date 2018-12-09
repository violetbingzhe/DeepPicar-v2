import csv
import os

# used to rename data, both image and entry

for filename in os.listdir('.'):
    if filename[-3:] == "jpg":
        os.rename(filename, "3"+filename[1:])
        print filename

input_raw = []

with open('output.txt') as file:
  csv_reader = csv.reader(file, delimiter=',')
  for row in csv_reader:
      # print row
      row[0] = "3"+row[0][1:]
      # print row
      input_raw.append(row)



with open('output3.txt', mode = 'wb') as file:
  csv_writer = csv.writer(file, delimiter=',')
  csv_writer.writerow(["img,wheel"])
  for row in input_raw:
      csv_writer.writerow(row)