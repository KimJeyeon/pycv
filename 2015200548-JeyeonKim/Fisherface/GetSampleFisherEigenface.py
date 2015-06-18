Created on Fri Jun 12 17:27:12 2015

@author: jykim15
"""

import numpy as np
from PIL import Image
from pylab import *
import GetFisherfaceFunction

img_height = 68
img_width = 90
img_sample_num = 15

img_sample = np.zeros((img_sample_num, img_height * img_width))
for sample_num in range(5):
    for h in range(img_height):
        for w in range(img_width):
            
            img_temp1 = Image.open('ImageDataset/subset1/{0:d}.bmp'.format(sample_num + 1))
            img_temp2 = Image.open('ImageDataset/subset2/{0:d}.bmp'.format(sample_num + 1))
            img_temp3 = Image.open('ImageDataset/subset3/{0:d}.bmp'.format(sample_num + 1))

            img_sample[sample_num, img_height * w + h] = array(img_temp1.convert('L'))[h, w] 
            img_sample[5 + sample_num, img_height * w + h] = array(img_temp2.convert('L'))[h, w]
            img_sample[10 + sample_num, img_height * w + h] = array(img_temp3.convert('L'))[h, w]
    

img_average_mat_total = np.zeros((img_height * img_width))    
img_average_mat_subset1 = np.zeros((img_height * img_width))
img_average_mat_subset2 = np.zeros((img_height * img_width))
img_average_mat_subset3 = np.zeros((img_height * img_width))


for index in range(img_sample_num):
    img_average_mat_total = img_average_mat_total + img_sample[index,:] / img_sample_num

for index in range(img_sample_num / 3):
    img_average_mat_subset1 = img_average_mat_subset1 + img_sample[index,:]
    img_average_mat_subset2 = img_average_mat_subset2 + img_sample[index + 5,:]
    img_average_mat_subset3 = img_average_mat_subset3 + img_sample[index + 10,:]

img_average_mat_subset1 = img_average_mat_subset1 / (img_sample_num / 3)
img_average_mat_subset2 = img_average_mat_subset2 / (img_sample_num / 3)
img_average_mat_subset3 = img_average_mat_subset3 / (img_sample_num / 3)

img_mean_subtract_mat_subset1 = np.zeros((img_sample_num / 3, img_height * img_width))
img_mean_subtract_mat_subset2 = np.zeros((img_sample_num / 3, img_height * img_width))
img_mean_subtract_mat_subset3 = np.zeros((img_sample_num / 3, img_height * img_width))

temp1_mat = np.zeros((img_height * img_width))
temp2_mat = np.zeros((img_height * img_width))

for index in range(img_sample_num / 3):
    for sample1_num in range(img_height * img_width):
        temp1_mat[sample1_num] = img_sample[index, sample1_num]

    temp2_mat = GetFisherfaceFunction.GetSubtractImage(temp1_mat, img_average_mat_subset1, img_height, img_width)
    for sample3_num in range(img_height * img_width):
        img_mean_subtract_mat_subset1[index, sample3_num] = temp2_mat[sample3_num]
        
        
for index in range(img_sample_num / 3):
    for sample1_num in range(img_height * img_width):
        temp1_mat[sample1_num] = img_sample[index + 5, sample1_num]

    temp2_mat = GetFisherfaceFunction.GetSubtractImage(temp1_mat, img_average_mat_subset2, img_height, img_width)
    for sample3_num in range(img_height * img_width):
        img_mean_subtract_mat_subset2[index, sample3_num] = temp2_mat[sample3_num]  
        
        
for index in range(img_sample_num / 3):
    for sample1_num in range(img_height * img_width):
        temp1_mat[sample1_num] = img_sample[index + 10, sample1_num]

    temp2_mat = GetFisherfaceFunction.GetSubtractImage(temp1_mat, img_average_mat_subset3, img_height, img_width)
    for sample3_num in range(img_height * img_width):
        img_mean_subtract_mat_subset3[index, sample3_num] = temp2_mat[sample3_num]         
                
        
img_total_mean_subtract_mat = np.zeros((3, img_height * img_width))  

img_total_mean_subtract_mat[0, :] = img_average_mat_subset1 -  img_average_mat_total 
img_total_mean_subtract_mat[1, :] = img_average_mat_subset2 -  img_average_mat_total 
img_total_mean_subtract_mat[2, :] = img_average_mat_subset3 -  img_average_mat_total 
            Ei

fisherface_weight = np.zeros((img_sample_num, img_sample_num))

fisherface_weight = GetFisherfaceFunction.GetWeight(img_sample, img_mean_subtract_mat_subset1, 
                                                    img_mean_subtract_mat_subset2, 
                                                    img_mean_subtract_mat_subset3, img_total_mean_subtract_mat, 
                                                    img_sample_num, img_height, img_width)



for sample_num in range(img_sample_num):
    temp_file = open('ImageDatasetWeight/{0:d}.txt'.format(sample_num + 1), 'w')
    for index in range(img_sample_num):
        temp_file.write(str(fisherface_weight[index, sample_num]))
        temp_file.write('\n')
    temp_file.close()

