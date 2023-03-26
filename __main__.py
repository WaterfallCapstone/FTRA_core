import Settings
from Modules import Camera
from Modules import Motor
from Modules import DataController
from Modules import Face
import time
import platform
import os


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

Data.print_env()
# def print_data():
#     print("camface_loc_polar : ",Data.camface_loc_polar," , camface_dir_cart : ",Data.camface_dir_cart)
#     print("armtip_loc_polar : ",Data.armtip_loc_polar," , armtip_loc_cart : ",Data.armtip_loc_cart," , armtip_dir_polar : ",Data.armtip_dir_polar)
#     print("cam_rot : ",CamLocation.cam_rot," , cam_trans : ",CamLocation.cam_trans)
#     print("cam_loc_cart : ",Data.cam_loc_cart," , cam_dir_polar : ",Data.cam_dir_polar)
#     print("camface_loc_cart : ",FaceLocation.camface_loc_cart," , camface_dir_cart : ",FaceLocation.camface_dir_cart)
#     print("face_rot : ",FaceLocation.face_rot," , face_dir_rot : ",FaceLocation.face_dir_rot)
#     print("face_trans : ",FaceLocation.face_trans," , face_dir_trans : ",FaceLocation.face_dir_trans)

# tickrate = float(env.get_config('system','tickrate')) / 1000
# nexttime = time.time() + tickrate
# # while(True):
# #     currenttime = time.time()
# #     if(currenttime > nexttime):
# #         nexttime = currenttime + tickrate
# #         if(OperatingSystem == "Windows"):
# #             os.system('cls')
# #         else:
# #             os.system('clear')
# #         print(currenttime)

# Data.set_armtip_loc_polar(MotorLocation.cal_armtip_loc_polar())
# Data.set_armtip_loc_cart(MotorLocation.armtip_loc_polar_to_cart())
# Data.set_armtip_dir_polar(MotorLocation.cal_armtip_dir_polar())

# Data.set_cam_loc_cart(CamLocation.cal_cam_loc_cart())
# Data.set_cam_dir_polar(CamLocation.cal_cam_dir_polar())

# face_loc_cart, face_lookat = FaceLocation.cal_face_loc()
# Data.set_face_loc_cart(face_loc_cart)
# Data.set_face_lookat(face_lookat)


# print_data()