import Settings
from Modules import Camera
from Modules import Motor
from Modules import DataController
from Modules import LocationController
import time
import platform
import os
import numpy as np
from multiprocessing import Process
import os



OperatingSystem = platform.system()
env = Settings.env()
Data = DataController(env)
MotorLocation = Motor.MotorLocation(Data)
if(env.get_config('system','axis') == '4') :
    CamLocation = Camera.CamLocation4(Data)
    FaceLocation = LocationController.FaceLocation4(Data)
else :
    CamLocation = Camera.CamLocation5(Data)
    FaceLocation = LocationController.FaceLocation5(Data)

########change params and connections
camera = LocationController.FaceCamera(1,"only dir")
data_service = LocationController.DataService("rpf511")
cameracontroller = LocationController.FaceCameraController(camera,data_service)
# cameracontroller.run_dev()

Data.print_env()
def print_data():
    print("camface_loc_polar : ",Data.camface_loc_polar," , camface_dir_cart : ",Data.camface_dir_cart)
    print("armtip_loc_polar : ",Data.armtip_loc_polar," , armtip_loc_cart : ",Data.armtip_loc_cart," , armtip_dir_polar : ",Data.armtip_dir_polar)
    print("cam_rot : ",CamLocation.cam_rot," , cam_trans : ",CamLocation.cam_trans)
    print("cam_loc_cart : ",Data.cam_loc_cart," , cam_dir_polar : ",Data.cam_dir_polar)
    print("camface_loc_cart : ",FaceLocation.camface_loc_cart," , camface_dir_cart : ",FaceLocation.camface_dir_cart)
    print("face_rot : ",FaceLocation.face_rot," , face_dir_rot : ",FaceLocation.face_dir_rot)
    print("face_trans : ",FaceLocation.face_trans," , face_dir_trans : ",FaceLocation.face_dir_trans)

tickrate = float(env.get_config('system','tickrate')) / 1000
nexttime = time.time() + tickrate
while cameracontroller.camera.cap.isOpened():
    currenttime = time.time()
    cameracontroller.camera.camera_update()
    if not cameracontroller.camera.success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue
    
    cameracontroller.camera.get_face_mesh_data()
    cameracontroller.camera.draw_face_mesh_data()
    if (cameracontroller.camera.results.multi_face_landmarks == None):
        continue
        
    data = cameracontroller.camera.get_data()
    cameracontroller.camera.dir_vector = cameracontroller.camera.calculate_face_dir_vector(data)
    cameracontroller.camera.face_loc = cameracontroller.camera.get_face_loc(data)
    cameracontroller.camera.eye = cameracontroller.camera.check_eye(data)
    cameracontroller.camera.current_face_dir_state()

    face_loc_raw = cameracontroller.camera.face_loc
    
    Data.set_camface_loc_polar(np.array([50, (0.5-face_loc_raw[0]) * np.pi / 6, np.pi / 2 - (0.5-face_loc_raw[1]) * np.pi / 8]))

    if(currenttime > nexttime):
        nexttime = currenttime + tickrate
        if(OperatingSystem == "Windows"):
            os.system('cls')
        else:
            os.system('clear')
        print(currenttime)
        Data.set_armtip_loc_polar(MotorLocation.cal_armtip_loc_polar())
        Data.set_armtip_loc_cart(MotorLocation.armtip_loc_polar_to_cart())
        Data.set_armtip_dir_polar(MotorLocation.cal_armtip_dir_polar())

        Data.set_cam_loc_cart(CamLocation.cal_cam_loc_cart())
        Data.set_cam_dir_polar(CamLocation.cal_cam_dir_polar())

        face_loc_cart, face_lookat = FaceLocation.cal_face_loc()
        Data.set_face_loc_cart(face_loc_cart)
        Data.set_face_lookat(face_lookat)
        print_data()



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



