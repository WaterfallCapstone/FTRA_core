import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
# mp_face_geometry = mp.solutions.face_geometry


import numpy as np
import os
import platform
import base64

class FaceCamera:
    def __init__(self, index,data, mode = "dev"):
        self.data = data
        self.cap = cv2.VideoCapture(index)
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)     
        self.mp_face = mp.solutions.face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5)
        self.success, self.image = self.cap.read()
        # self.results = self.face_mesh.process(self.image)
        self.results = None
        # self.loop = 0
        self.dir_vector = np.array([0.0,0.0,0.0])
        self.dir_state = 0
        self.mode = mode
        self.face_loc = np.array([0.0,0.0,0.0])
        self.eye = [0,0]
        self.OS = platform.system()
        # [up, down, left, right,  leftblink, rightblink]
        self.params = [-0.22,0.12,-0.5,0.2,  0.018, 0.018]

        self.base_distance = 50
        self.base_width = 10.0
        self.frame_width = 640
        self.frame_height = 480
        self.focal_length = 100

        self.mp_face_width = -1
        # self.distance = 50
        
    def camera_update(self):
        self.success, self.image = self.cap.read()
        # if not self.success:
            # self.image = cv2.flip(self.image, 1)
    
    def set_params(self,data):
        self.params = data

    def get_face_mesh_data(self):
        # self.image.flags.writeable = False
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.results = self.face_mesh.process(self.image)
    
    def draw_face_mesh_data(self):
        self.image.flags.writeable = True
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
        if self.results.multi_face_landmarks:
            for face_landmarks in self.results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=self.image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=self.image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=self.image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())
                # Flip the image horizontally for a selfie-view display.
        # cv2.imshow('MediaPipe Face Mesh',self.image)
    
    def get_data(self):
        # print (self.results.face_geometry)
        for face_landmarks in self.results.multi_face_landmarks:
            result = face_landmarks.landmark
        return result
    
    def release(self):
        self.cap.release()
    
    def get_loc_cart(self,data):
        return np.array([data[2], 0.5 - data[0], 0.5 - data[1]])

    def calculate_face_dir_vector(self,data):
        # 143, 130 : right eye end , 272, 359 : left eye end , 199 : jaw end
        
        right_eye_loc = self.get_loc_cart([data[130].x,data[130].y,data[130].z])
        left_eye_loc = self.get_loc_cart([data[359].x,data[359].y,data[359].z])
        mouth_loc = self.get_loc_cart([data[199].x,data[199].y,data[199].z])
        # vector_a = np.array([data[199].x,data[199].y,data[199].z]) - np.array([data[130].x,data[130].y,data[130].z])                          
        # vector_b = np.array([data[359].x,data[359].y,data[359].z]) - np.array([data[199].x,data[199].y,data[199].z])
        vector_a = mouth_loc - right_eye_loc
        vector_b = left_eye_loc - mouth_loc

        result = np.cross(vector_a,vector_b) 
        # if(self.mode == "dev"):
        #     print("168 : ",[data[168].x,data[168].y,data[168].z])
        #     print("130 : ",[data[130].x,data[130].y,data[130].z]," 359: ",[data[359].x,data[359].y,data[359].z]," 199 : ",[data[199].x,data[199].y,data[199].z])
        #     print("vector a : ",vector_a," vector b : ",vector_b)
        #     print("origin result vector : ",result)
            
        return result / np.linalg.norm(result)
    
    def get_loc_polar(self,data):
        temp = self.get_loc_cart(data)
        # cm / let distance is 50
        # print(temp)
        return np.array([70,1.5708 - np.arctan(temp[2] / 1.25), np.arctan(temp[1] / 1.166666667) ])
    

    def get_face_loc(self,data):
        return np.array([data[168].x,data[168].y,data[168].z])
        # return np.array([(data[143].x+data[199].x+data[272].x)/3,(data[143].y+data[199].y+data[272].y)/3,(data[143].z+data[199].z+data[272].z)/3])
    
    def check_eye(self,data):
        eye_right = np.array([data[159].x,data[159].y,data[159].z]) - np.array([data[145].x,data[145].y,data[145].z])                          
        eye_left = np.array([data[386].x,data[386].y,data[386].z]) - np.array([data[374].x,data[374].y,data[374].z])
        return [np.linalg.norm(eye_left, 2),np.linalg.norm(eye_right, 2)]
 
    #         7,8,9
    #         4,5,6       no face : -1
    #         1,2,3
    def current_face_dir_state(self):
        if(self.dir_vector[0] == 0 and self.dir_vector[1] == 0 and self.dir_vector[2] == 0):
            self.dir_state = -1
            return
        self.dir_state = 5
        if(self.dir_vector[1] < self.params[0]):
            self.dir_state += 3
        elif(self.dir_vector[1] > self.params[1]):
            self.dir_state -= 3
        
        if(self.dir_vector[0] < self.params[2]):
            self.dir_state += 1
        elif(self.dir_vector[0] > self.params[3]):
            self.dir_state -= 1
    
    def current_face_dir_to_text(self):
        res = ""
        if(self.dir_state == -1):
            return "no face"
        if(self.dir_state == 5):
            return "front"
        
        if(self.dir_state % 3 == 0):
            res += "right "
        elif(self.dir_state % 3 == 1):
            res += "left "
            
        if(self.dir_state > 6):
            res += "up "
        elif(self.dir_state < 4):
            res += "down "
        
        
        return res
    
    def current_eye_to_text(self):
        res = ""
        if(self.eye[0] < self.params[4]):
            res += "cl "
        else:
            res += "op "
        
        if(self.eye[1] < self.params[5]):
            res += "cl "
        else:
            res += "op "
        return res
        
    def get_mp_face_width(self):
        obj_width = -1
        # img = cv2.resize(self.image,(640,480))
        img = self.image
        results = self.mp_face.process(img)
        
        if results.detections:
            for detection in results.detections:
                bounding_box = detection.location_data.relative_bounding_box
                x, y, w, h = int(bounding_box.xmin*self.frame_width), int(bounding_box.ymin*self.frame_height), int(bounding_box.width*self.frame_width),int(bounding_box.height*self.frame_height)
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                obj_width=w
        self.mp_face_width = obj_width
        return
    
    def get_focal_length(self):
        self.focal_length = (self.mp_face_width * self.base_distance) / self.base_width
    
    def calculate_distance(self):
        self.distance = (self.base_width * self.focal_length)/self.mp_face_width
             

    def run(self):
        # while self.cap.isOpened():
            self.camera_update()
            # if not stat_q.empty():
            #     stat = stat_q.get()
            #     if stat == "stop":
            #         self.release()

            if not self.success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                return
            
            self.get_face_mesh_data()
            self.get_mp_face_width()
            self.draw_face_mesh_data()

            # if(self.OS == "Windows"):
            #     os.system('cls')
            # else:
            #     os.system('clear')
            if self.results.multi_face_landmarks:
                self.data.set_isface(True)
                data = self.get_data()
                self.data.set_camface_dir_cart(self.calculate_face_dir_vector(data))
                self.data.set_camface_loc_polar(self.get_loc_polar(self.get_face_loc(data)))
                # self.dir_vector = self.calculate_face_dir_vector(data)
                # self.face_loc = self.get_loc_polar(self.get_face_loc(data))
            else:
                self.data.set_isface(False)
            # imgencode = cv2.imencode('.jpg', self.image)[1]
            # stringData = base64.b64encode(imgencode).decode('utf-8')
            # b64_src = 'data:image/jpg;base64,'
            # stringData = b64_src + stringData
            # self.data.set_image(stringData)
            
            #     img_q.put({"stat" : True, "image" : self.image})
            #     data_q.put({"dir_vector":self.dir_vector, "face_loc":self.face_loc})
            # else:
            #     img_q.put({"stat" : False, "image" : self.image})
            
            

#             if(self.mode != "build"):
# #                 print("direction : ",self.dir_state," ",self.current_face_dir_to_text())
#                 print(self.current_face_dir_to_text())
#                 print("dir vector "+str(self.dir_vector)+" ")
#                 print("eye  "+self.current_eye_to_text()+str(self.eye))
#                 print("face loc   "+str(self.face_loc))
                
                
            # self.loop+=1
            # if cv2.waitKey(5) & 0xFF == 27:
            #     break
        
        