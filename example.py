# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 10:31:48 2019

@author: sindrev
"""


import NMDdata
import API

NMDdata.getNMDinfo()

help(NMDdata.DownloadDataToScratch)
help(NMDdata.getNMDinfo)
help(API.runReportFromRaw)
help(API.startLSSS)

#
#
#path2LSSS = 'cmd.exe /c "C:/Program Files/Marec/lsss-2.8.0-alpha/lsss/LSSS.bat"&'
#
#
#
#import sys
#
#if 'win' in sys.platform: 
#    main_dir = '//ces.imr.no/mea/2018_Redus/SurveyData'
#else: 
#    main_dir = '//data/mea/2018_Redus/SurveyData'
#    
#    
#    
#    
#    
#
##Grab cruise number per time series
#df = NMDdata.getNMDinfo()
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
#
#
#API.startLSSS(path2LSSS)
#
#
#API.runLSSSReportMaker(main_dir,
#                           timeSeries = 'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
#                           year='2019',
#                           survey = 'S2019842_PVENDLA_3206',
#                           vertical_resolution = 10,
#                           horizontal_resolution = 0.1, 
#                           frequency=38,
#                           saveReportToCruice = True,
#                           reportType = [20,25],
#                           URLprefix = 'http://localhost:8000')