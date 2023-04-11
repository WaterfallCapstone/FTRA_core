import numpy as np

class FaceLocation4:
    def __init__(self,data):
        self.data = data
        self.camface_loc_cart = np.array([0.0,0.0,0.0,0.0])
        self.camface_dir_cart = np.array([0.0,0.0,0.0,0.0])

        self.face_rot = np.array([0.0,0.0,0.0,0.0])
        self.face_dir_rot = np.array([0.0,0.0,0.0,0.0])

        self.face_trans = np.array([0.0,0.0,0.0,0.0])
        self.face_dir_trans = np.array([0.0,0.0,0.0,0.0])
        
    def cal_face_loc(self):
        camface_loc_polar = self.data.get_camface_loc_polar()
        # camface_dir_cart = self.data.get_camface_dir_cart()
        # camface_dir_cart.append(0.0)
        cam_loc_cart = self.data.get_cam_loc_cart()
        cam_loc_cart = np.append(cam_loc_cart,0.0)
        cam_dir_polar = self.data.get_cam_dir_polar()
    

        r = camface_loc_polar[0]
        phi = camface_loc_polar[1]
        theta = camface_loc_polar[2]
        self.camface_loc_cart[0] = r * np.sin(theta) * np.cos(phi)
        self.camface_loc_cart[1] = r * np.sin(theta) * np.sin(phi)
        self.camface_loc_cart[2] = r * np.cos(theta)

        # self.camface_dir_cart = self.camface_loc_cart + camface_dir_cart
        
        roll = cam_dir_polar[1]
        pitch = np.pi/2 - cam_dir_polar[2]
        roll_matrix = np.array(
            [
                [np.cos(roll), -np.sin(roll), 0, 0],
                [np.sin(roll), np.cos(roll), 0, 0],
                [0,0,1,0],
                [0,0,0,1]
            ]
        )
        pitch_matrix = np.array(
            [
                [1,0,0,0],
                [0,np.cos(pitch),-np.sin(pitch),0],
                [0,np.sin(pitch),np.cos(pitch),0],
                [0,0,0,1]
            ]
        )
        self.face_rot = roll_matrix @ (pitch_matrix @ self.camface_loc_cart)
        self.face_dir_rot = roll_matrix @ (pitch_matrix @ self.camface_dir_cart)


        self.face_trans = self.face_rot + cam_loc_cart
        self.face_dir_trans = self.face_dir_rot + cam_loc_cart

        return self.face_trans[:3], self.face_dir_trans[:3]






class FaceLocation5:
    def __init__(self,data):
        self.data = data
        self.camface_loc_cart = np.array([0.0,0.0,0.0,0.0])
        self.camface_dir_cart = np.array([0.0,0.0,20.0,0.0])

        self.face_rot = np.array([0.0,0.0,0.0,0.0])
        self.face_dir_rot = np.array([0.0,0.0,0.0,0.0])
        
class FaceLocation6:
    def __init__(self,data):
        self.data = data
        self.camface_loc_cart = np.array([0.0,0.0,0.0,0.0])
        self.camface_dir_cart = np.array([0.0,0.0,0.0,0.0])

        self.face_rot = np.array([0.0,0.0,0.0,0.0])
        self.face_dir_rot = np.array([0.0,0.0,0.0,0.0])

        self.face_trans = np.array([0.0,0.0,0.0,0.0])
        self.face_dir_trans = np.array([0.0,0.0,0.0,0.0])
        
    def cal_face_loc(self):
        camface_loc_polar = self.data.get_camface_loc_polar()
        # camface_dir_cart = self.data.get_camface_dir_cart()
        # camface_dir_cart.append(0.0)
        cam_loc_cart = self.data.get_cam_loc_cart()
        cam_loc_cart = np.append(cam_loc_cart,0.0)
        cam_dir_polar = self.data.get_cam_dir_polar()
    

        r = camface_loc_polar[0]
        phi = camface_loc_polar[1]
        theta = camface_loc_polar[2]
        self.camface_loc_cart[0] = r * np.sin(theta) * np.cos(phi)
        self.camface_loc_cart[1] = r * np.sin(theta) * np.sin(phi)
        self.camface_loc_cart[2] = r * np.cos(theta)

        # self.camface_dir_cart = self.camface_loc_cart + camface_dir_cart
        
        roll = cam_dir_polar[1]
        pitch = np.pi/2 - cam_dir_polar[2]
        roll_matrix = np.array(
            [
                [np.cos(roll), -np.sin(roll), 0, 0],
                [np.sin(roll), np.cos(roll), 0, 0],
                [0,0,1,0],
                [0,0,0,1]
            ]
        )
        pitch_matrix = np.array(
            [
                [1,0,0,0],
                [0,np.cos(pitch),-np.sin(pitch),0],
                [0,np.sin(pitch),np.cos(pitch),0],
                [0,0,0,1]
            ]
        )
        self.face_rot = roll_matrix @ (pitch_matrix @ self.camface_loc_cart)
        self.face_dir_rot = roll_matrix @ (pitch_matrix @ self.camface_dir_cart)


        self.face_trans = self.face_rot + cam_loc_cart
        self.face_dir_trans = self.face_dir_rot + cam_loc_cart

        return self.face_trans[:3], self.face_dir_trans[:3]