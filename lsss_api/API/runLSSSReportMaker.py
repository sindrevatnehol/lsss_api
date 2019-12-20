# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 10:59:45 2019

@author: sindrev
"""





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
    Process to make new report files from all avaliable data
    '''
    
    import os
    import API
    
    
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
    
        
    
    #Loop through each data version
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


            #Add report folder if this do not exist
            if not os.path.exists(cruise_dir+'ACOUSTIC/LSSS/'+'REPORTS'):
                os.makedirs(cruise_dir+'ACOUSTIC/LSSS/'+'REPORTS')
            
            
            
            #Get path and make the folder for the reports
            print('Do version: ' + EKdata+'_'+WORK_version)
            reportFileRaw = cruise_dir+'ACOUSTIC/LSSS/REPORTS/'+'REPORTS_'+EKdata+'_'+WORK_version+'/'
            if not os.path.exists(reportFileRaw):
                os.makedirs(reportFileRaw)


            #Filename of the report
            luf25file=reportFileRaw+'echosounder'+survey
        
            
            #Grab location of the data
            lsssFile = cruise_dir+'ACOUSTIC/LSSS/LSSS_FILES/'+LSSS_versions
            ek60File= cruise_dir+'ACOUSTIC/'+EKdata+'/'+EKdata+'_RAWDATA'
            
            
            
            
            #Prepare for an automatic rutine
            res = [i for i in WORK_versions if 'SNAP' in i] 
            if(len(res)>1): 
                print('Several SNAP, check code')
                asdf
                break
            
            
            
            #Run LSSS API
            API.runReportFromRaw(URLprefix,
                             lsssFile,
                             ek60File,
                             workFile=workFile,
                             luf25file=luf25file,
                             vertical_resolution=vertical_resolution,
                             horizontal_resolution=horizontal_resolution,
                             frequency=frequency,
                             reportType=reportType)
