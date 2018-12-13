import numpy as np
import random

class game_2048:
    def __init__(self, dim=4):
        self.dim = dim
        self.statinit = np.zeros((dim,dim), dtype=int)
        self.stat = np.zeros((dim, dim), dtype=int)
        self.score = 0
        self.stat = self.casttwo(self.stat, 2)
        print(self.stat)


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

if __name__ == "__main__":
    game = game_2048(2)

    while 1:
        action = input()
        S, R, D = game.step(action)
        print(S)
        print('R : {}\t score: {}'.format(R, game.score))
        if D == 1:
            print('game over\t Score : {}'.format(game.score))
            break


    #testarr = np.array([[2,0,2,0], [4,2,2,0], [2,2,2,2], [4,2,0,2]])

    #result, score = game.calib(testarr)
    #print(result, score)
    #print(game.stat)
