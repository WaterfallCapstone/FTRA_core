import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
import numpy as np
import os
import platform
import base64

class FaceCamera:
    def __init__(self, index):
        self.cap = None
        self.isOpen = False
        self.setIndex(index)
        self.image = None
        self.meshimg = None
        self.results = None
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)   
        self.meshdata = None
        print(self.isOpen)
    
    def setIndex(self,index):
        self.cap = cv2.VideoCapture(index)
        self.isOpen = self.cap.isOpened()
        return self.isOpen

    def camera_update(self):
        if self.isOpen:
            self.success, self.image = self.cap.read()
            return self.image
        else:
            return None
    
    def get_face_mesh_data(self):
        # self.image.flags.writeable = False
        if self.image is not None:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.results = self.face_mesh.process(self.image)
            if self.results.multi_face_landmarks:
                for face_landmarks in self.results.multi_face_landmarks:
                    result = face_landmarks.landmark
                    self.meshdata = result
                return result
        return None
    
    def draw_face_mesh_data(self):
        if self.image is not None:
            self.image.flags.writeable = True
            self.meshimg = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
            if self.results is not None and self.results.multi_face_landmarks:
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
        return self.meshimg