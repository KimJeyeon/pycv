# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 14:37:59 2015

@author: jykim15
"""

import numpy as np
from pylab import *



def GetSubtractImage(img_mat, average_img_vector, img_height, img_width):
    

    img_subtract_mat = np.zeros((img_height * img_width))
    
    for index in range(img_height * img_width):
        img_subtract_mat[index] = img_mat[index] - average_img_vector[index]
    
        
    
    return img_subtract_mat
    
    

def GetWeight(img_mat, img_subtract_mat_subset1, img_subtract_mat_subset2, 
              img_subtract_mat_subset3,
              img_subtract_mat_total, img_num, img_height, img_width):
    
    Sw_mat = np.zeros((img_height * img_width, img_height * img_width)) 
    Sw_mat = np.dot(img_subtract_mat_subset1.T, img_subtract_mat_subset1) + np.dot(img_subtract_mat_subset2.T, img_subtract_mat_subset2) + np.dot(img_subtract_mat_subset3.T, img_subtract_mat_subset3)

    
    
    img_eigenvector_sample = np.zeros((img_num, img_height * img_width))
    
    for sample_num in range(img_num):
        
        img_eigen_weight_temp = open('ImageDatasetEigenfaceEigenvector/{0:d}.txt'.format(sample_num + 1))
        
        for index in range(img_height * img_width):
            img_temp_eigen = img_eigen_weight_temp.readline()
            img_eigenvector_sample[sample_num, index] = float(img_temp_eigen)
            
        img_eigen_weight_temp.close()    

    sigma_Sw_mat = np.zeros((img_num, img_num))
    sigma_Sw_mat = np.dot(np.dot(img_eigenvector_sample, Sw_mat), img_eigenvector_sample.T)
    
    temp1 = np.zeros((5, img_height * img_width))
    temp2 = np.zeros((5, img_height * img_width))
    temp3 = np.zeros((5, img_height * img_width))
    
    for index in range(5):
        temp1[index] = img_subtract_mat_subset1[index, :] - img_subtract_mat_total[0, :]
        temp2[index] = img_subtract_mat_subset2[index, :] - img_subtract_mat_total[1, :]
        temp3[index] = img_subtract_mat_subset3[index, :] - img_subtract_mat_total[2, :]
    
    Sb_mat = np.zeros((img_height * img_width, img_height * img_width)) 
    Sb_mat = (np.dot(temp1.T, temp1) + np.dot(temp2.T, temp2) + np.dot(temp3.T, temp3)) * 5
    
    sigma_Sb_mat = np.zeros((img_num, img_num))
    sigma_Sb_mat = np.dot(np.dot(img_eigenvector_sample, Sb_mat), img_eigenvector_sample.T)
    
   
    eigenvalue, eigenvector = linalg.eigh(np.dot(np.linalg.inv(sigma_Sw_mat), sigma_Sb_mat))
    
    eigenvector_mat = np.zeros((img_num, img_height * img_width))
    eigenvector_mat = np.dot(eigenvector.T, img_eigenvector_sample)
    
    
    
    img_mean_subtract = np.zeros((img_height * img_width, img_num))
    
    img_mean_file = open('meanface.txt')

    img_mean_mat = np.zeros((img_height * img_width))


    for index in range(img_height * img_width):
        img_temp = img_mean_file.readline()
        img_mean_mat[index] = float(img_temp)

    img_mean_file.close()
    
    for index in range(img_num):
        img_mean_subtract[:, index] = img_mat.T[:, index] - img_mean_mat
    
    
    covar_mat_eigenvector = np.zeros((img_height * img_width, img_num))
    
    covar_mat_eigenvector[:, :] = eigenvector_mat.T[:, :]
    
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
           
    total_subtract_mat = np.zeros((img_height * img_width, img_num))
    
    for index in range(15):
        total_subtract_mat[:, index] = img_mat.T[:, index] - img_mean_mat
    
    weight = np.zeros((img_num, img_num))
    
    
    weight = np.dot(covar_mat_eigenvector.T, total_subtract_mat)
    
    
    return weight
