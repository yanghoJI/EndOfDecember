import cv2
import numpy as np

class hello:
        def haha(self):
                self.s_img = cv2.imread("plane.png", cv2.IMREAD_GRAYSCALE)
                self.l_img = np.zeros((512,1024))
                self.l_img[:,:] = 255 
                self.x_offset=120
                self.y_offset=120
        #        print(y_offset,y_offset+s_img.shape[0])
                self.l_img[self.y_offset:self.y_offset+self.s_img.shape[0], self.x_offset:self.x_offset+self.s_img.shape[1]] = self.s_img
                self.s_img = cv2.imread("bat.png", cv2.IMREAD_GRAYSCALE)
                self.x_offset=200
                self.y_offset=300
                self.l_img[self.y_offset:self.y_offset+self.s_img.shape[0], self.x_offset:self.x_offset+self.s_img.shape[1]] = self.s_img

                self.s_img = cv2.imread("bullet.png", cv2.IMREAD_GRAYSCALE)
                self.x_offset=50
                self.y_offset=50
                self.l_img[self.y_offset:self.y_offset+self.s_img.shape[0], self.x_offset:self.x_offset+self.s_img.shape[1]] = self.s_img


                cv2.imshow('dddd',self.l_img)
                cv2.waitKey(0)


if __name__=='__main__':
    env=hello()
    env.haha()


