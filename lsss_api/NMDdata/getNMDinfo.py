

    
def getNMDinfo():
    '''
    getNMDinfo()
    
    Description: 
        This package grabs the information from the nmd
        
    usage: 
        getNMDinfo()
    
    '''
        
    
    import urllib.request
    import xmltodict
    import pandas as pd
    import numpy as np
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
        
        
        