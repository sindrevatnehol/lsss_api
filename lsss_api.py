# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 12:47:43 2019

@author: sindrev
"""

import requests, os, json,shutil,subprocess, time, win32api, win32con
from datetime import date
import keyboard

import numpy as np





#To simulate mouse click
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


def automaticInstrument(URLprefix,lsssFile,ek60File,workFile,luf25file,vertical_resolution=10,horizontal_resolution=1,frequency=38,reportType=25):


    
    
    r = requests.get(URLprefix + '/lsss/application/info')
    lsss_version = json.loads(r.content)['version']
    
    print("Disconnected database")
    r = requests.post(URLprefix + "/lsss/application/config/unit/DatabaseConf/connected", json={'value':False})
    print("Disconnected database: " + str(r.status_code))
    
    print("Create a new database")
    r = requests.post(URLprefix + '/lsss/application/config/unit/DatabaseConf/create') #, json={'empty':True})
    print("Create a new database: " + str(r.status_code))
    
    print("Connect to the new database")
    r = requests.post(URLprefix + "/lsss/application/config/unit/DatabaseConf/connected", json={'value':True})
    print("Connect to the new database: " + str(r.status_code))
    
    print("Opening survey")
    r = requests.post(URLprefix+'/lsss/survey/open', json={'value':lsssFile})
    print("Opening survey:  " + lsssFile + ": " + str(r.status_code))
    
    
    
    #For first log
    #Set to 5 nm resolution
    print('Load interpretation data')
    r = requests.post(URLprefix + '/lsss/survey/config/unit/DataConf/parameter/WorkDir', json={'value':workFile})
    print( "Work Dir status: " + str(r.status_code))
    
    print('Load echosounder data')
    r = requests.post(URLprefix + '/lsss/survey/config/unit/DataConf/parameter/DataDir', json={'value':ek60File})
    print( "Raw Dir status: " + str(r.status_code))
    
    
    r = requests.get(URLprefix + '/lsss/survey/config/unit/DataConf/files')
    firstIndex = 0
    lastIndex = len(r.json()) - 1
    lastFile = r.json()[-1]['file']
    r = requests.post(URLprefix + '/lsss/survey/config/unit/DataConf/files/selection', json={'firstIndex':0, 'lastIndex':lastIndex})
    print("Selecting all files: " + str(r.status_code))
    
    	 
    
    
    #Merge alle lagene
    r=requests.post(URLprefix + '/lsss/regions/selection',json={ "all" : True })
    r=requests.post(URLprefix + '/lsss/regions/merge-layers')
    
    
    #Fjerne stimer
    r=requests.get(URLprefix + '/lsss/regions/region')
    data = json.loads(r.text)
    for dat in data: 
        r=requests.delete(URLprefix+'/lsss/regions/region/'+str(dat['id']))
        
        
    click(80,50)
    
    
    
    
    
    for i in range(1000):
                
        
        
        #Set to detailed
        r=requests.post(URLprefix + '/lsss/data/mode',json={'value':'DETAIL'})
        
        
        #Select all layers
        r=requests.post(URLprefix + '/lsss/regions/selection',json= { "all" : True})
        r.status_code
        
        
        #interpretation
        requests.post(URLprefix + '/lsss/module/ColorBarModule/threshold/min',json={'value':-55})
        
        
        
        r = requests.get(URLprefix + '/lsss/data/wait')
        print("Finish waiting: " + str(r.content))
        

        r=requests.get(URLprefix+'/lsss/module/PelagicEchogramModule/overlay/AccumulatedSaOverlay/data')
        t=json.loads(r.text)
        
        sa = np.max(t['datasets'][0]['sa'])/5
        
        requests.post(URLprefix + '/lsss/module/ColorBarModule/threshold/min',json={'value':-82})
        
        
        click(1500,1000)
        time.sleep(0.5)
        click(1850,820)
        time.sleep(1)
        keyboard.write('\b')
        keyboard.write('\b')
        keyboard.write('\b')
        keyboard.press('delete')   
        keyboard.press('delete')   
        keyboard.press('delete')   
        
        #Type sa values
        if sa <400: 
            sa = 0
            keyboard.write('0') 
        else:
            keyboard.write(str(sa))      
        keyboard.press('enter')  
            
        
        
#        
#        r = requests.post(URLprefix + '/lsss/survey/config/unit/GridConf/parameter/VerticalGridSizePelagic', 
#                          json={'value':vertical_resolution})
#        print( "Set vertical resolution (pelagic):" + str(r.status_code))
#        
#        r = requests.post(URLprefix + '/lsss/survey/config/unit/GridConf/parameter/VerticalGridSizeBottom', 
#                          json={'value':vertical_resolution})
#        print( "Set vertical resolution (bottom): " + str(r.status_code))
#                   
#        
#        r = requests.get(URLprefix + '/lsss/data/wait')
#        print("Finish waiting: " + str(r.content))
        
        # Store to local LSSS DB
#        print('Storing to database (This takes time)')
#        r = requests.post(URLprefix + '/lsss/module/InterpretationModule/database', json={'resolution':horizontal_resolution,
#                                                                                          'quality':1,
#                                                                                          'frequencies':[frequency, frequency]
                           
        #For å å hente bunnlinjen                                                               })
        
#        
#        r=requests.post(URLprefix + '/lsss/regions/region/651/mask',json={'time': '2019-02-13T16:17:49.145Z',
#                                                                          'pingNumber': 18531,
#                                                                          'vesselDistance': 10657.65376301745,
#                                                                          "depthRanges": [ { "min": 10, "max": 40 }, { "min": 10, "max": 40 } ] })
#        r.status_code
        
        
        r = requests.post(URLprefix + '/lsss/module/InterpretationModule/database', json={'resolution':horizontal_resolution,
                                                                                          'quality':1,
                                                                                          'frequencies':[frequency, frequency]
                                                                                          })
    
    
        r=requests.get(URLprefix + '/lsss/module')
        r.status_code
        r.json()
        
#        requests.post(URLprefix+'/lsss/application/save')
                      
                      
        
#        r = requests.get(URLprefix + '/lsss/survey/config/unit/DataConfId/files/selection')
    
        #Next 5 nmi
        click(40,50)
        
        
#    r=requests.get(URLprefix+'/lsss/module/InterpretationModule/config/parameter')
#    r.text

def runReportFromRaw(URLprefix,
                     lsssFile,
                     ek60File,
                     workFile,
                     luf25file,
                     vertical_resolution=10,
                     horizontal_resolution=1,
                     frequency=38,
                     reportType=25):
    
    r = requests.get(URLprefix + '/lsss/application/info')
    lsss_version = json.loads(r.content)['version']
    
    print("Disconnected database")
    r = requests.post(URLprefix + "/lsss/application/config/unit/DatabaseConf/connected", json={'value':False})
    print("Disconnected database: " + str(r.status_code))
    
    print("Create a new database")
    r = requests.post(URLprefix + '/lsss/application/config/unit/DatabaseConf/create') #, json={'empty':True})
    print("Create a new database: " + str(r.status_code))
    
    print("Connect to the new database")
    r = requests.post(URLprefix + "/lsss/application/config/unit/DatabaseConf/connected", json={'value':True})
    print("Connect to the new database: " + str(r.status_code))
    
    print("Opening survey")
    r = requests.post(URLprefix+'/lsss/survey/open', json={'value':lsssFile})
    print("Opening survey:  " + lsssFile + ": " + str(r.status_code))
    
    
    print('Load interpretation data')
    r = requests.post(URLprefix + '/lsss/survey/config/unit/DataConf/parameter/WorkDir', json={'value':workFile})
    print( "Work Dir status: " + str(r.status_code))
    
    print('Load echosounder data')
    r = requests.post(URLprefix + '/lsss/survey/config/unit/DataConf/parameter/DataDir', json={'value':ek60File})
    print( "Raw Dir status: " + str(r.status_code))
    
        
    #Hack to load all files
    #LSSS only load those files set in the .lsss file. T
    #Underneath will load the whole survey
    r = requests.get(URLprefix + '/lsss/survey/config/unit/DataConf/files')
    firstIndex = 0
    lastIndex = len(r.json()) - 1
    r = requests.post(URLprefix + '/lsss/survey/config/unit/DataConf/files/selection', json={'firstIndex':firstIndex, 'lastIndex':lastIndex})
    print("Selecting all files: " + str(r.status_code))
        
        
    # Wait until the program is ready for further processing
    r = requests.get(URLprefix + '/lsss/data/wait')
    print("Finish waiting: " + str(r.content))
        
    r = requests.post(URLprefix + '/lsss/survey/config/unit/GridConf/parameter/VerticalGridSizePelagic', 
                      json={'value':vertical_resolution})
    print( "Set vertical resolution (pelagic):" + str(r.status_code))
    
    r = requests.post(URLprefix + '/lsss/survey/config/unit/GridConf/parameter/VerticalGridSizeBottom', 
                      json={'value':vertical_resolution})
    print( "Set vertical resolution (bottom): " + str(r.status_code))
               
    
    r = requests.get(URLprefix + '/lsss/data/wait')
    print("Finish waiting: " + str(r.content))
    
    # Store to local LSSS DB
    print('Storing to database (This takes time)')
    r = requests.post(URLprefix + '/lsss/module/InterpretationModule/database', json={'resolution':horizontal_resolution,
                                                                                      'quality':1,
                                                                                      'frequencies':[frequency, frequency]
                                                                                      })
    
    print( "Set Interpretation Module parameters (and saving to DB): " + str(r.status_code))
    
    
    r = requests.get(URLprefix + '/lsss/data/wait')
    print("Finish waiting: " + str(r.content))
    
    if type(reportType)==int: 
        print('Making luf:'+ str(reportType))
        r = requests.get(URLprefix + '/lsss/database/report/'+str(reportType))
        print("Generating LUF"+str(reportType)+" from RAW: " + str(r.status_code))
        
         # Write it to disk
        if r.status_code == 200:
            print('Write report')
            with open(luf25file+'L_'+str(reportType)+'_LSSSV_'+lsss_version+'_T'+date.today().strftime("%Y%m%d")+'.xml', 'w+') as f:
                f.write(r.text)
    elif type(reportType)==list:
        for luftype in reportType: 
            print('Making luf:'+ str(luftype))
            r = requests.get(URLprefix + '/lsss/database/report/'+str(luftype))
            print("Generating LUF"+str(luftype)+" from RAW: " + str(r.status_code))
            
             # Write it to disk
            if r.status_code == 200:
                print('Write report')
                with open(luf25file+'L_'+str(luftype)+'_LSSSV_'+lsss_version+'.xml', 'w+') as f:
#                    +'_T'+date.today().strftime("%Y%m%d")+
                    f.write(r.text)


    r = requests.get(URLprefix + '/lsss/data/wait')
    print("Finish waiting: " + str(r.content))
    
    r = requests.post(URLprefix + '/lsss/survey/close')
    print("Closed survey: " + str(r.status_code))
    
    
    
    

#def getNMDEchosounderInfo(x):
#    '''
#    prosess to get list off all avaliable surveys
#    
#    '''
#    
#    print(x)




def runLSSSReportMaker(main_dir = '//ces.imr.no/mea/2018_Redus/SurveyData',
                       timeSeries = '',
                       year = '',
                       survey = '',
                       vertical_resolution = 10,
                       horizontal_resolution = 1, 
                       frequency=38,
                       saveReportToCruice = True,
                       reportType = 25,
                       URLprefix = 'http://localhost:8000',
                       path2LSSS=''):
    '''
    Process to make new report files
    
    '''
    
        
    
    lsssCommand = path2LSSS
    subprocess.Popen(lsssCommand,shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=None)
    
    time.sleep(10)
    
    
    click(1200,590)
    
    
    time.sleep(10)

    
    #Get the path to the survey on server
    cruise_dir = main_dir+'/'+timeSeries+'/'+str(year)+'/'+survey+'/'
    
    
    #Get all version of the lsss file
    LSSS_versions = [x for x in os.listdir(cruise_dir+'ACOUSTIC/LSSS/LSSS_FILES') if '.lsss' in x]
    if(len(LSSS_versions)>1): 
        print('Error: multiple raw files is avaliable. THis is not allowed at this current version')
    LSSS_versions = LSSS_versions[0]
    
    #Get all versions of interpretations
    WORK_versions = [x for x in os.listdir(cruise_dir+'ACOUSTIC/LSSS') if ('WORK'  in x or 'SNAP' in x) and not 'REPORT' in x]
    
    
    #Get all versios of echosounder data
    EKdatas = [x for x in os.listdir(cruise_dir+'ACOUSTIC/') if 'EK' in x]
#    KoronaDatas = [x for x in os.listdir(cruise_dir+'ACOUSTIC/LSSS') if 'KORONA' in x]
    
        
    
    for EKdata in EKdatas:
        
        for WORK_version in WORK_versions: 
            
            #Get path of the interpretation
            workFile = cruise_dir+'ACOUSTIC/LSSS/'+WORK_version
            
            if 'WORK' in WORK_version:
                print('Deleting snap from work')
                for snap_files_delete in os.listdir(workFile):
                    if '.snap' in snap_files_delete: 
                        print('    Deleting: ' + snap_files_delete)
                        os.remove(workFile+'/'+snap_files_delete)

            if 'SNAP' in WORK_version:
                print('Deleting work from snap')
                for snap_files_delete in os.listdir(workFile):
                    if '.work' in snap_files_delete: 
                        print('    Deleting: ' + snap_files_delete)
                        os.remove(workFile+'/'+snap_files_delete)

            if not os.path.exists(cruise_dir+'ACOUSTIC/LSSS/'+'REPORTS'):
                os.makedirs(cruise_dir+'ACOUSTIC/LSSS/'+'REPORTS')
            
            #Get path and make the folder for the reports
            reportFileRaw = cruise_dir+'ACOUSTIC/LSSS/REPORTS/'+'REPORTS_'+EKdata+'_'+WORK_version+'/'
            
            print('Do version: ' + EKdata+'_'+WORK_version)
            if not os.path.exists(reportFileRaw):
                os.makedirs(reportFileRaw)


            luf25file=reportFileRaw+'echosounder'+survey
        
            
            
            lsssFile = cruise_dir+'ACOUSTIC/LSSS/LSSS_FILES/'+LSSS_versions
            
            ek60File= cruise_dir+'ACOUSTIC/'+EKdata+'/'+EKdata+'_RAWDATA'
            
            
            
            
            #Prepare for an automatic rutine
            
            res = [i for i in WORK_versions if 'SNAP' in i] 
            if(len(res)>1): 
                print('Several SNAP, check code')
                asdf
                break
            
            src = cruise_dir+'ACOUSTIC/LSSS/'+res[0]
            src_files = os.listdir(cruise_dir+'ACOUSTIC/LSSS/'+res[0])
            for file_name in src_files:
                    full_file_name = os.path.join(src, file_name)
                    print(full_file_name)
                    if not os.path.exists(cruise_dir+'ACOUSTIC/LSSS/WORK_automatic/'):
                        os.makedirs(cruise_dir+'ACOUSTIC/LSSS/WORK_automatic/')
                    dst = os.path.join(cruise_dir+'ACOUSTIC/LSSS/WORK_automatic/', os.path.basename(file_name))
                    shutil.copyfile(full_file_name, dst)
                    
            automaticInstrument(URLprefix,
                     lsssFile,
                     ek60File,
                     workFile=cruise_dir+'ACOUSTIC/LSSS/WORK_automatic/',
                     luf25file=luf25file,
                     vertical_resolution=10,
                     horizontal_resolution=0.1,
                     frequency=38,
                     reportType=25)
            
            
            runReportFromRaw(URLprefix,
                             lsssFile,
                             ek60File,
                             workFile=workFile,
                             luf25file=luf25file,
                             vertical_resolution=vertical_resolution,
                             horizontal_resolution=horizontal_resolution,
                             frequency=frequency,
                             reportType=reportType)



'''
#Test if report files is identical: 
#Seperate between file types

#Test 1: Same files in same folder (timestamps)

#Test 2: Newest files between cases

filecmp.cmp('file1.txt', 'file2.txt')
'''
#
#filecmp.cmp('//ces.imr.no/mea/2018_Redus/SurveyData/Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar/2018/S2018831_PVENDLA_3670/ACOUSTIC/LSSS/REPORTS_EK60_SNAP_V1/echosounderS2018831_PVENDLA_3670L_25_LSSSV_2.7.0_T20191205.xml',
#            '//ces.imr.no/mea/2018_Redus/SurveyData/Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar/2018/S2018831_PVENDLA_3670/ACOUSTIC/LSSS/REPORTS_EK60_SNAP_V1/echosounderS2018831_PVENDLA_3670L_25_LSSSV_2.7.0_T20191205 - Copy.xml')


#    



    
main_dir = '//ces.imr.no/mea/2018_Redus/SurveyData'
timeSeries = 'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar'
year = '2019'
survey = 'S2019842_PVENDLA_3206'


runLSSSReportMaker(main_dir,
                       timeSeries,
                       year,
                       survey,
                       vertical_resolution = 10,
                       horizontal_resolution = 0.1, 
                       frequency=38,
                       saveReportToCruice = True,
                       reportType = [20,25],
                       URLprefix = 'http://localhost:8000',
                       path2LSSS = 'cmd.exe /c "C:/Program Files/Marec/LSSS 2.7.0/lsss/LSSS.bat"&')
