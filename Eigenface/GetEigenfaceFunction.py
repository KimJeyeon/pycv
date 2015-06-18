# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 14:37:59 2015

@author: jykim15
"""

import numpy as np
from pylab import *

#import _imaging

def GetSubtractImage(img_mat, average_img_vector, img_height, img_width):
    

    img_subtract_mat = np.zeros((img_height * img_width))
    
    for index in range(img_height * img_width):
        img_subtract_mat[index] = img_mat[index] - average_img_vector[index]
    
        
    
    return img_subtract_mat
    


def GetWeight(img_subtract_mat, img_num, img_height, img_width):
    
    L_mat = np.zeros((img_num, img_num)) 
    L_mat = np.dot(img_subtract_mat, img_subtract_mat.T)
    
    eigenvalue, eigenvector = linalg.eigh(L_mat)
    
    covar_mat_eigenvector = np.zeros((img_height * img_width, img_num))
    covar_mat_eigenvector = np.dot(img_subtract_mat.T, eigenvector)
    
    sum_eigen = np.zeros(img_num)
    
    for sample_num in range(img_num):
        for index in range(img_height * img_width):
            sum_eigen[sample_num] = sum_eigen[sample_num] + pow(covar_mat_eigenvector[index, sample_num], 2)
    
        sum_eigen[sample_num] = sqrt(sum_eigen[sample_num])
        
        for index in range(img_height * img_width):
            covar_mat_eigenvector[index, sample_num] = covar_mat_eigenvector[index, sample_num] / sum_eigen[sample_num]
    
    
    for sample_num in range(img_num):
        temp_file = open('ImageDatasetEigenvector/{0:d}.txt'.format(sample_num + 1), 'w')
        for index in range(img_height * img_width):
            temp_file.write(str(covar_mat_eigenvector[index, sample_num]))
            temp_file.write('\n')
        temp_file.close()
        
    temp_file = open('temp1.txt', 'w')    
    for sample_num in range(img_num):
        for index in range(15):
            temp_file.write(str(img_subtract_mat[sample_num, index]))
            temp_file.write(' ')
        temp_file.write('\n')
    temp_file.close()    
    
    
    weight = np.zeros((img_num, img_num))
    
    
    weight = np.dot(covar_mat_eigenvector.T, img_subtract_mat.T)
    
    return weight
