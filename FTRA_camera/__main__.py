import os
import numpy as np
from flask import Flask, url_for, render_template
from flask_socketio import SocketIO, emit
from Modules import Config
from Modules import FaceCamera
import time
import cv2
import base64

config = Config()

port = config.get_config('system','PORT',"int")
tickrate = config.get_config('camera',"tickrate","int") / 1000
camindex = config.get_config('camera','camindex',"int")
iscamerarun = False
isfacemesh = False
camera = FaceCamera(index=camindex)
image = None
meshimg = None

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(ROOT_PATH, "src")
TEMPLATE_FOLDER = STATIC_FOLDER

app = Flask(
  __name__,
  static_url_path="/static/",
  static_folder=STATIC_FOLDER,
  template_folder=TEMPLATE_FOLDER
)
app.config['SECRET_KEY'] = 'possward'
io = SocketIO(app,cors_allowed_origins="*")

@io.on("connect", namespace="/controller")
def connect():
    emit("connected")
    return

@io.on("disconnect", namespace="/controller")
def disconnect():
    emit("response")
    return

@io.on("getconfig", namespace="/controller")
def getconfig():
    emit("getconfig", {"tickrate" : tickrate, "camindex" : camindex, "iscamrun" : iscamerarun, "isfacemesh" : isfacemesh, "isOpen" : camera.isOpen})

@io.on("setconfig", namespace="/controller")
def setconfig(json):
    global tickrate, tickrate, iscamerarun, isfacemesh
    for key in json.keys():
        if key == "camera" :
            global camera, camindex
            if (json['camera'] == True):
                camera.setIndex(camindex)
                iscamerarun = camera.isOpen
            elif (json['camera'] == False):
                iscamerarun = False
                
        if key == "facemesh" :
            if (json['facemesh'] == True) or (json['facemesh'] == False):
                isfacemesh = json['facemesh']
        if config.exists("camera", str(key)) : 
            if(str(key) == "tickrate") : 
                tickrate = json[key] / 1000
            if(str(key) == "camindex") : 
                camindex = json[key]
            config.set_config("camera",str(key),str(json[key]))
        else: 
            json[key] = "KeyError"
    emit("getconfig", {"tickrate" : tickrate, "camindex" : camindex, "iscamrun" : iscamerarun, "isfacemesh" : isfacemesh, "isOpen" : camera.isOpen})
    
@io.on("getimg", namespace="/controller")
def getimg():
    global iscamerarun, isfacemesh, tickrate, image, meshimg
    cur_time_cont =time.time()
    nex_time_cont = cur_time_cont
    while iscamerarun:
        cur_time_cont = time.time()
        if(cur_time_cont > nex_time_cont):

            if image is not None:
                if isfacemesh:
                    imgencode = cv2.imencode('.jpg', meshimg)[1]
                else:
                    imgencode = cv2.imencode('.jpg', image)[1]
                stringData = base64.b64encode(imgencode).decode('utf-8')
                b64_src = 'data:image/jpg;base64,'
                stringData = b64_src + stringData
                emit("video", {"image" : stringData})

            nex_time_cont = cur_time_cont + tickrate
        
@io.on("start", namespace="/controller")
def start():
    global iscamerarun, isfacemesh, tickrate, image, meshimg
    cur_time_cont = time.time()
    nex_time_cont = cur_time_cont
    print(iscamerarun)
    while iscamerarun:
        cur_time_cont = time.time()
        if(cur_time_cont > nex_time_cont):
            image = camera.camera_update()
            # if isfacemesh:
            #     imgencode = cv2.imencode('.jpg', image)[1]
            
            nex_time_cont = cur_time_cont + tickrate

@io.on("stop", namespace="/controller")
def stop():
    global iscamerarun
    iscamerarun = False
    emit("getconfig", {"tickrate" : tickrate, "camindex" : camindex, "iscamrun" : iscamerarun, "isfacemesh" : isfacemesh, "isOpen" : camera.isOpen})

@io.on("connect", namespace="/data")
def connect():
    emit("connected", {"tickrate" : tickrate, "iscamrun" : iscamerarun, "isfacemesh" : isfacemesh})

@io.on("disconnect", namespace="/data")
def disconnect():
    emit("response")



    
    
    
    
    
    
    
    
    
    
    




if __name__ == '__main__':
    # print(camera.isOpen)
    print("creating server")
    io.run(app,host='localhost',port=port)
    