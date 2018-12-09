import os
import local_common as cm
import params
from shutil import copyfile

data_dir = ""
csv_path = cm.jn(data_dir, 'data/output.txt')
rows = cm.fetch_csv_data(csv_path)

count = len(params.epochs['train']) + len(params.epochs['val'])
num = len(rows)/count
name = []
name.extend(params.epochs['train'])
name.extend(params.epochs['val'])
cur = num
index = 0

print len(rows), num

data_dir = 'epochs/data'+str(name[index])
if not os.path.isdir(data_dir):
	os.mkdir(data_dir)
f = open(data_dir + '/output.txt', 'w')
f.write("img,wheel\n")
for row in rows:
	cur = cur - 1
	if cur < 0:
		index = index + 1
		cur = num
		data_dir = 'epochs/data'+str(name[index])
		if not os.path.isdir(data_dir):
			os.mkdir(data_dir)
		f.close()
		f = open(data_dir +'/output.txt', 'w')
		f.write("img,wheel\n")

	# print row
	yy = float(row['wheel'])
	img_path = row['img']
	img_path_old = 'data/' + img_path
	if not os.path.isfile(img_path_old):
		continue
	copyfile(img_path_old, data_dir +"/"+img_path)
	f.write(img_path+","+str(yy)+"\n")
    
