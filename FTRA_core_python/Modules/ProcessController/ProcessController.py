from multiprocessing import Process, Queue
import time
import cv2
import base64

class ProcessController:
    def __init__(self):
        self.isrunning = False
        pass
    
    # def set_isrunning(self):
    #     return
    
    # def process_main(self, q_in, q_out):
    #     cur_time_cam =time.time()
    #     nex_time_cam = cur_time_cam
    #     print("on data")
    #     while self.isrunning:
    #         cur_time_cam = time.time()
    #         if(cur_time_cam > nex_time_cam):
    #             camera.run()
    #             imgencode = cv2.imencode('.jpg', camera.image)[1]
    #             stringData = base64.b64encode(imgencode).decode('utf-8')
    #             b64_src = 'data:image/jpg;base64,'
    #             stringData = b64_src + stringData
    #             isface = Data.get_isface()
    #             emit("video", {"image" : stringData, "isface" : isface})
    #             if isface :
    #                 camface_dir = Data.get_camface_dir_cart()
    #                 camface_loc = Data.get_camface_loc_polar()
    #                 emit("face_from_cam", {"dir_vector" : [camface_dir[0],camface_dir[1],camface_dir[2]], "face_loc" : [camface_loc[0],camface_loc[1],camface_loc[2]]})
                
                
    #             data =[np.random.randint(0,10),np.random.randint(0,10),np.random.randint(0,10),np.random.randint(0,10),np.random.randint(0,10)]
    #             emit("motor", {"motorvalue" : data})
                
    #             nex_time_cam = cur_time_cam + tickrate
    #     return