# Camera    
## Config Variables  
* TICKRATE  
    camera update rate  
    Type : INT  
    Unit : ms  
    tickrate 30 : about 33fps  
  
* camindex  
    Type : INT  
    Unit : idx  
    camera index  
  
## Config control  

  
## API  
socket  
### /controller  
    control modules and change config  
  
* /getconfig  
    - Requests  
        headers : {}  
        params : {}  
    - Responses  
        on : getconfig  
        params : {  
            "tickrate",  
            "camindex",  
            "iscamrun",  
            "isfacemesh",  
            "isOpen"  
        }  
        - tickrate  
            current camera update tickrate  
            Type : INT  
        - camindex  
            current camera index  
            Type : INT  
          
        - iscamrun  
            True if camera is running   
            Type : BOOL  
          
        - isfacemesh  
            True if mediapipe facemesh detection  
            Type : BOOL  
        - isOpen  
            True if there is camera with index 'camindex'  
          
* /setconfig  
    - Requests  
        headers : {}  
        params : {  
            configkeyname : data  
        }  
        - configkeyname  
            "camera" : BOOL  
            "facemesh" : BOOL  
            "tickrate" : INT  
            "camindex" : INT  
      
    - Responses  
        on : getconfig  
        params : {  
            "tickrate",  
            "camindex",  
            "iscamrun",  
            "isfacemesh",  
            "isOpen"  
        }  
        params same with /getconfig  
  
* /getimg  
    get camera video img stream if iscamrun is True and isOpen is True by 'tickrate'  
    if isfacemesh is True, server will send videostream with face mesh  
    - Requests  
        headers : {}  
        params : {}  
      
    - Responses  
        on : /video  
        params : {  
            "image"  
        }  
        - image  
            stream img  
            Type : .jpg:base64  
  
* /start  
    camera run if iscamrun is True  
    camera run in backend. if you want to get stream, emit /  getimg  
    - Requests  
        headers : {}  
        params : {}  
      
    - Responses  
        no response  
  
* /startmesh  
    detect face mesh on img if camera is running  
    detection in backend. if you want to get stream, emit /getimg  
    - Requests  
        headers : {}  
        params : {}  
      
    - Responses    
        no response  
  
* /stop    
    stop camera run, mesh calculation, and video img stream  
    - Requests  
        headers : {}  
        params : {}  
      
    - Responses    
        on : getconfig    
        params : {  
            "tickrate",  
            "camindex",  
            "iscamrun",  
            "isfacemesh",  
            "isOpen"  
        }  
        params same with /getconfig  
  
### /data  
* /start    
    camera run if iscamrun is True    
    camera run in backend. if you want to get stream, emit /getimg  
    - Requests  
        headers : {}  
        params : {}  
    
    - Responses  
        no response  

* /startmesh    
    detect face mesh on img if camera is running    
    detection in backend. if you want to get stream, emit /  getimg    
    - Requests  
        headers : {}  
        params : {}
    
    - Responses  
        no response  

* /getlandmarks      
    get face landmarks by 'tickrate'    
    - Requests    
        headers : {}    
        params : {}    
    
    - Responses      
        on : landmarks  
        params : {  
            "landmark"  
        }
        - landmark    
