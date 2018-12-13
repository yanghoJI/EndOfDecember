import artint1991_v1
import cv2
import numpy as np


if __name__=='__main__':
    env=artint1991_v1.sky_1991()
    #env.initGame()
    #env.R_getframe()
    observe = env.reset()
    while(1):
        cv2.imshow('1991', observe)
        action = cv2.waitKey(3)
        if action == 119:
            action = 1
        elif action == 115:
            action = 2
        elif action == -1:
            action = 5
        else:
            action = 3

        #action = int(input('inset antion : '))
        observe, reward, done, info = env.step(action)
        #cv2.imshow('1991', image)
        cv2.waitKey(1)
    #cv2.imshow('1991', image)
    cv2.waitKey(0)