# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 10:31:48 2019

@author: sindrev
"""


import NMDdata
import API
import numpy as np





path2LSSS = 'cmd.exe /c "C:/Program Files/Marec/lsss-2.8.0-alpha/lsss/LSSS.bat"&'



import sys

if 'win' in sys.platform: 
    main_dir = '//ces.imr.no/mea/2018_Redus/SurveyData'
    work_dir = '//ces.imr.no/mea/2018_Redus/WorkData'
else: 
    main_dir = '//data/mea/2018_Redus/SurveyData'
    work_dir = '//data/2018_Redus/WorkData'
    
    
    
    
    

#Grab cruise number per time series
df = NMDdata.getNMDinfo()
#
#
##Add saildrone
#import pandas as pd
#d = {'name':'Saildrone','cruiseid':list([2019204,2019207,2019847])}
#df = df.append(pd.DataFrame(d))
#
#
#
#cruise_id = df[df['name']=='Saildrone']['cruiseid']
#cruise_name = df[df['name']=='Saildrone']['name'][0]


cruise_id = df[df['name']==np.unique(df['name'])[17]]['cruiseid']
cruise_name = df[df['name']==np.unique(df['name'])[17]]['name'][0]
    


#
#


for cruise in cruise_id[12:len(cruise_id)]: 
    print(cruise)
    
    #Download cleane structure to a server
    NMDdata.DownloadWORKToScratchFromCES(cruise, cruise_name,work_dir)
    
    
    NMDdata.DownloadDataToScratch(cruise, cruise_name,main_dir)
    
    
    
NMDdata.DownloadInterpretation(main_dir,work_dir,cruise_name)
    
    
API.startLSSS(path2LSSS)


API.runLSSSReportMaker(main_dir,
                           timeSeries = 'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                           year='2015',
                           survey = 'S2015833_PNYBO_4135',
                           vertical_resolution = 10,
                           horizontal_resolution = 0.1, 
                           frequency=38,
                           saveReportToCruice = True,
                           reportType = [20,25],
                           URLprefix = 'http://localhost:8000')




import os
import API
time_series = os.listdir(main_dir)

for time_s in time_series: 
    for year in os.listdir(os.path.join(main_dir,time_s)):
        for platform in os.listdir(os.path.join(main_dir,time_s,year)): 
            data_dir =np.sort([name for name in os.listdir(os.path.join(main_dir,time_s,year,platform,'DATA')) if 'RAWDATA' in name])
            if len(data_dir)>1: 
                data_dir = os.path.join(main_dir,time_s,year,platform,'DATA',data_dir[-1])
            else: 
                data_dir = os.path.join(main_dir,time_s,year,platform,'DATA',data_dir[0])
                
            lsss_file = os.path.join(main_dir,time_s,year,platform,'INTERPRETATION','LSSS',
                                     ([name for name in os.listdir(os.path.join(main_dir,time_s,year,platform,'INTERPRETATION','LSSS')) 
                                     if '.lsss' in name])[0])
            
            work_dir = os.path.join(main_dir,time_s,year,platform,'INTERPRETATION','LSSS',
                                    [name for name in os.listdir(os.path.join(main_dir,time_s,year,platform,'INTERPRETATION','LSSS')) 
                                    if 'WORK' in name][-1])
            
            API.automaticInstrument(baseUrl = 'http://localhost:8000',
                     lsssFile=lsss_file,
                     ek60File=data_dir,
                     workFile=work_dir,
                     vertical_resolution=1,
                     horizontal_resolution=0.1,
                     frequency=38,
                     reportType=25,
                     TH_min = -55,
                     sa_min = 200,
                     acocat = [12,1])


    break



