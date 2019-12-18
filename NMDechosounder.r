library(Rstox)
library(stringi)
library(stringr)



#Get all surveys from nmd
nmdinfo <- getNMDinfo('cs')



#Directory to where to store the data
survey_dir <- '//ces.imr.no/mea/2018_Redus/SurveyData'




#Directory to the cruise data
server_directory <-'//ces.imr.no/cruise_data'




#Loop through each survey
# cruise_series <- c('`Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar`')



#Make folder to containe the timeseries data
dir.create(paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',sep='/'), showWarnings = FALSE)


#Get all cruise_id of the timeseries
cruise_id <- nmdinfo$`Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar`$Cruise
# year_id <- nmdinfo$`Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar`$Year

cruise<-cruise_id[length(cruise_id)-5]


#Loop through each survey
for(cruise in cruise_id){
  print(paste('Downloading data from:', cruise))
  year <- (substring(cruise,1,4))
  
  #Make year directory
  dir.create(paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',year,sep='/'), showWarnings = FALSE)
  
  #Get all vessel in the year
  vessels <- (list.dirs(paste0('//ces.imr.no/cruise_data/',year), recursive = FALSE))
  
  #Get current vessel name
  vessel_name <- vessels[grepl(cruise,vessels)]
  
  
  
  if(length(vessel_name)>1)stop('multiple vessels with same id')
  
  
  
  
  
  #Make vessel folder
  print('Make standart directories')
  dir.create(Survey_folder <- paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                   year,strsplit(vessel_name,split = '/')[[1]][6],sep='/'), showWarnings = FALSE)
  dir.create(ACOUSTIC_folder <- paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                   year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC',sep='/'), showWarnings = FALSE)
  dir.create(paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                                  year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','LSSS',sep='/'), showWarnings = FALSE)
  # dir.create(WORK_folder <- paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
  #                                 year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','LSSS','WORK',sep='/'), showWarnings = FALSE)
  dir.create(LSSS_files_folder <- paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                                  year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','LSSS','LSSS_FILES',sep='/'), showWarnings = FALSE)
  
  
  
  

  #Get all files with path
  files <-(list.files(vessel_name, recursive = TRUE,full.names = TRUE))
  dire <- (list.dirs(vessel_name, recursive = TRUE,full.names = TRUE))

  
  #Get those linked to interpretation
  files_to_copy<-files[grepl('.work',files)|grepl('.snap',files)]
  
  
  #seperate between files and paths
  library(gsubfn)
  m <- strapply(files_to_copy, '(.*)/(.*)', ~ c(FPath=x, FileName=y), simplify=rbind)
  Final <- as.data.frame(m, stringsAsFactors = FALSE)
  
  
  #Copy all interpertation in different folders
  v=1
  for (f_path in unique(Final$FPath)){
    dir.create(WORK_folder <- paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                                    year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','LSSS',paste0('WORK_V',toString(v)),sep='/'), showWarnings = FALSE)
    dir.create(SNAP_folder <- paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                                    year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','LSSS',paste0('SNAP_V',toString(v)),sep='/'), showWarnings = FALSE)
    v=v+1
    
    copy_these_files <- Final[Final$FPath==f_path,]$FileName
    for(f in copy_these_files){
      print(f)
      if(grepl('.snap',f)){
        new_file <- paste(SNAP_folder,f,sep='/')
        file.copy(paste(f_path,f,sep='/'),new_file)
      }else{
      new_file <- paste(WORK_folder,f,sep='/')
      file.copy(paste(f_path,f,sep='/'),new_file)
      }
    }
  }
  
  
  
  #Find all .lsss files  
  lsss_files <- (list.files(vessel_name, recursive = TRUE,full.names = TRUE,pattern = "\\.lsss$"))

  v=1
  for(lsss_file in lsss_files){
    new_file <- paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','LSSS','LSSS_FILES',paste0('V',toString(v),'_',basename(lsss_file)),sep='/')
    file.copy(lsss_file,new_file)
    v=v+1
  }  
  
  
  
  
  #Get those linked to the raw files
  #NB: All raw files are copied as these is identical
  files_to_copy<-files[(grepl('.raw',files)|grepl('.bot',files)|grepl('.idx',files))&(grepl('EK',files))]
  
  if(length(files_to_copy)>0){
    
    
    
    print('Copying raw files')
    for(f in files_to_copy){
      print(f)
      if(grepl('EK60',f)){
        
        dir.create(paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                                    year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','EK60',sep='/'), showWarnings = FALSE)
        dir.create(EK_folder <- paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                                      year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','EK60','EK60_RAWDATA',sep='/'), showWarnings = FALSE)
        
        if (any(grepl('ORIGINAL',files_to_copy)>0)){
          print('Two sets of data')
          dir.create(EK_folder_original <- paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                                        year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','EK60','EK60_RAWDATA_V0',sep='/'), showWarnings = FALSE)}
          
        
      
    }
      if(grepl('EK80',f)){
      dir.create(paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                       year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','EK80',sep='/'), showWarnings = FALSE)
      dir.create(EK_folder <- paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                                    year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','EK80','EK80_RAWDATA',sep='/'), showWarnings = FALSE)
      
      if (any(grepl('ORIGINAL',files_to_copy)>0)){
        
        print('Two sets of data')
        dir.create(EK_folder_original <- paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                                      year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','EK80','EK80_RAWDATA_V0',sep='/'), showWarnings = FALSE)}
      
        
    # 
    # new_file <- paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','EK80','EK80_RAWDATA',basename(f),sep='/')
    # 
    # file.copy(f,new_file)
      
      }
      
      
      grepl(f,'EK60_ORIGINALRAWDATA')
      if(grepl('ORIGINAL',f)){
        new_file <- paste(EK_folder_original,sub('.*/', '', f),sep='/')
      }else{
      new_file <- paste(EK_folder,sub('.*/', '', f),sep='/')
      }
      file.copy(f,new_file)
    }
    }
  
  
  
  files_to_copy<-files[grepl('korona',files)]
  if(length(files_to_copy)>0){
  m <- strapply(files_to_copy, '(.*)/(.*)', ~ c(FPath=x, FileName=y), simplify=rbind)
  Final <- as.data.frame(m, stringsAsFactors = FALSE)
  
  #Copy all interpertation in different folders
  v=1
  for (f_path in unique(Final$FPath)){
    dir.create(KORONA_folder <- paste(survey_dir,'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar',
                                    year,strsplit(vessel_name,split = '/')[[1]][6],'ACOUSTIC','LSSS',paste0('KORONA_V',toString(v)),sep='/'), showWarnings = FALSE)
    v=v+1
    
    copy_these_files <- Final[Final$FPath==f_path,]$FileName
    for(f in copy_these_files){
      print(f)
      new_file <- paste(KORONA_folder,f,sep='/')
      file.copy(paste(f_path,f,sep='/'),new_file)
    }
  }
  }
  
}

