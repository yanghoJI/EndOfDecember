import pygame
import random
from time import sleep

class sky_1991:
    def __init__(self,):

        self.WHITE = (255,255,255)
        self.RED = (255,0,0)
        self.pad_width = 1024
        self.pad_height = 512

                #background_width = 724

        self.aircraft_width = 90
        self.aircraft_height = 55
        self.bat_width = 110
        self.bat_height = 67

        self.fireball1_width = 140
        self.fireball1_height = 60
        self.fireball2_width = 86
        self.fireball2_height = 60


    def reset(self):
        self.observe=self.drawObject(self.aircraft,self.pad_width*0.05,self.pad_height * 0.8)
#        self.drawObject(self.bat, self.pad_width, random.randrange(0,self.pad_height))
#       self.drawObject(self.fire[1],self.pad_width,random.randrange(0, self.pad_height))
        return self.observe


    def render(self):

        self.drawObject(self.aircraft,self.x,self.y)
        self.drawObject(self.bullet, bx, by)
        self.drawObject(self.bat, self.bat_x, self.bat_y)
        self.drawObject(self.boom, self.bat_x, self.bat_y)
        self.drawObject(self.fire[1],self.fire_x,self.fire_y)
        pygame.display.update()



    def step(self,real_action):
        self.real_action=real_action

        if real_action==1:
            self.y_change =-5

        elif real_action==2:
            self.y_change = 5

        elif real_action==3:
            self.bullet_x = self.x+ self.aircraft_width
            self.bullet_y = self.y +self.aircraft_height/2
            self.bullet_xy.append([self.bullet_x, self.bullet_y])


        self.observe=self.render()
        self.reward=self.reward
        self.done=done
        self.info=1

        return self.observe, self.reward, self.done, self.info








#def drawScore(count):
#    global gamepad

#    font = pygame.font.SysFont(None, 25)
#    text = font.render('Bat Passed: ' + str(count), True, WHITE)
#    gamepad.blit(text, (0,0))

#def gameOver():
#    global gamepad
#    dispMessage('GAME OVER')

    def textObj(self,text,font):
        self.textSurface = font.render(text, True, self.RED)
        return self.textSurface, self.textSurface.get_rect()

    def dispMessage(self,text):
        self.largeText = pygame.font.Font('freesansbold.ttf',115)
        self.TextSurf, self.TextRect =  self.textObj(text,self.largeText)
        self.TextRect.center = ((self.pad_width/2),(self.pad_height/2))
        self.gamepad.blit(self.TextSurf, self.TextRect)
        pygame.display.update()
        sleep(1)
        self.runGame()

    def crash(self):
        self.done=1
        self.dispMessage('Crashed!')

    def drawObject(self,obj,x,y):
        self.gamepad
        self.gamepad.blit(obj,(x,y))

    def runGame(self):
        self.done=0
        self.reward = 0
        self.isShotBat = False
        self.boom_count = 0
        self.bullet_xy = []

        self.x = self.pad_width*0.05
        self.y = self.pad_height * 0.8
        self.y_change = 0

        self.bat_x = self.pad_width
        self.bat_y = random.randrange(0,self.pad_height)

        self.fire_x = self.pad_width
        self.fire_y = random.randrange(0, self.pad_height)
        random.shuffle(self.fires)
        self.fire = self.fires[0]




        self.crashed = False
        while not self.crashed:
            for self.event in pygame.event.get():
