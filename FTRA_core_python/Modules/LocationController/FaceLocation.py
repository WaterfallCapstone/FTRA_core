import numpy as np
import math

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
        
        # 
        cam_loc_cart = self.data.get_cam_loc_cart()
        cam_loc_cart = np.append(cam_loc_cart,0.0)
        cam_dir_polar = self.data.get_cam_dir_polar()
        

        r = camface_loc_polar[0]
        theta = camface_loc_polar[1]
        phi = camface_loc_polar[2]
        self.camface_loc_cart[0] = r * np.sin(theta) * np.cos(phi)
        self.camface_loc_cart[1] = r * np.sin(theta) * np.sin(phi)
        self.camface_loc_cart[2] = r * np.cos(theta)
        
        camface_dir_cart = self.data.get_camface_dir_cart() * self.data.get_destination_distance()
        camface_dir_cart =np.append(camface_dir_cart,0.0)
        

        camface_dir_cart = self.camface_loc_cart + camface_dir_cart
        
        roll = cam_dir_polar[2]
        pitch = np.pi/2 - cam_dir_polar[1]
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
        self.face_dir_rot = roll_matrix @ (pitch_matrix @ camface_dir_cart)


        self.face_trans = self.face_rot + cam_loc_cart
        self.face_dir_trans = self.face_dir_rot + cam_loc_cart

        return self.face_trans[:3], self.face_dir_trans[:3]

    def calculate_sphere_point_of_contact(self,face, target, r, height):

        x1 = face[0]
        y1 = face[1]
        z1 = face[2] - height

        x2 = target[0]
        y2 = target[1]
        z2 = target[2] - height
        

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        

        a = dx**2 + dy**2 + dz**2
        b = 2 * (dx * x1 + dy * y1 + dz * z1)
        c = x1**2 + y1**2 + z1**2 - r**2
        

        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            return (0,0,0)

        t1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t2 = (-b - math.sqrt(discriminant)) / (2 * a)
        
        t = min(t1, t2)
        
        x = x1 + t * dx
        y = y1 + t * dy
        z = z1 + t * dz
        
        return (x, y, z)

    def calculate_normal_sphere_intersection(self,face, target, height):
        x1 = face[0]
        y1 = face[1]
        z1 = face[2] - height

        x2 = target[0]
        y2 = target[1]
        z2 = target[2] - height

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        

        dot_product = dx * x1 + dy * y1 + dz * z1
        
        direction_length = math.sqrt(dx**2 + dy**2 + dz**2)

        t = dot_product / direction_length**2
        
        x = t * dx
        y = t * dy
        z = t * dz
        
        return (x, y, z)


    def destination(self,face, target, range, height):
        length = math.sqrt(target[0] ** 2 + target[1] ** 2 + (target[2] - height) ** 2)
        if(target[1] >= 0 and target[2] >= 0):# y > 0 && z > 0 이어야 함
            if(length <= range):#범위안에 있으면
                return target
            else:
                result = np.array([target[0], target[1], target[2] - height])
                result = result * (range/length)
                return result
        else:
            tmp = self.calculate_sphere_point_of_contact(face,target, range,height)
            if(tmp[1] > 0 and tmp[2] > 0):
                result = np.array(tmp)
                return result
            else:
                tmp = self.calculate_normal_sphere_intersection(face,target,height)
                tmp1 = np.array(tmp)
                result = tmp1 * (math.sqrt((tmp[0] ** 2 + tmp[1] ** 2 + (tmp[2] - height) ** 2)) / length)
                return result
    
    def calc_dest_arm(self, dest):
        result =np.array([0.0,0.0,0.0,0.0,0.0,0.0])
        face_loc_cart = self.data.get_face_loc_cart()
        arm_length = self.data.get_arm_length()
        lookat_cart = face_loc_cart - dest
        
        roll = np.arctan(dest[1] / dest[0])
        if roll < 0:
            result[0] = np.pi + roll
        roll_matrix = np.array(
            [
                [np.cos(-roll), -np.sin(-roll), 0, 0],
                [np.sin(-roll), np.cos(-roll), 0, 0],
                [0,0,1,0],
                [0,0,0,1]
            ]
        )
        
        lookat_xbase = roll_matrix @ np.append(lookat_cart,0.0)
        
        result[0] = roll
        
        
        
        a_len = arm_length[1]
        b_len = arm_length[2]
        c_len = np.sqrt(np.square(dest[0])+np.square(dest[1])+np.square(dest[2]))
        
        
        angle_ac = np.arccos((np.square(a_len)+np.square(c_len)-np.square(b_len)) / (2 * a_len * c_len))
        
        angle_dest = np.arccos(np.sqrt( np.square(dest[0]) + np.square(dest[1]) ) / c_len)
        # print(c_len / np.sqrt( np.square(dest[0]) + np.square(dest[1]) ))
        # print(angle_dest)
        result[1] = np.pi - angle_ac - angle_dest
        
        angle_ab = np.arccos((np.square(a_len)+np.square(b_len)-np.square(c_len)) / (2 * a_len * b_len))
        
        result[2] = (3/2) * np.pi - self.data.get_motor_offset_angle() - angle_ab
        
        result[3] = np.pi/2 + angle_ab - result[1]
        
        result[4] = np.pi/2 + np.arctan(lookat_xbase[1] / lookat_xbase[0])
        
        look_len = np.sqrt(np.square(lookat_xbase[0])+np.square(lookat_xbase[1])+np.square(lookat_xbase[2]))
        
        result[5] = np.pi - np.arccos(lookat_xbase[2]/look_len)
        # print(result)
        
        return result
        
        
        