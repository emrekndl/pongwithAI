from pong import *


class dataCreate(Game):
    """ Kendi veri setimiz oluşturma sınıfı """
    def __init__(self):
        super().__init__()
        #  csv dosyası veri kümesi oluşturma
        #  yeni veri kümesi oluşturmak için dosyayı "w" kipi ile açın
        self.dataSet = open("dataSet/gameDataSet.csv", "a")
        #  gameDataSet.csv -> sadece topun paddle a çağtığı anları kaydedlmiş halidir
        #  gameDataSet2.csv -> yanma dışındaki tün anları kaydedilmiş halidir.

        # veri kümesi tablo başlıkları,yalnızca yeni dosya oluşturulurken
        #print("x,y,vX,vY,pY", file=self.dataSet)

        self.g = Game()
        self.gameLoop()

    def gameLoop(self):
        while True:
            #  döngü hızı
            self.t.tick(FRAMERATE)
            #  pencereyi güncelle
            pygame.display.flip()
            self.ball.update(self.screen, self.bgcolor, self.fgcolor, self.paddle)
            self.paddle.update(self.screen, self.bgcolor, self.fgcolor)
            #  yanma durumu kontrolü ve yeniden başlatma
            if self.isFailed(self.ball.x+self.ball.vX):
                print("Failed")
                self.restart()
            elif (self.ball.x+self.ball.vX)+Ball.RADIUS > WIDTH-Paddle.WIDTH+2 and  abs((self.ball.y+self.ball.vY)-self.paddle.y) < Paddle.HEIGHT//2:
                #  topun ile paddle in konumlarının yazdırılması
                print(f"ball x: {self.ball.x} ball y: {self.ball.y} paddle y: {self.paddle.y}")
                print(f"{self.ball.x},{self.ball.y},{self.ball.vX},{self.ball.vY},{self.paddle.y}", file=self.dataSet)
            #else:
            #   print(f"{self.ball.x},{self.ball.y},{self.ball.vX},{self.ball.vY},{self.paddle.y}", file=self.dataSet)
            #  oyunu sonlandırmak için
            self.evnt = pygame.event.poll()
            if self.evnt.type == pygame.QUIT:
                break

        #  pencereyi kapatma
        pygame.quit()
        #  dosyayı kapatma
        self.dataSet.close()


def mainData():
    dc = dataCreate()

if "__main__" == __name__:
    mainData()
