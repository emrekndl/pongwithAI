import pong
import os
import pandas as pd
import pickle


#pong.VELOCITY = 2

class PongAi(pong.Game):
    """ Oluşturulan veri kümesinin KNN ile eğitilmesi ve test edilmesi  """
    def __init__(self):
        super().__init__()

        #  Eğitilmiş modelin yüklenmesi
        with open("Model/knn_model.pkl", "rb") as f:
            self.clf = pickle.load(f)

        #  yeni veriler ile test edilmesi
        self.df = pd.DataFrame(columns=["x", "y", "vX", "vY"])
        #########
        g = pong.Game()
        self.screen.fill(self.bgcolor)
        self.drawBorder(self.screen, self.fgcolor, True)
        self.paddle2 = pong.Paddle(pong.HEIGHT//2)
        self.paddle2.show(self.screen, self.bgcolor, 0)

        self.gameLoop()

    def paddleUpdateAI(self, screen, color1, color2, prePY):
        if prePY-self.paddle.HEIGHT//2 > pong.BORDER and prePY+self.paddle.HEIGHT//2 < pong.HEIGHT-pong.BORDER:
            self.paddle.show(screen, color1)
            self.paddle.y = prePY
            self.paddle.show(screen, color2)


    def gameLoop(self):
        self.i = 0
        while True:
            #  döngü hızı
            self.t.tick(pong.FRAMERATE)
            #  pencereyi güncelle
            pong.pygame.display.flip()
            #  yeni verilerde test edilmesi
            self.toPredict = self.df.append({"x" : self.ball.x, "y" : self.ball.y, "vX" : self.ball.vX, "vY" : self.ball.vY}, ignore_index=True)
            #  print(f"prePY: {predictPy}")
            #  test , verilen yeni değerler ile sonucun tahmin edilmesi
            self.predictPy = self.clf.predict(self.toPredict)
            self.ball.update(self.screen, self.bgcolor, self.fgcolor, self.paddle, self.paddle2)
            #  yanma durumu kontrolü ve yeniden başlatma
            if self.isFailed(self.ball.x+self.ball.vX):
                self.i = 0
                print("Failed")
                self.restart(left=True)

            elif (self.ball.x+self.ball.vX)+pong.Ball.RADIUS > pong.WIDTH-pong.Paddle.WIDTH+2 and  abs((self.ball.y+self.ball.vY)-self.paddle.y) < pong.Paddle.HEIGHT//2:
                #  yanmadan kaçkez oynandığının yazılması
                self.i += 1
                os.system("clear")
                #  print(chr(27) + "[2J")
                print(f"AI: {self.i}")

            #  tahmin edilen değerler ile paddle in hareket etmesi, ai
            self.paddle2.update(self.screen, self.bgcolor, self.fgcolor, 0)
            self.paddleUpdateAI(self.screen, self.bgcolor, self.fgcolor, int(self.predictPy))

            #  oyunu sonlandırmak için
            self.evnt = pong.pygame.event.poll()
            if self.evnt.type == pong.pygame.QUIT:
                break

        #  pencereyi kapatma
        pong.pygame.quit()



def mainAI():
    p = PongAi()

if "__main__" == __name__:
    mainAI()
