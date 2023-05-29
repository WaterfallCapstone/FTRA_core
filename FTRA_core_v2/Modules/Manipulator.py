import cv2
from rembg import remove
import numpy as np

class Manipulator:
    def __init__(self):
        return
    
    def get_channel(self,image):
        if len(image.shape) > 2:
            return image.shape[2]
    
    def channel_3to4(self,image):
        if len(image.shape) > 2 and image.shape[2] == 3:
            b_channel, g_channel, r_channel = cv2.split(image)
            alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype)
            image = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
            return image
    
    def channel_4to3(self,image):
        if len(image.shape) > 2 and image.shape[2] == 4:
            image = image[:, :, :3]
            return image
    
    def combine4(self, bg , img, y_offset, x_offset, a_offset = 20):
        image = bg
        h, w = img.shape[:2]
        for i in range(h):
            for j in range(w):
                if img[i][j][3] > a_offset:
                    image[y_offset+i][x_offset+j] = img[i][j]
        return image
        
    
    def remove_bg(self, image, savepath = "", setChroma = False):
        img = remove(image)

        if setChroma:
            bg = cv2.imread("Images/ChromaKey.png", cv2.IMREAD_COLOR) 
            bg = self.channel_3to4(bg)
            bg = self.combine4(bg, img, 0, 0)
            h, w = img.shape[:2]
            img = bg[:h,:w]
            img = self.channel_4to3(img)
            

        if savepath != "":
            cv2.imwrite(savepath, img)

        return img
    
    def combine_chroma(self, chromaimg, destimg, y_offset, x_offset):
        hsv = cv2.cvtColor(chromaimg, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (50, 150, 0), (70, 255, 255))
        mask_inv = cv2.bitwise_not(mask)
        h, w = chromaimg.shape[:2]
        roi = destimg[y_offset:y_offset+h, x_offset : x_offset + w]
        fg = cv2.bitwise_and(chromaimg,chromaimg,mask=mask_inv)
        bg = cv2.bitwise_and(roi, roi, mask=mask)
        destimg[y_offset:y_offset+h, x_offset : x_offset + w] = fg + bg
        return destimg

    
if __name__ == "__main__":
    manipulator = Manipulator()
    lenna = cv2.imread("Images/Lenna.png", cv2.IMREAD_COLOR) 
    
    
    cv2.imshow("Remove background : 4channel png with transparency",manipulator.remove_bg(lenna, "Images/Lenna_rmbg.png"))
    cv2.imshow("Remove background with Chroma Key Option : 3hannel",manipulator.remove_bg(lenna, "", True))


    lenna_nobg = manipulator.remove_bg(lenna, "")
    bg = cv2.imread("Images/windows.jpg", cv2.IMREAD_COLOR) 
    bg = manipulator.channel_3to4(bg)
    newimg = manipulator.combine4(bg, lenna_nobg, 200, 300)
    cv2.imshow("Put 4channel img with Certain Offset" ,newimg)


    lenna_with_chroma = cv2.imread("Images/Lenna_rmbg_chroma.png", cv2.IMREAD_COLOR) 
    back = cv2.imread("Images/windows.jpg", cv2.IMREAD_COLOR) 
    newimgwithchroma = manipulator.combine_chroma(lenna_with_chroma, back, 500, 700)
    cv2.imshow("Put 3channel chroma img with certain offset",newimgwithchroma)

    cv2.waitKey(0)
