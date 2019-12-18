# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 12:47:43 2019

@author: sindrev
"""

import requests, os, json,shutil, time, win32api, win32con
from datetime import date
import keyboard
import numpy as np





#To simulate mouse click
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)




def getNMDinfo():
    
    import urllib.request
    import xmltodict
    import pandas as pd
    server = "http://tomcat7.imr.no:8080/apis/nmdapi/reference/v2/dataset/cruiseseries?version=2.0"
    with urllib.request.urlopen(server) as f:
        data = xmltodict.parse(f.read())
        
    df = pd.DataFrame([])
    for i in range(0,len(data['list']['row'])):       
        name = data['list']['row'][i]['name']
        
        cruise_id = []
        for ii in range(0,len(data['list']['row'][i]['samples']['sample'])):
            
            for iii in range(0,len(data['list']['row'][i]['samples']['sample'][ii]['cruises']['cruise'])):
                try: 
                    cruise_id=np.hstack((cruise_id,data['list']['row'][i]['samples']['sample'][ii]['cruises']['cruise'][iii]['cruisenr']))
                except KeyError: 
                    cruise_id=np.hstack((cruise_id,data['list']['row'][i]['samples']['sample'][ii]['cruises']['cruise']['cruisenr']))
        cruise_id = (np.unique(cruise_id))
        
    
        d = {'name':name,'cruiseid':list(cruise_id)}
        df = df.append(pd.DataFrame(d))
        
    return(df)
    
    
    
    

def DownloadDataToScratch(cruise, cruise_name,main_dir):
    
    
    year = cruise[0:4]
    
    
    #list all surveys in year
    ces = os.listdir('//ces.imr.no/cruise_data/'+year)
    
    #list the platform to download
    platform = [i for i in ces if cruise in i] 
    
    
                    
         
    if len(platform)>1:
        print('Several vessel has the same kode')
    else: 
        platform = platform[0]
        
        
    #list all files in folder    
    liste = []
    for root, subdirs, files in os.walk('//ces.imr.no/cruise_data/'+year+'/'+platform):
        if len(files)>0: 
            for file in files: 
                liste.append(os.path.join(root,file))
                
    
    
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
    
    
    
    


def startLSSS(path2LSSS): 
    #An automated way to start the LSSS software
    
    import subprocess
    
    lsssCommand = path2LSSS
    subprocess.Popen(lsssCommand,shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=None)
    time.sleep(15)
    click(1200,590)
    time.sleep(10)







def automaticInstrument(URLprefix,
                        lsssFile,
                        ek60File,
                        workFile,
                        vertical_resolution=10,
                        horizontal_resolution=1,
                        frequency=38,
                        reportType=25,
                        TH_min = -55):

    
    
    #Function to simulate a instrement person

    
    #Read the lsss version. 
    #This will in future help to keep track of ther version
    r = requests.get(URLprefix + '/lsss/application/info')
    lsss_version = json.loads(r.content)['version']
    
    
    #Prepare the lsss database
    print("Disconnected database")
    r = requests.post(URLprefix + "/lsss/application/config/unit/DatabaseConf/connected", json={'value':False})
    print("Create a new database")
    r = requests.post(URLprefix + '/lsss/application/config/unit/DatabaseConf/create') #, json={'empty':True})
    print("Connect to the new database")
    r = requests.post(URLprefix + "/lsss/application/config/unit/DatabaseConf/connected", json={'value':True})


    #Open the lsss survey file
    print("Opening survey")
    r = requests.post(URLprefix+'/lsss/survey/open', json={'value':lsssFile})
    print("Opening survey:  " + lsssFile + ": " + str(r.status_code))
    
    
    #Sett the location of the data
    print('Load interpretation data')
    r = requests.post(URLprefix + '/lsss/survey/config/unit/DataConf/parameter/WorkDir', json={'value':workFile})
    print('Load echosounder data')
    r = requests.post(URLprefix + '/lsss/survey/config/unit/DataConf/parameter/DataDir', json={'value':ek60File})
    
    
    #Load all the files
    r = requests.get(URLprefix + '/lsss/survey/config/unit/DataConf/files')
    firstIndex = 0
    lastIndex = len(r.json()) - 1
    lastFile = r.json()[-1]['file']
    r = requests.post(URLprefix + '/lsss/survey/config/unit/DataConf/files/selection', json={'firstIndex':0, 'lastIndex':lastIndex})
    print("Selecting all files: " + str(r.status_code))
    
    	 
    
    
    #Merge all layers into one
    r=requests.post(URLprefix + '/lsss/regions/selection',json={ "all" : True })
    r=requests.post(URLprefix + '/lsss/regions/merge-layers')
    
    
    #Remove all schools
    r=requests.get(URLprefix + '/lsss/regions/region')
    data = json.loads(r.text)
    for dat in data: 
        r=requests.delete(URLprefix+'/lsss/regions/region/'+str(dat['id']))
        
        
        
    #Click to 5 nm resolution
    #This should be replaced with an api function
    click(80,50)
    
    
    
    
    #Loop through each 5 nm distance
    #This should be replaced so we recognise if we are at the end of the last file
    for i in range(1000):
                
        
        #Grab all the frequencies
        r=requests.get(URLprefix + '/lsss/data/frequencies')
        frequencies = r.json()
        
        #To be included in future, loop through each frequency
        for freq in frequencies: 
            freq
        
        
        #Sett frequency
        freq = 38000.0
        r=requests.post(URLprefix + '/lsss/data/frequency',json={'value':freq})
        
        #Set to detailed window
        r=requests.post(URLprefix + '/lsss/data/mode',json={'value':'DETAIL'})
        
        
        #Select all layers in window
        r=requests.post(URLprefix + '/lsss/regions/selection',json= { "all" : True})
        r.status_code
        
        
        #Sett the lower threshold
        requests.post(URLprefix + '/lsss/module/ColorBarModule/threshold/min',json={'value':TH_min})
        
        
        #Wait for all the data to be loaded
        r = requests.get(URLprefix + '/lsss/data/wait')
        

        #Grab
        r=requests.get(URLprefix+'/lsss/module/PelagicEchogramModule/overlay/AccumulatedSaOverlay/data')
        t=json.loads(r.text)
        
        r=requests.get(URLprefix+'/lsss/module/PelagicEchogramModule/overlay/AccumulatedSaOverlay/data')
        
        #Need to check this        
        log_distance = 5
        sa = np.max(t['datasets'][0]['sa'])/log_distance
        
        
        #Set back threshold to deafault
        requests.post(URLprefix + '/lsss/module/ColorBarModule/threshold/min',json={'value':-82})
        
        
        #THis function may in future replece the one below
        #r = requests.get(URLprefix+'/lsss/module/InterpretationModule/database')
        
        
#        http://localhost:8000/lsss/module/InterpretationModule/config/parameter
        
        
        #Punching inn data
        #This has to be more automated
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
            
        
        
        #Load to database
        r = requests.post(URLprefix + '/lsss/module/InterpretationModule/database', json={'resolution':horizontal_resolution,
                                                                                          'quality':1,
                                                                                          'frequencies':[frequency, frequency]
                                                                                          })
    
    
        r=requests.get(URLprefix + '/lsss/module')
        
    
        #Next 5 nmi
        click(40,50)
        


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
                       URLprefix = 'http://localhost:8000'):
    '''
    Process to make new report files
    
    '''
    
        
    
    
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



    
main_dir = '//ces.imr.no/mea/2018_Redus/SurveyData'
timeSeries = 'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar'
year = '2019'
survey = 'S2019842_PVENDLA_3206'
path2LSSS = 'cmd.exe /c "C:/Program Files/Marec/LSSS 2.7.0/lsss/LSSS.bat"&'

path2LSSS = 'cmd.exe /c "C:/Program Files/Marec/lsss-2.8.0-alpha/lsss/LSSS.bat"&'



#Grab cruise number per time series
df = getNMDinfo()



#Get the spawning survey
cruise_id = df[df['name']==np.unique(df['name'])[17]]['cruiseid']
cruise_name = df[df['name']==np.unique(df['name'])[17]]['name'][0]
    

for cruise in cruise_id[12:len(cruise_id)]: 
    print(cruise)
    DownloadDataToScratch(cruise, cruise_name,main_dir)

cruise = cruise_id[len(cruise_id)-5]

startLSSS(path2LSSS)




automaticInstrument(URLprefix = 'http://localhost:8000',
                     lsssFile='//ces.imr.no/mea/2018_Redus/SurveyData/Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar/2019/S2019842_PVENDLA_3206/ACOUSTIC/LSSS/LSSS_FILES/S2019842_PVendla[3670].lsss',
                     ek60File='//ces.imr.no/mea/2018_Redus/SurveyData/Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar/2019/S2019842_PVENDLA_3206/ACOUSTIC/EK60/EK60_RAWDATA',
                     workFile='//ces.imr.no/mea/2018_Redus/SurveyData/Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar/2019/S2019842_PVENDLA_3206/ACOUSTIC/LSSS/WORK_automatic/',
                     vertical_resolution=10,
                     horizontal_resolution=0.1,
                     frequency=38,
                     reportType=25,
                     TH_min = -55)


runLSSSReportMaker(main_dir,
                       timeSeries,
                       year,
                       survey,
                       vertical_resolution = 10,
                       horizontal_resolution = 0.1, 
                       frequency=38,
                       saveReportToCruice = True,
                       reportType = [20,25],
                       URLprefix = 'http://localhost:8000')



