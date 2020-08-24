import pygame
import random


##  Değişkenler
WIDTH = 1200
HEIGHT = 600
BORDER = 10
#  hız
VELOCITY = 1
#  framerate ,(döngü hızı) işletim sistemine göre farklılık gösterebiliyor
FRAMERATE = 310 # linux

##  Sınıfların Tanımlanması
class Ball():
    RADIUS = 20
    def __init__(self, x, y, vX, vY):
        self.x = x
        self.y = y
        self.vX = vX
        self.vY = vY

    #  topun pencerede gösterilmesi
    def show(self, screen, color):
        pygame.draw.circle(screen, color, (self.x, self.y), self.RADIUS)


    #  topun konumunun güncellenmesi, topun bir sonraki koordinatları
    def update(self, screen, color1, color2, paddle, paddle2=None):
        #  öceki topları gizlemek için arkaplan rengi ile aynı renkte yapılması
        vx = self.x + self.vX
        vy = self.y + self.vY

        if paddle2 is None:
            #  topun x ekseninde sınıra çarpması ve yönünün değiştirilmesi(+,-)
            if vx < BORDER+Ball.RADIUS:
                self.vX = -self.vX
            #  topun y ekseninde sınıra çarpması ve yönünün değiştirilmesi
            elif  vy < BORDER+Ball.RADIUS or vy > HEIGHT-BORDER-Ball.RADIUS:
                self.vY = -self.vY
            #  topun paddle a çarpması
            elif vx+Ball.RADIUS > WIDTH-Paddle.WIDTH+2 and  abs(vy-paddle.y) < Paddle.HEIGHT//2:
                self.vX = -self.vX
            #  sınıra çarpmadığı durumlarda
            else:
                self.show(screen, color1)
                self.x = vx
                self.y = vy
                self.show(screen, color2)
        else:
            if  vy < BORDER+Ball.RADIUS or vy > HEIGHT-BORDER-Ball.RADIUS:
                self.vY = -self.vY
            #  topun paddle a çarpması
            elif (vx+Ball.RADIUS > WIDTH-Paddle.WIDTH+2 and  abs(vy-paddle.y) < Paddle.HEIGHT//2) or (vx-Ball.RADIUS < Paddle.WIDTH and abs(vy-paddle2.y) < Paddle.HEIGHT//2):
                self.vX = -self.vX
            else:
                self.show(screen, color1)
                self.x = vx
                self.y = vy
                self.show(screen, color2)



class Paddle():
    WIDTH = 20
    HEIGHT = 100

    def __init__(self, y):
        self.y = y

    #Rect(left, top, width, height)
    def show(self, screen, color, x=None, y=None):
        if x is None: x = WIDTH-self.WIDTH
        if y is None: y = self.y-(self.HEIGHT//2)
        #  paddle in oluşturulması
        pygame.draw.rect(screen, color, pygame.Rect(x, y, self.WIDTH, self.HEIGHT))

    def update(self, screen, color1, color2, x=None):
        vy = pygame.mouse.get_pos()[1]
        #  paddle in dikey kenarları sınırı geçmemesi için kontrol
        if vy-self.HEIGHT//2 > BORDER and vy+self.HEIGHT//2 < HEIGHT-BORDER:
            self.show(screen, color1, x=x)
            self.y = vy
            self.show(screen, color2, x=x)

class Game():
    def __init__(self):
        pygame.init()
        #  pencerenin oluşturulması
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # renkler
        self.fgcolor = pygame.Color("white")
        self.bgcolor = pygame.Color("black")
        self.screen.fill(self.bgcolor)

        #  sınırların çizimi
        self.drawBorder(self.screen, self.fgcolor)
        ## Nesnelerin oluşturulması
        # topun oluşturulması
        #  x ve y koordinatı , x ve y hızı
        self.ball = Ball(600, 300, -VELOCITY, -VELOCITY)
        #WIDTH-Ball.RADIUS-20, HEIGHT//2, -VELOCITY, -VELOCITY)

        #  topun çizdirlmesi
        self.ball.show(self.screen, self.fgcolor)
        #  paddle in pencredeki konumunu oluşturulması
        self.paddle = Paddle(HEIGHT//2)
        #  paddle in pencrede çizdirilmesi
        self.paddle.show(self.screen, self.fgcolor)

        # oyunun döngüsünün hızını azaltmak için
        self.t = pygame.time.Clock()

    def drawBorder(self, screen, color, left=None):
        pygame.draw.rect(screen, color, pygame.Rect(0, 0, WIDTH, BORDER))
        pygame.draw.rect(screen, color, pygame.Rect(0, HEIGHT-BORDER, WIDTH, BORDER))

        if left is  None:
            pygame.draw.rect(screen, color, pygame.Rect(0,0,BORDER, HEIGHT))


    def isFailed(self, xB):
        if xB >= WIDTH-BORDER-2 or xB < BORDER+2: return True
        else: return False

    def getRandomBall(self):
        # xB, yB
        xB = random.randint(200, 800)
        yB = random.randint(200, 400)
        if xB%2==0:
            return xB, yB, -1
        else:
            return xB, yB, 1

    def restart(self, left=None):
        runing = True
        while runing:
            e = pygame.event.poll()
            if e.type == pygame.MOUSEBUTTONDOWN:
                    #if(e.button == 1):
                    break
            elif  e.type == pygame.QUIT:
                runing = False
        if not runing: pygame.quit()

        self.ball.show(self.screen, self.bgcolor)
        self.paddle.show(self.screen, self.fgcolor)
        if left is not None:
            self.paddle2.show(self.screen, self.fgcolor, 0)
            self.drawBorder(self.screen,self.fgcolor, True)
        else:
            self.drawBorder(self.screen,self.fgcolor)
        self.ball.x, self.ball.y, vel = self.getRandomBall()
        self.ball.vX = vel*VELOCITY
        self.ball.vY = vel*VELOCITY
        self.ball.update(self.screen, self.bgcolor, self.fgcolor, self.paddle)
        #self.__init__(xB, yB, -VELOCITY, -VELOCITY)

    def gameLoop(self):
        while True:
            #  döngü hızı
            self.t.tick(FRAMERATE)
            #  pencereyi güncelle
            pygame.display.flip()
            self.ball.update(self.screen, self.bgcolor, self.fgcolor, self.paddle)
            #  yanma durumu kontrolü ve yeniden başlatma
            if self.isFailed(self.ball.x+self.ball.vX):
                self.restart()
            #  tahmin edilen değerler ile paddle in hareket etmesi, ai
            self.paddle.update(self.screen, self.bgcolor, self.fgcolor)

            #  oyunu sonlandırmak için
            self.evnt = pygame.event.poll()
            if self.evnt.type == pygame.QUIT:
                break

        #  pencereyi kapatma
        pygame.quit()

def main():
    g = Game()
    g.gameLoop()

if "__main__" == __name__:
    main()
