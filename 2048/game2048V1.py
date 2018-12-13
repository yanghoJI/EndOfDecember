import numpy as np
import random
import cv2


class game_2048:
    def __init__(self, dim=4):
        self.dim = dim
        self.statinit = np.zeros((dim,dim), dtype=int)
        self.stat = np.zeros((dim, dim), dtype=int)
        self.score = 0
        self.stat = self.casttwo(self.stat, 2)
        print(self.stat)

        ## set display
        self.h = 700
        self.w = 500
        if self.dim == 3:
            self.BG = cv2.imread('./images/3by3.png')
        elif self.dim == 4:
            self.BG = cv2.imread('./images/4by4.png')
        self.BG = cv2.resize(self.BG, (500, 500))
        self.disp = 0
        self.setdisp()
        self.dispArr()

        '''
        self.push_left()
        print(self.stat)
        tempstat = self.rot(self.stat, direc='r')
        print(tempstat)
        tempstat = self.unrot(tempstat, direc='r')
        print(tempstat)

        tempstat = self.rot(self.stat, direc='u')
        print(tempstat)
        tempstat = self.unrot(tempstat, direc='u')
        print(tempstat)

        tempstat = self.rot(self.stat, direc='d')
        print(tempstat)
        tempstat = self.unrot(tempstat, direc='d')
        print(tempstat)
        '''


    def setdisp(self):

        disp = np.zeros((self.h, self.w, 3), dtype='uint8')
        disp[:,:,:] = 234
        disp[200:, :] = self.BG
        self.disp = disp

    def puttext(self, text, LB, size = 1.3):
        #cv2.putText(self.disp, text, LB, cv2.FONT_HERSHEY_SIMPLEX, size, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.disp, text, LB, cv2.FONT_HERSHEY_COMPLEX_SMALL, size, (0, 0, 0), 2, 100)


    def dispArr(self):
        self.puttext('Score : {}'.format(self.score), (20, 60))
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
                self.puttext(val, LB, fontsize)


    def casttwo(self, stat, num):
        zeroidxX, zeroidxY= np.where(stat == 0)
        samidx = random.sample(range(len(zeroidxX)), num)
        stat[zeroidxX[samidx], zeroidxY[samidx]] = 2
        return stat


    def push_left(self, stat):
        tempstat = np.copy(self.statinit)
        for row in range(self.dim):
            nonzeroidxcol = np.where(stat[row, :] != 0)
            temp = stat[row, :][nonzeroidxcol]
            if len(temp) > 0:
                tempstat[row, :len(temp)] = temp

        #stat = tempstat
        return tempstat


    def rot(self,stat, direc):
        if direc == 'r':
            return np.fliplr(stat)

        elif direc == 'u':
            return np.transpose(stat)

        elif direc == 'd':
            return np.transpose(np.flipud(stat))

        else:
            print('error')
            return 0


    def unrot(self,stat, direc):
        if direc == 'r':
            return np.fliplr(stat)

        elif direc == 'u':
            return np.transpose(stat)

        elif direc == 'd':
            return np.flipud(np.transpose(stat))

        else:
            print('error')
            return 0


    def calib(self, stat):
        P = stat[:, 0]
        result = np.copy(self.statinit)
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
        tscore = 0
        temparr, score = self.calib(stat)
        tscore += score
        for a in ('r','u','d'):
            temparr = self.rot(stat, a)
            temparr, score = self.calib(temparr)
            tscore += score

        if tscore == 0:
            return 1
        else:
            return 0


    def step(self, action):
        if action != 'l':
            temparr = self.rot(self.stat, action)
        else:
            temparr = np.copy(self.stat)

        temparr, score = self.calib(temparr)
        temparr = self.push_left(temparr)

        if len(np.where(temparr == 0)[0]) != 0:
            temparr = self.casttwo(temparr, 1)

        self.score += score
        if action != 'l':
            temparr = self.unrot(temparr, action)

        self.stat = temparr


        S = self.stat
        R = score
        D = 0
        if len(np.where(self.stat == 0)[0]) == 0:
            flag = self.cheakDone(self.stat)
            D = flag

        return (S, R, D)

    def run(self):
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
            else:
                print('key error')
            S, R, D = game.step(actkey)
            self.setdisp()
            self.dispArr()
            cv2.imshow('2048', game.disp)
            if D == 1:
                self.puttext('Game over !!', (int(self.w * 0.1), int(self.h * 0.5)), 2.5)
                print('game over\t Score : {}'.format(game.score))
                cv2.imshow('2048', game.disp)
                actkey = cv2.waitKey(-1)
                break

if __name__ == "__main__":
    while 1:
        game = game_2048(3)
        game.run()

