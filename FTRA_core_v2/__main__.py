import os
import numpy as np
from flask import Flask, url_for, render_template
from flask_socketio import SocketIO, emit
from Modules import Config, FaceCamera, MotorController
import time
import cv2
import base64

config = Config()

port = config.get_config('system','PORT',"int")
tickrate = config.get_config('system',"tickrate","int") / 1000
camindex = config.get_config('camera','camindex',"int")
baudrate = config.get_config('motor','baudrate',"str")
motor = MotorController(config.get_config('motor','arduinoport',"str"), baudrate)

iscamerarun = False
isfacemesh = False


camera = FaceCamera(index=camindex)
image = None
meshimg = None

def getclientenv():
    return {
                "tickrate" : tickrate, 
                "camindex" : camindex, 
                "iscamrun" : iscamerarun, 
                "isfacemesh" : isfacemesh, 
                "isOpen" : camera.isOpen,
                "arduinoport" : motor.port,
                "baudrate" : motor.baudrate,
                "portlist" : motor.portlist,
                "isarduino" : motor.arduinoexists
            }

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
    emit("getconfig", getclientenv())

@io.on("setconfig", namespace="/controller")
def setconfig(json):
    for key in json.keys():
        if json[key] is None : 
            print("key None")
            continue
        if key == "camera" :
            global camera, camindex, iscamerarun
            if (json['camera'] == True):
                camera.setIndex(camindex)
                iscamerarun = camera.isOpen
            elif (json['camera'] == False):
                iscamerarun = False
        if key == "facemesh" :
            global isfacemesh
            if (json['facemesh'] == True) or (json['facemesh'] == False):
                isfacemesh = json['facemesh']
        if(str(key) == "tickrate") : 
            global tickrate
            if config.exists("system", str(key)) : 
                tickrate = json[key] / 1000
                config.set_config("system",str(key),str(json[key]))
        if(str(key) == "camindex") : 
            if config.exists("camera", str(key)) : 
                camindex = json[key]
                config.set_config("camera",str(key),str(json[key]))
        if(str(key) == "arduinoport") : 
            global motor
            if config.exists("motor", str(key)) : 
                if motor.set_port(str(json[key])):
                    config.set_config("motor",str(key),str(json[key]))
        if(str(key) == "baudrate") : 
            global baudrate
            if config.exists("motor", str(key)) : 
                baudrate = json[key]
                config.set_config("motor",str(key),str(json[key]))
        else: 
            json[key] = "KeyError"
    emit("getconfig", getclientenv())
    
@io.on("getimg", namespace="/controller")
def getimg():
    global iscamerarun, isfacemesh, tickrate, image, meshimg
    cur_time_cont =time.time()
    nex_time_cont = cur_time_cont
    while iscamerarun:
        cur_time_cont = time.time()
        if(cur_time_cont > nex_time_cont):

            isimg = False
            if isfacemesh :
                meshimg = camera.draw_face_mesh_data()
                if meshimg is not None:
                    imgencode = cv2.imencode('.jpg', meshimg)[1]
                    isimg = True
            elif iscamerarun and image is not None:
                imgencode = cv2.imencode('.jpg', image)[1]
                isimg = True
            if isimg:
                stringData = base64.b64encode(imgencode).decode('utf-8')
                b64_src = 'data:image/jpg;base64,'
                stringData = b64_src + stringData
                emit("video", {"image" : stringData})

            nex_time_cont = cur_time_cont + tickrate
        
@io.on("startcam", namespace="/controller")
def startcam():
    global iscamerarun, isfacemesh, tickrate, image, meshimg
    while iscamerarun:
        image = camera.camera_update()

@io.on("startmesh", namespace="/controller")
def startmesh():
    global image, meshimg, isfacemesh
    if isfacemesh:
        while iscamerarun:
            camera.get_face_mesh_data()
            # meshimg = camera.draw_face_mesh_data()


@io.on("stop", namespace="/controller")
def stop():
    global iscamerarun
    iscamerarun = False
    emit("getconfig", getclientenv())



    
    
    
    
    
    
    
    
    




if __name__ == '__main__':
    # print(camera.isOpen)
    print("creating server")
    io.run(app,host='localhost',port=port)
    