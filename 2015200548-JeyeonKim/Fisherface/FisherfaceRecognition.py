# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 16:39:01 2015

@author: JYKIM
"""

import numpy as np
from PIL import Image
from pylab import *



img_height = 68
img_width = 90
img_sample_num = 15

img_mat = np.zeros(img_height * img_width)

for h in range(img_height):
    for w in range(img_width):
        img_temp = Image.open('ImageTestset/subset2_2.bmp')
        img_mat[img_height * w + h] = array(img_temp.convert('L'))[h, w]


img_mean_file = open('meanface.txt')

img_mean_mat = np.zeros((img_height * img_width))


for index in range(img_height * img_width):
    img_temp = img_mean_file.readline()
    img_mean_mat[index] = float(img_temp)

img_mean_file.close()

img_subtract_mat = np.zeros((img_height * img_width))

for index in range(img_height * img_width):
    img_subtract_mat[index] = img_mat[index] - img_mean_mat[index]


img_eigenvector_sample = np.zeros((img_sample_num, img_height * img_width))
    
for sample_num in range(img_sample_num):
    
    img_eigen_temp = open('ImageDatasetEigenvector/{0:d}.txt'.format(sample_num + 1))
    
    for index in range(img_height * img_width):
        img_temp_eigen = img_eigen_temp.readline()
        img_eigenvector_sample[sample_num, index] = float(img_temp_eigen)
        
    img_eigen_temp.close()    


img_test_weight = np.zeros((img_sample_num))

img_test_weight = np.dot(img_eigenvector_sample, img_subtract_mat.T)  






img_weight_sample = np.zeros((img_sample_num, img_sample_num))
img_weight_distance = np.zeros((img_sample_num))

for sample_num in range(img_sample_num):
    
    img_weight_temp = open('ImageDatasetWeight/{0:d}.txt'.format(sample_num + 1))
    
    
        
    for index in range(img_sample_num):
        img_temp_weight = img_weight_temp.readline()
        img_weight_sample[sample_num, index] = float(img_temp_weight)
    
    img_weight_temp.close()
   
   
for sample_num in range(img_sample_num):     
    for index in range(img_sample_num):
        img_weight_distance[sample_num] = img_weight_distance[sample_num] + pow(img_weight_sample[sample_num, index] - img_test_weight[index], 2)
        
    img_weight_distance[sample_num] = sqrt(img_weight_distance[sample_num])
    
        
min_distance = 10000
classify = 0

for sample_num in range(img_sample_num):
    temp = min_distance
    min_distance = min(min_distance, img_weight_distance[sample_num])
    if temp != min_distance:
        classify = sample_num


classnum = int(classify / 5) + 1

if img_weight_distance[classify] <= 1800: 
    print 'Error : '
    print img_weight_distance[classify]
    print '\n'
    print 'Subset : '
    print classnum
else:
    print 'Error : '
    print img_weight_distance[classify]
    print '\n'
    print 'Subset : '
    print 'This image is a new image!'

print '\n'    
print 'Fisher Face'

img_eigenface = np.zeros((img_height, img_width))
img_temp_eigenface = np.zeros((img_height * img_width))

num = 0
for img_sample in range(img_sample_num):
    num = num + 1
    
    for h in range(img_height):
        for w in range(img_width):
            img_eigenface[h, w] = abs(img_eigenvector_sample[img_sample, img_height * w + h])
            
            
    subplot(3, 5, num)
    imshow(img_eigenface) 

    
    
