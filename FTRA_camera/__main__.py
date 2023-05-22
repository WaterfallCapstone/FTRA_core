import os
import numpy as np
from flask import Flask, url_for, render_template
from flask_socketio import SocketIO, emit
from Modules import Config


config = Config()

port = config.get_config('system','PORT',"int")
tickrate = config.get_config('camera',"tickrate","int") / 1000
camindex = config.get_config('camera','camindex',"int")
iscamerarun = False
isfacemesh = False

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
    emit("getconfig", {"tickrate" : tickrate, "camindex" : camindex, "iscamrun" : iscamerarun, "isfacemesh" : isfacemesh})

@io.on("setconfig", namespace="/controller")
def setconfig(json):
    for key in json.keys():
        if config.exists("camera", str(key)) : 
            if(str(key) == "tickrate") : 
                global tickrate
                tickrate = json[key] / 1000
                print("tickrate ",tickrate)
                print(type(tickrate))
            if(str(key) == "camindex") : 
                global camindex
                camindex = json[key]
                print("camindex ",camindex)
                print(type(camindex))
            config.set_config("camera",str(key),str(json[key]))
        else: 
            json[key] = "KeyError"
    emit("getconfig", {"tickrate" : tickrate, "camindex" : camindex, "iscamrun" : iscamerarun, "isfacemesh" : isfacemesh})
    
    
    
    
    
    
    
    
    


@io.on("connect", namespace="/data")
def connect():
    emit("connected", {"tickrate" : tickrate, "iscamrun" : iscamerarun, "isfacemesh" : isfacemesh})

@io.on("disconnect", namespace="/data")
def disconnect():
    emit("response")

    
    
    
    
    
    
    
    
    
    
    




if __name__ == '__main__':
    
    print("creating server")
    io.run(app,host='localhost',port=port)
  