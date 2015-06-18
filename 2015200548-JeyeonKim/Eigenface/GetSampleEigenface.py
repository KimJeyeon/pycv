# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 17:27:12 2015

@author: jykim15
"""

import numpy as np
from PIL import Image
from pylab import *
import GetEigenfaceFunction

img_height = 68
img_width = 90
img_sample_num = 15

img_sample = np.zeros((img_sample_num, img_height * img_width))
for sample_num in range(5):
    for h in range(img_height):
        for w in range(img_width):
            temp1 = Image.open('ImageDataset/subset1/{0:d}.bmp'.format(sample_num + 1))
            temp2 = Image.open('ImageDataset/subset2/{0:d}.bmp'.format(sample_num + 1))
            temp3 = Image.open('ImageDataset/subset3/{0:d}.bmp'.format(sample_num + 1))
           
            img_sample[sample_num, img_height * w + h] = array(temp1.convert('L'))[h, w] 
            img_sample[5 + sample_num, img_height * w + h] = array(temp2.convert('L'))[h, w]
            img_sample[10 + sample_num, img_height * w + h] = array(temp3.convert('L'))[h, w]
    
    
img_average_mat = np.zeros((img_height * img_width))

for index in range(img_sample_num):
    img_average_mat[:] = img_average_mat[:] + img_sample[index,:] 
    
img_average_mat[:] = img_average_mat[:] / img_sample_num    

temp_img = np.zeros((img_height, img_width))
for h in range(img_height):
    for w in range(img_width):
        temp_img[h, w] = img_average_mat[img_height * w + h]
        
  

img_mean_subtract_mat = np.zeros((img_sample_num, img_height * img_width))
temp1_mat = np.zeros((img_height * img_width))
temp2_mat = np.zeros((img_height * img_width))

for index in range(img_sample_num):
    for sample1_num in range(img_height * img_width):
        temp1_mat[sample1_num] = img_sample[index, sample1_num]

    temp2_mat = GetEigenfaceFunction.GetSubtractImage(temp1_mat, img_average_mat, img_height, img_width)
    for sample3_num in range(img_height * img_width):
        img_mean_subtract_mat[index, sample3_num] = temp2_mat[sample3_num]
                
        
eigenface_weight = np.zeros((img_sample_num, img_sample_num))

eigenface_weight = GetEigenfaceFunction.GetWeight(img_mean_subtract_mat, img_sample_num, img_height, img_width)



for sample_num in range(img_sample_num):
    temp_file = open('ImageDatasetWeight/{0:d}.txt'.format(sample_num + 1), 'w')
    for index in range(img_sample_num):
        temp_file.write(str(eigenface_weight[index, sample_num]))
        temp_file.write('\n')
    temp_file.close()

temp_meanface_file = open('meanface.txt', 'w')
for index in range(img_height * img_width):
    temp_meanface_file.write(str(img_average_mat[index]))
    temp_meanface_file.write('\n')
temp_meanface_file.close()
