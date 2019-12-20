# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 12:47:43 2019

@author: sindrev
"""

import requests, os, json,shutil, time, win32api, win32con
from datetime import date
import numpy as np

baseUrl = 'http://localhost:8000'


def get(path, params=None):
    url = baseUrl + path
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    raise ValueError(url + ' returned status code ' + str(response.status_code) + ': ' + response.text)


def post(path, params=None, json=None, data=None):
    url = baseUrl + path
    response = requests.post(url, params=params, json=json, data=data)
    if response.status_code == 200:
        return response.json()
    if response.status_code == 204:
        return None
    raise ValueError(url + ' returned status code ' + str(response.status_code) + ': ' + response.text)


def delete(path, params=None):
    url = baseUrl + path
    response = requests.delete(url, params=params)
    if response.status_code == 200:
        return None
    raise ValueError(url + ' returned status code ' + str(response.status_code) + ': ' + response.text)



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
    
    #Convert to string
    cruise = str(cruise)
    
    
    #Grab year
    year = cruise[0:4]
    
    
    import sys
    
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
                        vertical_resolution=1,
                        horizontal_resolution=0.1,
                        frequency=38,
                        reportType=25,
                        TH_min = -55,
                        sa_min = 0,
                        acocat = [3,1]):

    
    
    #Function to simulate a instrement person

    
    #Read the lsss version. 
    #This will in future help to keep track of ther version
    lsss_version = get('/lsss/application/info')['version']
    
    
    
    
    #Prepare the lsss database
    print("Disconnected database")
    post("/lsss/application/config/unit/DatabaseConf/connected",json={'value':False})
    print("Create a new database")
    post('/lsss/application/config/unit/DatabaseConf/create',json={'empty':True})
    print("Connect to the new database")
    post("/lsss/application/config/unit/DatabaseConf/connected",json={'value':True})




    #Open the lsss survey file
    print("Opening survey")
    post('/lsss/survey/open', json={'value':lsssFile})
    
    #Sett the location of the data
    print('Load interpretation data')
    post('/lsss/survey/config/unit/DataConf/parameter/WorkDir', json={'value':workFile})
    print('Load echosounder data')
    post('/lsss/survey/config/unit/DataConf/parameter/DataDir', json={'value':ek60File})
    
    #Load all the files
    r=get('/lsss/survey/config/unit/DataConf/files')
    lastIndex = len(r) - 1
#    lastFile = r[-1]['file']
    post('/lsss/survey/config/unit/DataConf/files/selection', json={'firstIndex':0, 'lastIndex':lastIndex})
    	 
    
    
    #Merge all layers into one
    post('/lsss/regions/selection',json={ "all" : True })
    try: 
        post('/lsss/regions/merge-layers')
    except ValueError:
        d=1
    
    
    #Remove all schools
    r=requests.get(URLprefix + '/lsss/regions/region')
    data = json.loads(r.text)
    for dat in data: 
        r=requests.delete(URLprefix+'/lsss/regions/region/'+str(dat['id']))
        
        
    #set ping mapping to distance
    post('/lsss/survey/config/unit/SurveyMiscConf/parameter/PingMapping',json={'value':'Distance'})
        
    
    
    
    #Click to 5 nm resolution
    #This should be replaced with an api function
    click(80,50)
    click(40,50)
    click(80,50)
    
    
    last_ping = -1
    
    
    #Loop through each 5 nm distance
    #This should be replaced so we recognise if we are at the end of the last file
    run = True
    while(run == True):
                
        
        #Grab all the frequencies
        frequencies = get('/lsss/data/frequencies')
        
        sounder_info = get('/lsss/data/config')['transducers']
        
        
        #To be included in future, loop through each frequency
        for freq in frequencies: 
            freq
        
        
        #Sett frequency
        freq = 38000.0
        post('/lsss/data/frequency',json={'value':freq})
        
        #Set to detailed window
        post('/lsss/data/mode',json={'value':'DETAIL'})
        
        
        #Select all layers in window
        post('/lsss/regions/selection',json= { "all" : True})
        
        
        #Sett the lower threshold
        post('/lsss/module/ColorBarModule/threshold/min',json={'value':TH_min})
        
        
        #Wait for all the data to be loaded
        get('/lsss/data/wait')
        

        #Grab data 
        t=get('/lsss/module/PelagicEchogramModule/overlay/AccumulatedSaOverlay/data')
        
        
        #Set the species cathegory to be used
        spec=[]
        spec.append([i for i in t if i['id'] == acocat[0] ][0]['initials'])
        spec.append([i for i in t if i['id'] == acocat[1] ][0]['initials'])
    
    
        
        #Need to check this        
        log_distance = max(t['datasets'][0]['vesselDistance'])-min(t['datasets'][0]['vesselDistance'])
        sa = np.max(t['datasets'][0]['sa'])/log_distance
        
        
        #Trigger
        if sa<sa_min: 
            sa = 0

        
        if not last_ping == max(t['datasets'][0]['vesselDistance']):
            
            #Check if we have a new file
            last_ping = max(t['datasets'][0]['vesselDistance'])
            
            
            #Set back threshold to deafault
            post('/lsss/module/ColorBarModule/threshold/min',json={'value':-82})
            t=get('/lsss/module/PelagicEchogramModule/overlay/AccumulatedSaOverlay/data')
            sa_all = np.max(t['datasets'][0]['sa'])/log_distance
            
            
            
            #get the channel id
            channel_id = [i for i in sounder_info if i['frequency']==freq][0]['id']
            
            
            #Post to scruitiny
            post('/lsss/module/InterpretationModule/scrutiny' ,
                 json={'channels': [{'channelId': channel_id,
                                     'categories': [{'id': acocat[1], 'initials': spec[1], 'assignment': (sa_all-sa)/sa_all},
        {'id': acocat[0], 'initials': spec[0], 'assignment': sa/sa_all}]}]})
        
    
            t = get('/lsss/survey/config/unit/AcousticCategoryConf/category')        
            
    
            
            #Set vertical resolution
            post('/lsss/survey/config/unit/GridConf/parameter/VerticalGridSizePelagic', 
                              json={'value':vertical_resolution})
        
        
            #Load to database
            post('/lsss/module/InterpretationModule/database', json={'resolution':horizontal_resolution,
                                                                                              'quality':1,
                                                                                              'frequencies':[round(freq/1000), round(freq/1000)]
                                                                                              })
        
            
        
#            post('/lsss/package/lsss/action/previousSegment/run',json={"name": True})
            
    
#    CommetModule
#    ConditionalMaskingExtractionModule
#    TrackInfoModule
            #Next 5 nmi
            click(40,50)
        else: 
            break


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
    
    
    #This has to be cleened
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
    
    r = requests.post(URLprefix +'/lsss/package/lsss/action/nextSegment/run')
    
    

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



import sys

if 'win' in sys.platform: 
    main_dir = '//ces.imr.no/mea/2018_Redus/SurveyData'
else: 
    main_dir = '//data/mea/2018_Redus/SurveyData'
    
    
timeSeries = 'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar'
year = '2019'
survey = 'S2019842_PVENDLA_3206'
path2LSSS = 'cmd.exe /c "C:/Program Files/Marec/LSSS 2.7.0/lsss/LSSS.bat"&'

path2LSSS = 'cmd.exe /c "C:/Program Files/Marec/lsss-2.8.0-alpha/lsss/LSSS.bat"&'



#Grab cruise number per time series
df = getNMDinfo()


#Add saildrone
import pandas as pd
d = {'name':'Saildrone','cruiseid':list([2019204,2019207,2019847])}
df = df.append(pd.DataFrame(d))



cruise_id = df[df['name']=='Saildrone']['cruiseid']
cruise_name = df[df['name']=='Saildrone']['name'][0]


for cruise in cruise_id: 
    print(cruise)
    DownloadDataToScratch(cruise, cruise_name,main_dir)


#Get the spawning survey
cruise_id = df[df['name']==np.unique(df['name'])[17]]['cruiseid']
cruise_name = df[df['name']==np.unique(df['name'])[17]]['name'][0]
    

for cruise in cruise_id[12:len(cruise_id)]: 
    print(cruise)
    DownloadDataToScratch(cruise, cruise_name,main_dir)

cruise = cruise_id[len(cruise_id)-5]



startLSSS(path2LSSS)




automaticInstrument(URLprefix = 'http://localhost:8000',
                     lsssFile='E:/Data/2019011_PSAILDRONE_1031/ACOUSTIC/LSSS/LSSS_FILES/S2019001_PSaildrone.lsss',
                     ek60File='E:/Data/2019011_PSAILDRONE_1031/ACOUSTIC/EK80/EK80_RAWDATA',
                     workFile='E:/Data/2019011_PSAILDRONE_1031/ACOUSTIC/LSSS/Work',
                     vertical_resolution=1,
                     horizontal_resolution=0.1,
                     frequency=38,
                     reportType=25,
                     TH_min = -55,
                     sa_min = 200,
                     acocat = [12,1])


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



