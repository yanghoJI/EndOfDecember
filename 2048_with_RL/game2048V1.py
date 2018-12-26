import numpy as np
import random
import cv2
import time

class Game2048:
    def __init__(self, dim=4):
        self.dim = dim
        self.stat_init = np.zeros((dim,dim), dtype=int)
        self.stat = np.zeros((dim, dim), dtype=int)
        self.score = 0
        self.stat = self.fillNumber(self.stat, 2)
        self.dispstat = np.zeros((dim, dim), dtype=int)
        #print(self.stat)

        ## set display
        self.h = 700
        self.w = 500
        self.edge = cv2.imread('./images/edge6.png')
        if self.dim == 3:
            self.BG = cv2.imread('./images/3by3.png')
            self.edge = cv2.resize(self.edge, (self.w // self.dim, self.w // self.dim))
            self.dispmode = True

        elif self.dim == 4:
            self.BG = cv2.imread('./images/4by4.png')
            self.edge = cv2.resize(self.edge, (self.w // self.dim, self.w // self.dim))
            self.dispmode = True
        else:
            self.BG = cv2.imread('./images/4by4.png')
            self.dispmode = False

        self.WSAD = cv2.imread('./images/wsad.png')
        self.WSAD = self.WSAD[:260, :]
        self.WSAD = cv2.resize(self.WSAD, (200, 130))
        self.BG = cv2.resize(self.BG, (self.w, self.w))
        self.disp = 0

        self.setDispInit()
        if self.dispmode:
            self.setDispArray()



    def setDispInit(self):
        # initialize display
        disp = np.zeros((self.h, self.w, 3), dtype='uint8')
        disp[:,:,:] = 234
        disp[200:, :] = self.BG
        disp[50:180, 280:-20, :] += self.WSAD
        self.disp = disp
        self.putText('Newgame: Q', (20, 90))


    def putText(self, text, LB, size = 1.3):
        # write text on display
        cv2.putText(self.disp, text, LB, cv2.FONT_HERSHEY_COMPLEX_SMALL, size, (0, 0, 0), 2, 100)


    def setDispArray(self):
        # write state-array on display
        self.edgedisp = np.zeros((self.h, self.w, 3), dtype='uint8')
        self.putText('Score : {}'.format(self.score), (20, 60))
        if self.dim == 3:
            fontinter = 20
            fontsize = 3
        elif self.dim == 4:
            fontinter = int(20 * 0.666)
            fontsize = 2
        interval = self.w // self.dim
        inix = int(interval * 0.5)
        iniy = int(interval * 0.6 + 200)

        for row in range(self.dim):
            for col in range(self.dim):
                val = str(self.stat[row, col])
                if val == '0':
                    continue
                LB = (int(inix + interval * col - len(val) * fontinter), int(iniy + interval * row))
                self.putText(val, LB, fontsize)

                if self.stat[row, col] != self.dispstat[row, col]:
                    rowst = int(interval*row + 200)
                    colst = int(interval*col)
                    self.edgedisp[rowst:rowst+self.edge.shape[0], colst:colst+self.edge.shape[0]] = self.edge
        self.dispstat = np.copy(self.stat)


    def fillNumber(self, stat, num):
        # fill empty space with number
        zeroidxX, zeroidxY= np.where(stat == 0)
        samidx = random.sample(range(len(zeroidxX)), num)
        samplelist = [2,2,2,2,4]
        num = random.sample(samplelist, 1)
        stat[zeroidxX[samidx], zeroidxY[samidx]] = num
        return stat


    def pushLeft(self, stat):
        # push number against left-side
        tempstat = np.copy(self.stat_init)
        for row in range(self.dim):
            nonzeroidxcol = np.where(stat[row, :] != 0)
            temp = stat[row, :][nonzeroidxcol]
            if len(temp) > 0:
                tempstat[row, :len(temp)] = temp

        return tempstat


    def rotArray(self,stat, direc):
        # rotate array
        if direc == 'r':
            return np.fliplr(stat)

        elif direc == 'u':
            return np.transpose(stat)

        elif direc == 'd':
            return np.transpose(np.flipud(stat))

        else:
            print('error')
            return 0


    def unrotArray(self,stat, direc):
        # undo rotation
        if direc == 'r':
            return np.fliplr(stat)

        elif direc == 'u':
            return np.transpose(stat)

        elif direc == 'd':
            return np.flipud(np.transpose(stat))

        else:
            print('error')
            return 0


    def calculNextArray(self, stat):
        # calculate next array
        P = stat[:, 0]
        result = np.copy(self.stat_init)
        score = 0
        for col in range(1, self.dim):
            tempP = np.zeros(P.shape)
            for row in range(self.dim):
                pa = P[row]
                da = stat[row, col]

                if pa == da:
                    result[row, col-1] = pa + pa
                    score += pa + pa
                    tempP[row] = 0

                elif pa == 0 or da == 0:
                    result[row, col-1] = 0
                    tempP[row] = pa + da

                else:
                    result[row, col-1] = pa
                    tempP[row] = da

            P = tempP
        result[:, -1] = P

        return (result, score)


    def cheakDone(self, stat):
        # cheak Done condition
        tscore = 0
        temparr, score = self.calculNextArray(stat)
        tscore += score
        for a in ('r','u','d'):
            temparr = self.rotArray(stat, a)
            temparr, score = self.calculNextArray(temparr)
            tscore += score

        if tscore == 0:
            return 1
        else:
            return 0


    def step(self, action):
        # do one step and return state, reward, done for RL
        if action == None:
            S = self.stat
            R = 0
            D = 0
            return (S, R, D)
        elif action == 'l':
            temparr = np.copy(self.stat)
        else:
            temparr = self.rotArray(self.stat, action)

        temparr, score = self.calculNextArray(temparr)
        temparr = self.pushLeft(temparr)

        self.score += score
        if action != 'l':
            temparr = self.unrotArray(temparr, action)

        poolact = False
        if (len(np.where(temparr == 0)[0]) != 0) and (not np.array_equal(temparr, self.stat)):
            temparr = self.fillNumber(temparr, 1)
        elif np.array_equal(temparr, self.stat):
            poolact = True



        self.stat = temparr

        S = self.stat
        R = score if not poolact else -10
        D = 0
        if len(np.where(self.stat == 0)[0]) == 0:
            flag = self.cheakDone(self.stat)
            D = flag

        return (S, R, D)


    def run(self):
        # play game
        cv2.imshow('2048', game.disp)
        while 1:
            actkey = cv2.waitKey(-1)
            if actkey == 119:
                actkey = 'u'
            elif actkey == 115:
                actkey = 'd'
            elif actkey == 97:
                actkey = 'l'
            elif actkey == 100:
                actkey = 'r'
            elif actkey == 113:
                break
            else:
                actkey = None
                print('key error')
            S, R, D = game.step(actkey)
            if self.dispmode:
                self.setDispInit()
                self.setDispArray()
                tempdisp = np.copy(self.disp)
                tempdisp[np.nonzero(self.edgedisp)] = self.edgedisp[np.nonzero(self.edgedisp)]
                cv2.imshow('2048', tempdisp)
                #time.sleep(1)
                cv2.waitKey(250)
                cv2.imshow('2048', self.disp)
            else:
                print(self.stat)
            if D == 1:
                self.putText('Game over !!', (int(self.w * 0.15), int(self.h * 0.5)), 2.5)
                print('game over\t Score : {}'.format(self.score))
                cv2.imshow('2048', self.disp)
                cv2.waitKey(-1)
                time.sleep(3)

                break


if __name__ == "__main__":
    while 1:
        # set size of grid 3 or 4
        game = Game2048(4)
        game.run()

