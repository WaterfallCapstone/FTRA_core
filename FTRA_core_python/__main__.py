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
from Modules import LocationController
from Modules import ProcessController
import time
import cv2
import base64

OperatingSystem = platform.system()
env = Settings.env()
Data = DataController(env)
MotorLocation = Motor.MotorLocation(Data)
if(env.get_config('system','axis') == '4') :
    CamLocation = LocationController.CamLocation4(Data)
    FaceLocation = LocationController.FaceLocation4(Data)
else :
    CamLocation = LocationController.CamLocation5(Data)
    FaceLocation = LocationController.FaceLocation5(Data)

########change params and connections
camera = Camera.FaceCamera(1,"only dir")
data_service = LocationController.DataService("rpf511")
# cameracontroller.run_dev()
p_controller = ProcessController.ProcessController()

stat2main = Queue()

stat2cam = Queue()
cam2main = Queue()
camdata2main = Queue()

# main_p_list = []
cam_p = Process(target = camera.run, args= (stat2cam, cam2main, camdata2main))


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
    print("connected ",int(env.get_config('system','axis')))
    emit("connected", {"axis" : int(env.get_config('system','axis'))})

@io.on("disconnect", namespace="/controller")
def disconnect():
    emit("response")

@io.on("start", namespace="/controller")
def start():
    print("started")
    cam_p.start()
    # main_p = Process(target=p_controller.process_main, args = (io,stat2main,cam2main,camdata2main))
    # main_p_list.append(main_p)
    # main_p.start()
    emit("started")

@io.on("data", namespace="/controller")
def data():
    stat = True
    print("on data")
    if( not cam2main.empty):
        print("image")
        imgjson = cam2main.get()
        stat = imgjson["stat"]
        img = imgjson["image"]
        imgencode = cv2.imencode('.jpg', img)[1]
        stringData = base64.b64encode(imgencode).decode('utf-8')
        b64_src = 'data:image/jpg;base64,'
        stringData = b64_src + stringData
        emit("video", {"image" : stringData})



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
