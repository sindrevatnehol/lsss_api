# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 10:55:52 2019

@author: sindrev
"""



def startLSSS(path2LSSS): 
    '''
    startLSSS()
    
    Description: 
        This package is an automated way to start the LSSS software, where a
        click event is automatically enforced. 
        
    usage: 
        startLSSS(path2LSSS)
        
        path2LSSS is the path to the lsss batch file
    
    '''
    
    
    
    import subprocess, time
    
    
#    if not os.path.isfile(path2LSSS): 
#        print('The LSSS path do not exist')
    
    
    #To simulate mouse click
    def click(x,y):
        import  win32api, win32con
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)





    
    lsssCommand = path2LSSS
    subprocess.Popen(lsssCommand,shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=None)
    time.sleep(15)
    click(1200,590)
    time.sleep(10)
