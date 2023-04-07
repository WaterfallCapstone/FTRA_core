import os
import platform
import numpy as np
from flask import Flask, url_for, render_template
from flask_socketio import SocketIO, emit
import dotenv
from multiprocessing import Process, Queue
import Settings
from Modules import Camera
from Modules import Motor
from Modules import DataController
from Modules import Face
import time

OperatingSystem = platform.system()
env = Settings.env()
Data = DataController(env)
MotorLocation = Motor.MotorLocation(Data)
if(env.get_config('system','axis') == '4') :
    CamLocation = Camera.CamLocation4(Data)
    FaceLocation = Face.FaceLocation4(Data)
else :
    CamLocation = Camera.CamLocation5(Data)
    FaceLocation = Face.FaceLocation5(Data)

########change params and connections
camera = Face.FaceCamera(1,"only dir")
data_service = Face.DataService("rpf511")
cameracontroller = Face.FaceCameraController(camera,data_service)
# cameracontroller.run_dev()

port = 4000


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
    print("connected")
    emit("response")

@io.on("disconnect", namespace="/controller")
def disconnect():
    emit("response")

@io.on("start", namespace="/controller")
def start():
    print("start")
    emit("response")


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.static_folder, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


if __name__ == '__main__':
    io.run(app,host='localhost',port=port)
