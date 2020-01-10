# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 10:45:35 2019

@author: sindrev
"""


        
def DownloadDataToScratch(cruise, cruise_name,main_dir):
    import sys, shutil,os
    import numpy as np
    
    
    #Convert to string
    cruise = str(cruise)
    
    
    #Grab year
    year = cruise[0:4]
    
    
    
    if 'win' in sys.platform: 
        ces_server = '//ces.imr.no/cruise_data/'
    else: 
        ces_server = '//data/cruise_data/'
        
    
    
    #list all surveys in year
    ces = os.listdir(ces_server+year)
    
    
    #list the platform to download
    platform = [ name for name in os.listdir(ces_server+year) if os.path.isdir(os.path.join(ces_server+year, name)) and cruise in name]
                    
         
    if len(platform)>1:
        print('Several vessel has the same kode')
    else: 
        platform = platform[0]
        
        
    #list all files in folder    
    liste = []
    for root, subdirs, files in os.walk(ces_server+year+'/'+platform):
        if len(files)>0: 
            for file in files: 
                liste.append(os.path.join(root,file))
    print('All files in server have been mapped')            
    
    
    if not os.path.exists(main_dir+'/'+cruise_name):
        os.makedirs(main_dir+'/'+cruise_name)
    
    if not os.path.exists(main_dir+'/'+cruise_name+'/'+year):
        os.makedirs(main_dir+'/'+cruise_name+'/'+year)
        
    if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform):
        os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform)
        
#    if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC'):
#        os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC')
    
    
    if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/DATA'):
        os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/DATA')
    if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/INTERPRETATION'):
        os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/INTERPRETATION')
    if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/INTERPRETATION/LSSS'):
        os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/INTERPRETATION/LSSS')
    
    
    
    #Write a log file of where the original files is stoored
    with open(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/DATA/original_data_location.txt', "w") as f: 
        f.write('DataLocation,NewDataLocation'+'\n')
    
    
    
    #Grab all raw data
    raw_files = [i for i in liste if i.endswith(('.raw','.idx','.bot')) and 'SX90' not in i and 'CALIBRATION' not in i and 'SU90' not in i and 'KORONA' not in i and 'SH90' not in i and 'OBSERVATION_PLATFORMS' not in i and 'OTHER_DATA' not in i]
    raw_folders = list(np.unique([os.path.dirname(i) for i in raw_files ]))


    version_tag =-1
    for folder in raw_folders: 
        version_tag =version_tag+1
        with open(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/DATA/original_data_location.txt', "a") as f: 
            f.write(str(folder)+','+main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/DATA/RAWDATA_V'+str(version_tag)+'\n')
        raw_dir =  main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/DATA/RAWDATA_V'+str(version_tag)
#    
        
        #Make directory if it does not exist
        if not os.path.exists(raw_dir):
                os.makedirs(raw_dir)
                
                
        #Copy file
        for raw in raw_files:
            if os.path.dirname(raw) == folder: 
                if not os.path.isfile(os.path.join(raw_dir,os.path.basename(raw))): 
                    print('copying: '+ os.path.basename(raw))
                    shutil.copyfile(raw, os.path.join(raw_dir,os.path.basename(raw)))
        
       
    
    