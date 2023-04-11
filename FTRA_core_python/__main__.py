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
camera = Camera.FaceCamera(0,Data,"only dir")
data_service = LocationController.DataService("rpf511")
# cameracontroller.run_dev()
p_controller = ProcessController.ProcessController()



isrunning = False
command = ""

port = 4000
tickrate = float(env.get_config('system','tickrate')) / 1000


# def process_main(q_in, q_out):
#     global isrunning, Data, tickrate
#     isrunning = True
#     cur_time_cam =time.time()
#     nex_time_cam = cur_time_cam
#     print("on data")
#     while isrunning:
#         cur_time_cam = time.time()
#         if(not q_in.empty()):
#             q_data = q_in.get()
#             command = q_data["command"]
#             if(command == "stop"):
#                 isrunning = False
#             if(command == "image"):
#                 print("onimage")
#                 q_out.put({"image" : Data.get_image(), "isface" : Data.get_isface()})
        
#         if(cur_time_cam > nex_time_cam):
#             camera.run()
            
#             nex_time_cam = cur_time_cam + tickrate
#     return

# q_in = Queue()
# q_out = Queue()
# main_process = Process(target=process_main, args=(q_in,q_out))



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
    emit("mainprocess", {"stat" : True})
    # main_process.start()
    # main_p = Process(target=p_controller.process_main, args = (io,stat2main,cam2main,camdata2main))
    # main_p_list.append(main_p)
    # main_p.start()
    
@io.on("stop", namespace="/controller")
def stop():
    print("stop")
    emit("mainprocess", {"stat" : False})
    global isrunning
    isrunning = False
    # global q_in
    # q_in.put({"command" : "stop"})



@io.on("video", namespace="/controller")
def video():
    global isrunning
    isrunning = True
    cur_time_cam =time.time()
    nex_time_cam = cur_time_cam
    print("on data")
    while isrunning:
        cur_time_cam = time.time()
        if(cur_time_cam > nex_time_cam):
            camera.run()
            imgencode = cv2.imencode('.jpg', camera.image)[1]
            stringData = base64.b64encode(imgencode).decode('utf-8')
            b64_src = 'data:image/jpg;base64,'
            stringData = b64_src + stringData
            isface = Data.get_isface()
            emit("video", {"image" : stringData, "isface" : isface})
            if isface :
                camface_dir = Data.get_camface_dir_cart()
                camface_loc = Data.get_camface_loc_polar()
                emit("face_from_cam", {"dir_vector" : [camface_dir[0],camface_dir[1],camface_dir[2]], "face_loc" : [camface_loc[0],camface_loc[1],camface_loc[2]]})
            
            
            data =[np.random.randint(0,10),np.random.randint(0,10),np.random.randint(0,10),np.random.randint(0,10),np.random.randint(0,10)]
            emit("motor", {"motorvalue" : data})
            
            nex_time_cam = cur_time_cam + tickrate
    print("running done")
    return
        



# @io.on("image", namespace="/controller")
# def image():
#     global q_in, q_out
#     q_in.put({"command" : "image"})
#     while True:
#         if(not q_out.empty()):
#             print("yes queue")
#             imagedata = q_out.get()
#             emit("video", imagedata)
#             break
#         else:
#             print("no queue")

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
    
    print("creating server")
    io.run(app,host='localhost',port=port)
