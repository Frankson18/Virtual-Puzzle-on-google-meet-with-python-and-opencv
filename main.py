import cv2
import cvzone
import pyvirtualcam
from pyvirtualcam import PixelFormat
from cvzone.HandTrackingModule import HandDetector # detectar mãos

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.7) #precisão de 70%

class imgObject():
    #iniciando varaiveis do retangulo
    def __init__(self,posCenter,size=[200,200]):
        self.posCenter = posCenter
        self.size = size

    def updata(self,cursor):
        cx,cy = self.posCenter
        w,h = self.size

        # conferir se o dedo esta em cima do quadrado e move para a posição do dedo
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2 :
            self.posCenter = cursor

imgList = []

#preparando a imagem para o quebra cabeça
imagem = cv2.imread("test.jpg")
imagem1 = imagem[0:200,0:200]
imagem2 = imagem[0:200,200:400]
imagem3 = imagem[0:200,400:600]
imagem4 = imagem[0:200,600:800]
imagem5 = imagem[0:200,800:1000]
cv2.imwrite("test3.jpg",imagem1)
cv2.imwrite("test4.jpg",imagem2)
cv2.imwrite("test1.jpg",imagem3)
cv2.imwrite("test2.jpg",imagem4)
cv2.imwrite("test0.jpg",imagem5)

for x in range(5):
    imgList.append(imgObject([x*250+150,150]))

with pyvirtualcam.Camera(width=1280, height=720, fps=24, fmt=PixelFormat.BGR) as cam:
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, _ = detector.findPosition(img) # posição da mão e dos dedos

        if lmList:
            l, _, _ = detector.findDistance(8,12,img,draw=False) # conta a distancia dos dedos

            #conferir se os dedos estão juntos ou não (click)
            if l < 40 :
                cursor = lmList[8] #posição do dedo indicador
                # atualiza a posição
                for rect in imgList:
                    rect.updata(cursor)
        try:
            #desenhar imagem na tela
            for i, rect in enumerate(imgList):
                filename = "test%d.jpg" % i
                cx, cy = rect.posCenter
                w, h = rect.size
                imagem = cv2.imread(filename)
                imagem = cv2.flip(imagem, 1)
                img[cy-h//2:cy+h//2,cx-w//2:cx+w//2] = imagem.copy()

                #parte verde do retangulo
                cvzone.cornerRect(img,(cx-w//2,cy-h//2,w,h),20,rt=0)
        except:
            pass

        cam.send(img)
        cam.sleep_until_next_frame()

        cv2.waitKey(1)



































