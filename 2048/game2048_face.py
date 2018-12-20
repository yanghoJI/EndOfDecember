import cv2
#import sys
import numpy as np
from game2048V1 import Game2048
import time

env = Game2048(4)
cv2.imshow('2048', env.disp)

cascPath = 'face.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

cnt = 0
avg = 5
buf = [None] * avg
prestat = None
while True:

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    frame = frame[:, frame.shape[1] // 10: -(frame.shape[1] // 10), :]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=1,
        minSize=(200, 200),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    black = np.zeros(gray.shape)
    if len(faces) == 1:
        cnt += 1
        (x, y, w, h) = faces[0]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #print(x, y, x + w, y + h)
        black[y:y+h, x:x+w] = 255
        #cv2.imshow('ddd', black)
        # center
        cv2.rectangle(frame, (400, 244), (600, 470), (255, 0, 0), 2)
        centerV = len(np.nonzero(black[244:470, 400:600])[0])
        # Right
        cv2.rectangle(frame, (139, 214), (339, 530), (0, 0, 255), 2)
        rightV = len(np.nonzero(black[214:530, 139:339])[0])
        # Left
        cv2.rectangle(frame, (650, 214), (850, 530), (0, 0, 255), 2)
        leftV = len(np.nonzero(black[214:530, 650:850])[0])
        # down
        cv2.rectangle(frame, (339, 530), (650, 730), (255, 0, 255), 2)
        downV = len(np.nonzero(black[530:730, 339:650])[0])
        # up
        cv2.rectangle(frame, (339, 14), (650, 214), (0, 255, 255), 2)
        upV = len(np.nonzero(black[14:214, 339:650])[0])

        templist = [rightV, leftV, upV, downV]
        maxidx = templist.index(max(templist))
        maxv = templist[maxidx]
        if maxidx == 0:
            maxori = 'r'
            maxv -= 3000
        elif maxidx == 1:
            maxori = 'l'
            maxv -= 3000
        elif maxidx == 2:
            maxori = 'u'
        elif maxidx == 3:
            maxori = 'd'
        else:
            print('error')
        #print('c:{}\tori:{}\t{}'.format(centerV, maxori, maxv))

        if maxv > 21000 and centerV < 45000:
            #print('action : {}'.format(maxori))
            action = maxori
        else:
            #print('actions : center')
            action = None

        buf[cnt%avg] = action
        templist = [buf.count('r'), buf.count('l'), buf.count('u'), buf.count('d'), buf.count(None)]
        maxidx = templist.index(max(templist))
        if maxidx == 0:
            maxori = 'r'
        elif maxidx == 1:
            maxori = 'l'
        elif maxidx == 2:
            maxori = 'u'
        elif maxidx == 3:
            maxori = 'd'
        else:
            maxori = None


        if maxori != None and maxori != prestat:
            prestat = maxori
            actkey = maxori
            print('real actions : {}'.format(maxori))
            S, R, D = env.step(actkey)
            if env.dispmode:
                env.setDispInit()
                env.setDispArray()
                tempdisp = np.copy(env.disp)
                tempdisp[np.nonzero(env.edgedisp)] = env.edgedisp[np.nonzero(env.edgedisp)]
                cv2.imshow('2048', tempdisp)
                #time.sleep(1)
                cv2.waitKey(250)
                cv2.imshow('2048', env.disp)
            else:
                print(env.stat)
            if D == 1:
                env.putText('Game over !!', (int(env.w * 0.15), int(env.h * 0.5)), 2.5)
                print('game over\t Score : {}'.format(env.score))
                cv2.imshow('2048', env.disp)
                cv2.waitKey(-1)
                time.sleep(3)
                break

        elif maxori == None and maxori != prestat:
            prestat = maxori
            print('real actions : {}'.format(maxori))
        frame = np.fliplr(frame)
        cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()