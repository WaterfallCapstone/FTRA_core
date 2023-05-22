import os
import numpy as np
from flask import Flask, url_for, render_template
from flask_socketio import SocketIO, emit
from Modules import Config


config = Config()


tickrate = config.get_config('camera',"TICKRATE","int") / 1000
port = config.get_config('system','PORT',"int")
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
    emit("connected", {"tickrate" : tickrate, "iscamrun" : iscamerarun, "isfacemesh" : isfacemesh})
    return

@io.on("disconnect", namespace="/controller")
def disconnect():
    emit("response")
    return

@io.on("setconfig", namespace="/controller")
def disconnect(json):
    for key in json.keys():
        if config.exists("camera", str(key)) : 
            config.set_config("camera",str(key),str(json[key]))
        else: 
            json[key] = "KeyError"
    emit("setconfig", json)
    
    
    
    
    
    
    
    
    


@io.on("connect", namespace="/data")
def connect():
    emit("connected", {"tickrate" : tickrate, "iscamrun" : iscamerarun, "isfacemesh" : isfacemesh})

@io.on("disconnect", namespace="/data")
def disconnect():
    emit("response")

    
    
    
    
    
    
    
    
    
    
    




if __name__ == '__main__':
    
    print("creating server")
    io.run(app,host='localhost',port=port)
  