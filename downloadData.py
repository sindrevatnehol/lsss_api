# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 13:46:37 2019

@author: sindrev
"""



import os
from distutils.dir_util import copy_tree



fleet = [2019207,2019847,2019204]

for f in fleet: 
    print(f)

year_folder = os.listdir('//data/cruise_data/'+str(f)[0:4])

survey = [s for s in year_folder if str(f) in s]

data_dir = '//data/cruise_data/'+str(f)[0:4]+'/'+survey[0]+'/ACOUSTIC'

fromDirectory = data_dir
toDirectory = '//data/mea/2018_Redus/SurveyData/Saildrone/'+str(f)[0:4]+'/'+survey[0]
if not os.path.exists(toDirectory):
    os.makedirs(toDirectory)
    os.makedirs(toDirectory+'/ACOUSTIC')

copy_tree(fromDirectory, toDirectory+'/ACOUSTIC')