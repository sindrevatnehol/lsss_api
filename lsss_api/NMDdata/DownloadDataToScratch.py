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
    platform = [i for i in ces if cruise in i] 
    
    
                    
         
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
        
    if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC'):
        os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC')
    
    
    #Copy raw data
    raw_files = [i for i in liste if i.endswith(('.raw','.idx','.bot')) and 'SX90' not in i and 'CALIBRATION' not in i and 'SU90' not in i and 'KORONA' not in i and 'SH90' not in i]
    raw_folders = list(np.unique([os.path.dirname(i) for i in raw_files ]))
    print(raw_folders)
    #Force an error
    if len(raw_folders)==1: 
        if 'EK60' in raw_folders[0]: 
            if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK60'):
                os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK60')
            if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK60/EK60_RAWDATA'):
                os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK60/EK60_RAWDATA')
            raw_dir = main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK60/EK60_RAWDATA'
                
        elif 'EK80' in raw_folders[0]: 
            if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK80'):
                os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK80')
            if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK80/EK80_RAWDATA'):
                os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK80/EK80_RAWDATA')
            raw_dir = main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK80/EK80_RAWDATA'
        
        
        for raw in raw_files:
            if not os.path.isfile(os.path.join(raw_dir,os.path.basename(raw))): 
                print('copying: '+ os.path.basename(raw))
                shutil.copyfile(raw, os.path.join(raw_dir,os.path.basename(raw)))
            
    
     
    else: 
        for i in range(0,len(raw_folders)): 
            if 'EK60' in raw_folders[0]: 
                if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK60'):
                    os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK60')
                if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK60/EK60_RAWDATA_V'+str(i)):
                    os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK60/EK60_RAWDATA_V'+str(i))
                raw_dir = main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK60/EK60_RAWDATA'
                    
            elif 'EK80' in raw_folders[0]: 
                if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK80'):
                    os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK80')
                if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK80/EK80_RAWDATA_V'+str(i)):
                    os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK80/EK80_RAWDATA_V'+str(i))
                raw_dir = main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/EK80/EK80_RAWDATA'       

    
        for raw in raw_files:
            if not os.path.isfile(os.path.join(raw_dir + '_V'+str(raw_folders.index(os.path.dirname(raw))),os.path.basename(raw))): 
                print('copying: '+ os.path.basename(raw))
                shutil.copyfile(raw, os.path.join(raw_dir + '_V'+str(raw_folders.index(os.path.dirname(raw))),os.path.basename(raw)))
            
    
    
    #Work information
    work_files = [i for i in liste if i.endswith(('.work','.snap'))]
    work_folders = list(np.unique([os.path.dirname(i) for i in work_files ]))
    print(work_folders)
    if len(work_folders)>1: 
        print('Several work folders')
        asdf
    
    if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/LSSS'):
        os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/LSSS')
        
    if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/LSSS/WORK'):
            os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/LSSS/WORK')
        
    if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/LSSS/SNAP'):
            os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/LSSS/SNAP')
    
    
    for file in work_files: 
        
        if file.endswith('.work'): 
            if not os.path.isfile(os.path.join(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/LSSS/WORK',os.path.basename(file))): 
                print('Copying: '+ os.path.basename(file))
                shutil.copyfile(file, os.path.join(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/LSSS/WORK',os.path.basename(file)))
        if file.endswith('.snap'): 
            if not os.path.isfile(os.path.join(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/LSSS/SNAP',os.path.basename(file))): 
                print('copying: '+ os.path.basename(file))
                shutil.copyfile(file, os.path.join(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/LSSS/SNAP',os.path.basename(file)))
    
    
    #Copy lsss files
    lsss_files = [i for i in liste if i.endswith('.lsss')]
    
    
    
    if not os.path.exists(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/LSSS/LSSS_FILES'):
        os.makedirs(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/LSSS/LSSS_FILES')
    
    
    
    if len(lsss_files)>1: 
        base_name = np.unique([os.path.basename(i) for i in lsss_files])
        if len(base_name)<len([os.path.basename(i) for i in lsss_files]):
            print('multiple lsss files')
            asdf
        
        
        
    for lsss in lsss_files:
        shutil.copyfile(lsss, os.path.join(main_dir+'/'+cruise_name+'/'+year+'/'+platform+'/ACOUSTIC/LSSS/LSSS_FILES/',os.path.basename(lsss)))
    
    
    
    