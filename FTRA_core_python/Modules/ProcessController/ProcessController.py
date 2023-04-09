from multiprocessing import Process, Queue
import time
import cv2
import base64

class ProcessController:
    def __init__(self):
        pass
    
    def process_main(self,socket,stat_q,cam_q,cam_data_q):
        while True:
            if not cam_q.empty():
                image = cam_q.get()
                # socket.emit("image",image)
            if not cam_data_q.empty():
                imgjson = cam_data_q.get()
                stat = imgjson["stat"]
                img = imgjson["image"]
                imgencode = cv2.imencode('.jpg', img)[1]
                stringData = base64.b64encode(imgencode).decode('utf-8')
                b64_src = 'data:image/jpg;base64,'
                stringData = b64_src + stringData
                # emit("video", stringData)