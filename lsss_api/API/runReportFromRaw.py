# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 10:49:30 2019

@author: sindrev
"""


def runReportFromRaw(baseUrl,
                     lsssFile,
                     ek60File,
                     workFile,
                     luf25file,
                     vertical_resolution=10,
                     horizontal_resolution=0.1,
                     frequency=38,
                     reportType=25):
    
    
    
    
    import requests, json
    from datetime import date
    
            
        
    
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



    
    #Grab lsss verssion
    r = requests.get(baseUrl + '/lsss/application/info')
    lsss_version = json.loads(r.content)['version']
    
    print("Disconnected database")
    post("/lsss/application/config/unit/DatabaseConf/connected", json={'value':False})
    
    print("Create a new database")
    post('/lsss/application/config/unit/DatabaseConf/create') #, json={'empty':True})
    
    print("Connect to the new database")
    r = requests.post(baseUrl + "/lsss/application/config/unit/DatabaseConf/connected", json={'value':True})
    print("Connect to the new database: " + str(r.status_code))
    
    print("Opening survey")
    post('/lsss/survey/open', json={'value':lsssFile})
    
    
    print('Load interpretation data')
    post('/lsss/survey/config/unit/DataConf/parameter/WorkDir', json={'value':workFile})
    
    print('Load echosounder data')
    post('/lsss/survey/config/unit/DataConf/parameter/DataDir', json={'value':ek60File})
    
        
    #Hack to load all files
    #LSSS only load those files set in the .lsss file. T
    #Underneath will load the whole survey
    r = requests.get(baseUrl + '/lsss/survey/config/unit/DataConf/files')
    firstIndex = 0
    lastIndex = len(r.json()) - 1
    post('/lsss/survey/config/unit/DataConf/files/selection', json={'firstIndex':firstIndex, 'lastIndex':lastIndex})
        
        
    # Wait until the program is ready for further processing
    get('/lsss/data/wait')


    #Set the grid size        
    post('/lsss/survey/config/unit/GridConf/parameter/VerticalGridSizePelagic', 
                      json={'value':vertical_resolution})
    
    post('/lsss/survey/config/unit/GridConf/parameter/VerticalGridSizeBottom', 
                      json={'value':vertical_resolution})
               
    
    get('/lsss/data/wait')
    
    # Store to local LSSS DB
    print('Storing to database (This takes time)')
    post('/lsss/module/InterpretationModule/database', json={'resolution':horizontal_resolution,
                                                                                      'quality':1,
                                                                                      'frequencies':[frequency, frequency]
                                                                                      })
    
    
    
    get('/lsss/data/wait')
    
    
    #This has to be cleened
    if type(reportType)==int: 
        print('Making luf:'+ str(reportType))
        r = requests.get(baseUrl + '/lsss/database/report/'+str(reportType))
        print("Generating LUF"+str(reportType)+" from RAW: " + str(r.status_code))
        
         # Write it to disk
        if r.status_code == 200:
            print('Write report')
            with open(luf25file+'L_'+str(reportType)+'_LSSSV_'+lsss_version+'_T'+date.today().strftime("%Y%m%d")+'.xml', 'w+') as f:
                f.write(r.text)
    elif type(reportType)==list:
        for luftype in reportType: 
            print('Making luf:'+ str(luftype))
            r = requests.get(baseUrl + '/lsss/database/report/'+str(luftype))
            print("Generating LUF"+str(luftype)+" from RAW: " + str(r.status_code))
            
             # Write it to disk
            if r.status_code == 200:
                print('Write report')
                with open(luf25file+'L_'+str(luftype)+'_LSSSV_'+lsss_version+'.xml', 'w+') as f:
                    f.write(r.text)
    print('Finnished writing report')

    get('/lsss/data/wait')
    
    post('/lsss/survey/close')
    
    