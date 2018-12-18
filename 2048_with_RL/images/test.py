import cv2
import numpy as np
s_img = cv2.imread("plane.png", cv2.IMREAD_GRAYSCALE)

pad_width = 1024
pad_height = 512
#s_img = cv2.imread("plane.png")
#l_img = cv2.imread("background.jpg")
l_img = np.zeros((512,1024))
l_img[:,:] = 255 

x_offset=0
y_offset=0
print(y_offset,y_offset+s_img.shape[0])
l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
#l_img[10:100, 10:100] = 0
cv2.imshow('dddd',l_img)
cv2.waitKey(0)