#                print(self.event)
                if self.event.type == pygame.QUIT:
                    self.crashed = True

                if self.event.type == pygame.KEYDOWN:
                    if self.event.key == pygame.K_UP:
                        self.y_change =-5
                    elif self.event.key == pygame.K_DOWN:
                        self.y_change = 5

                    elif self.event.key == pygame.K_LCTRL:
                        self.bullet_x = self.x+ self.aircraft_width
                        self.bullet_y = self.y +self.aircraft_height/2
                        self.bullet_xy.append([self.bullet_x, self.bullet_y])

                if self.event.type == pygame.KEYUP:
                    if self.event.key == pygame.K_UP or self.event.key == pygame.K_DOWN:
                        self.y_change =  0


            self.gamepad.fill(self.WHITE)

            self.y += self.y_change
            if self.y<0:
                self.y=0

            elif self.y> self.pad_height - self.aircraft_height:
                self.y = self.pad_height - self.aircraft_height

            self.bat_x -= 7
            if self.bat_x <= 0:
        #            bat_passed +=1
                self.bat_x = self.pad_width
                self.bat_y = random.randrange(0,self.pad_height)

            if self.fire[1] == None:
                self.fire_x -= 30
            else:
                self.fire_x -= 15

            if self.fire_x <=0:
                self.fire_x = self.pad_width
                self.fire_y = random.randrange(0,self.pad_height)
                random.shuffle(self.fires)
                self.fire = self.fires[0]

            if len(self.bullet_xy)!=0:
                for i, bxy in enumerate(self.bullet_xy):
                    bxy[0] +=15
                    self.bullet_xy[i][0] = bxy[0]


                    if bxy[0] > self.bat_x:
                        if bxy[1] > self.bat_y and bxy[1] <self.bat_y + self.bat_height:
                            self.bullet_xy.remove(bxy)
                            self.isShotBat=True

                            self.reward += 100
                            print(self.reward)

                    if bxy[0] >= self.pad_width:
                        try:
                            self.bullet_xy.remove(bxy)
                        except:
                            pass

            if self.x + self.aircraft_width > self.bat_x:
                if(self.y > self.bat_y and self.y < self.bat_y+self.bat_height) or (self.y + self.aircraft_height > self.bat_y and self.y+self.aircraft_height < self.bat_y+self.bat_height):
                    self.reward -=1000
                    print(self.reward)
                    self.crash()

            if self.fire[1]!=None:
                if self.fire[0] == 0:
                    self.fireball_width = self.fireball1_width
                    self.fireball_height = self.fireball1_height
                elif self.fire[0] == 1:
                    self.fireball_width = self.fireball2_width
                    self.fireball_height = self.fireball2_height

                if self.x + self.aircraft_width > self.fire_x:
                    if(self.y>self.fire_y and self.y < self.fire_y+self.fireball_height) or (self.y+self.aircraft_height > self.fire_y and self.y+self.aircraft_height < self.fire_y+self.fireball_height):
                        self.reward -=1000
                        print(self.reward)
                        self.crash()

            self.drawObject(self.aircraft,self.x,self.y)

            if len(self.bullet_xy) !=0:
                for bx, by in self.bullet_xy:
                    self.drawObject(self.bullet, bx, by)

            if not self.isShotBat:
                self.drawObject(self.bat, self.bat_x, self.bat_y)
            else:
                self.drawObject(self.boom, self.bat_x, self.bat_y)
                self.boom_count +=1
                if self.boom_count > 5:
                    self.boom_count = 0
                    self.bat_x = self.pad_width
                    self.bat_y = random.randrange(0,self.pad_height-self.bat_height)
                    self.isShotBat = False

            if self.fire[1]!=None:
                self.drawObject(self.fire[1],self.fire_x,self.fire_y)

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        quit()

    def initGame(self):

        self.fires = []
        pygame.init()
        self.gamepad = pygame.display.set_mode((self.pad_width,self.pad_height))
        pygame.display.set_caption('1991')
        self.aircraft = pygame.image.load('images/plane.png')
        self.background1 = pygame.image.load('images/background.png')
        self.background2 = self.background1.copy()
        self.bat = pygame.image.load('images/bat.png')


        self.fires.append((0,pygame.image.load('images/fireball.png')))
        self.fires.append((1,pygame.image.load('images/fireball2.png')))

        self.boom=pygame.image.load('images/boom.png')

        for i in range(3):
            self.fires.append((i+2,None))

        self.bullet = pygame.image.load('images/bullet.png')

        self.clock = pygame.time.Clock()
#        imshow(self.gamepad)
        self.runGame()


if __name__=='__main__':
    env=sky_1991()
    env.initGame()






































