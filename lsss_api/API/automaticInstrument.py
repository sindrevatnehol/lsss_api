# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 11:04:45 2019

@author: sindrev
"""





def automaticInstrument(baseUrl,
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

        
    import requests, json
    import numpy as np
    
        
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
        import  win32api, win32con
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

    
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
    r=requests.get(baseUrl + '/lsss/regions/region')
    data = json.loads(r.text)
    for dat in data: 
        r=requests.delete(baseUrl+'/lsss/regions/region/'+str(dat['id']))
        
        
    #set ping mapping to distance
    post('/lsss/survey/config/unit/SurveyMiscConf/parameter/PingMapping',json={'value':'Distance'})
        
    
    
    
    #Click to 5 nm resolution
    #This should be replaced with an api function
    click(80,50)
    click(40,50)
    click(80,50)
#    post('/lsss/package/lsss/action/nextegment/run',json={"name": True})
    
    
    
    #Set to browser window
    post('/lsss/data/mode',json={'value':'BROWSE'})
        
        
        
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

