import pong
import os
import pandas as pd
import pickle

pong.VELOCITY = 6 #18

class PongAi(pong.Game):
    """ Oluşturulan veri kümesinin makine öğrenmesi modelleri ile eğitilmesi ve test edilmesi  """
    def __init__(self):
        super().__init__()

        # aı eğitim
        #self.data = open("dataSet/gameDataSet2.csv", "a")

        #  KNN ile sınıflandırma
        #  Eğitimin modelin yüklenmesi (pickle)
        with open("Model/knn_model.pkl", "rb") as f:
           self.clf = pickle.load(f)
        #  tODO: Keras ile 3 katmanlı yapay sinir ağı, eğitilmiş modelin kullanılması
        #import keras
        #from keras.models import load_model
        #self.clf = load_model("Model/neuralNetwork_model.h5")

        #  yeni veriler ile test edilmesi
        self.df = pd.DataFrame(columns=["x", "y", "vX", "vY"])

        g = pong.Game()
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
            self.ball.update(self.screen, self.bgcolor, self.fgcolor, self.paddle)
            #  yanma durumu kontrolü ve yeniden başlatma
            if self.isFailed(self.ball.x+self.ball.vX):
                self.i = 0
                print("Failed")
                self.restart()

            elif (self.ball.x+self.ball.vX)+pong.Ball.RADIUS > pong.WIDTH-pong.Paddle.WIDTH+2 and  abs((self.ball.y+self.ball.vY)-self.paddle.y) < pong.Paddle.HEIGHT//2:
                #  yanmadan kaçkez oynandığının yazılması
                self.i += 1
                os.system("clear")
                #  print(chr(27) + "[2J")
                print(f"AI: {self.i}")
                #  ai eğitim
                #  topun ile paddle in konumlarının yazdırılması
                #print(f"{self.ball.x},{self.ball.y},{self.ball.vX},{self.ball.vY},{self.paddle.y}", file=self.data)

            #  tahmin edilen değerler ile paddle in hareket etmesi, ai
            self.paddleUpdateAI(self.screen, self.bgcolor, self.fgcolor, int(self.predictPy))

            #  oyunu sonlandırmak için
            self.evnt = pong.pygame.event.poll()
            if self.evnt.type == pong.pygame.QUIT:
                break

        #  pencereyi kapatma
        pong.pygame.quit()
        #self.data.close()



def mainAI():
    p = PongAi()

if "__main__" == __name__:
    mainAI()
