import cv2
import mediapipe as mp

import numpy as np
import os
import platform
import base64

class FaceCamera:
    def __init__(self, index):
        self.cap = None
        self.isOpen = self.setIndex(index)
        
    
    def setIndex(self,index):
        self.cap = cv2.VideoCapture(index)
        self.isOpen = self.cap.isOpened()
        return

    def camera_update(self):
        if self.isOpen:
            self.success, self.image = self.cap.read()
            return self.image
        else:
            return None