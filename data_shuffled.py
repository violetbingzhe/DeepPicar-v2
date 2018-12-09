#!/usr/bin/env python
from __future__ import division

import random
import os
import sys
from collections import OrderedDict
import cv2
import params
# import preprocess
import local_common as cm
import numpy as np

################ parameters ###############
data_dir = params.data_dir
epochs = params.epochs
img_height = params.img_height
img_width = params.img_width
img_channels = params.img_channels

purposes = ['train', 'val']
imgs = OrderedDict()
wheels = OrderedDict()
for purpose in purposes:
    imgs[purpose] = []
    wheels[purpose] = []

categories = ['center', 'curve']    
imgs_cat = OrderedDict()
wheels_cat = OrderedDict()
for p in purposes:
    imgs_cat[p] = OrderedDict()
    wheels_cat[p] = OrderedDict()
    for c in categories:
        imgs_cat[p][c] = []
        wheels_cat[p][c] = []
    
# load all preprocessed training images into memory
def load_imgs():
    global imgs
    global wheels

    for p in purposes:
        print p
        for epoch_id in epochs[p]:
            print 'processing and loading "{}" epoch {} into memory, current num of imgs is {}...'.format(
                p, epoch_id, len(imgs[p]))


            # csv_path = cm.jn(data_dir, 'epoch{:0>2}_steering.csv'.format(epoch_id))
            csv_path = cm.jn(data_dir, 'data{}/output.txt'.format(epoch_id))
            assert os.path.isfile(csv_path)

            print "DBG:", csv_path
            rows = cm.fetch_csv_data(csv_path)

            # print len(rows)
            #print len(rows), frame_count
            #assert frame_count == len(rows)

            for row in rows:
                # print row
                yy = float(row['wheel'])
                img_path = row['img']

                ############ using opencv to read img here
                img_path = cm.jn(data_dir, 'data{}/{}'.format(epoch_id, img_path))
                if not os.path.isfile(img_path):
                    continue
                img = cv2.imread(img_path)

                ########### doing data augmentation

                # move along height of photo
                # for i in range(-2,3,1):
                # for i in range(-1,2,1):
                for i in range(1):
                    i *= 2

                    # move along width of photo
                    # for j in range(-1,2,1):
                    for j in range(1):
                        j *= 2
                        crop = img[40+i:200+i, 50+j:270+j]

                        # resize to 200*66
                        rsz = cv2.resize(crop, (200, 66))
                        imgs[p].append(rsz)
                        wheels[p].append(yy)

                        # flip image and add again
                        flip =  np.flip(rsz,1)
                        imgs[p].append(flip)
                        wheels[p].append(-yy)

                # img = preprocess.preprocess(img)
                # imgs[p].append(img)
                # wheels[p].append(yy)
            # print "wheels"
            # print wheels
            assert len(imgs[p]) == len(wheels[p])


def categorize_imgs():
    global imgs
    global wheels
    global imgs_cat
    global wheels_cat

    for p in purposes:
        n = len(imgs[p])

        for i in range(n):
            print 'wheels[{}][{}]:{}'.format(p, i, wheels[p][i])
            if abs(wheels[p][i]) < 0.001:
                imgs_cat[p]['center'].append(imgs[p][i])
                wheels_cat[p]['center'].append(wheels[p][i])
            else:
                imgs_cat[p]['curve'].append(imgs[p][i])
                wheels_cat[p]['curve'].append(wheels[p][i])

        print '---< {} >---'.format(p)
        for c in categories:
            print '# {} imgs: {}'.format(c, len(imgs_cat[p][c]))

    # print "finish categorize"

def load_batch(purpose):
    p = purpose
    assert len(imgs[p]) == len(wheels[p])
    n = len(imgs[p])
    assert n > 0

    ii = random.sample(xrange(0, n), params.batch_size)
    assert len(ii) == params.batch_size

    xx, yy = [], []
    for i in ii:
        xx.append(imgs[p][i])
        yy.append([wheels[p][i]])

    return xx, yy

# requires each category to be non-empty
def load_batch_category_normal(purpose):
    # print "enter load_batch"
    p = purpose
    xx, yy = [], []
    nc = len(categories)
    # print categories
    # print imgs_cat
    for c in categories:
        n = len(imgs_cat[p][c])
        # print n
        assert n > 0
        # print n, int(params.batch_size/nc)
        ii = random.sample(xrange(0, n), int(params.batch_size/nc))
        assert len(ii) == int(params.batch_size/nc)
        for i in ii:
            xx.append(imgs_cat[p][c][i])
            yy.append([wheels_cat[p][c][i]])
    # print "finish load_batch"
    return xx, yy

if __name__ == '__main__':
    load_imgs()

    load_batch('train')
    categorize_imgs()
    load_batch_category_normal('val')
