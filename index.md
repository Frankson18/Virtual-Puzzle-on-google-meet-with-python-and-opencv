# Virtual Puzzle on google meet with python and opencv

# INTRODUÇÃO

Trabalho final da disciplina de Processamento digital de imagens da UFRN. Inspirado no vídeo do [MurtazasWorkshopRoboticsandAI](https://www.youtube.com/watch?v=6DxN8G9vB50&t=87s), o quebra-cabeça virtual é um programa que faz com que o usuário consiga manipular fotos presentes no seu visor utilizando o movimento de suas mãos, assim sendo possível criar um quebra-cabeça para ser montado.

### **Exemplo de funcionamento:**

![ezgif.com-gif-maker.gif](Virtual%20Puzzle%20on%20google%20meet%20with%20python%20and%20open%20001108725ca94819a65e9cfead454e68/ezgif.com-gif-maker.gif)

# COMO UTILIZAR

para poder utilizar você vai ter instalado o `python`, eu utilizei a `versão 3.9`, o programa de captura de tela `OBS` para gerar a câmera virtual para usar no meet e instalar no python a biblioteca `cvzone versão 1.4`.

Para exemplo utilizei uma imagem 1000x200 com o nome [test.jpg](https://saskatoonfood.ca/images/headers/1000x200-StoonDusk.jpg), assim quando for executar e tiver outra imagem basta muda o endereço no código.

### Passo a passo

1. abri o OBS e iniciar a câmera virtual
2. executar o código python
3. se divertir com o a montagem do quebra-cabeça

caso queria ver o passo a passo pode assistir o vídeo: 

[https://www.youtube.com/watch?v=5MpKMHGrYTk](https://www.youtube.com/watch?v=5MpKMHGrYTk)

# FUNCIONAMENTO DO CÓDIGO

```python
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
    #iniciando varaiveis da imagem
    def __init__(self,posCenter,size=[200,200]):
        self.posCenter = posCenter
        self.size = size

    def updata(self,cursor):
        cx,cy = self.posCenter
        w,h = self.size

        # conferir se o dedo esta em cima da imagem e move para a posição do dedo
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
```

---

Começo com a importação das bibliotecas necessárias para o funcionamento: `cv2` para o `opencv`, `cvzone` para poder utilizar bibliotecas de visão computacional,`pyvirtualcam` para criar a câmera virtual.

```python
import cv2
import cvzone
import pyvirtualcam
from pyvirtualcam import PixelFormat
from cvzone.HandTrackingModule import HandDetector # detectar mãos
```

---

logo após inicio a variável de captura o vídeo da webcam e seleciono o seu tamanho para ser 1280x720 e também inicializo a função que responsável por detectar minha mão com 70% de precisão.

```python
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.7) #precisão de 70%
```

---

Aqui eu crio a classe `imgObject` responsável por guarda todas as informações importantes para minha imagem, e o método `update` que atualiza a posição central da imagem, que vamos usar para poder fazer seu movimento na tela, futuramente.

```python
class imgObject():
    #iniciando varaiveis da imagem
    def __init__(self,posCenter,size=[200,200]):
        self.posCenter = posCenter
        self.size = size

    def updata(self,cursor):
        cx,cy = self.posCenter
        w,h = self.size

        # conferir se o dedo esta em cima da imagem e move para a posição do dedo
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2 :
            self.posCenter = cursor
```

---

Crio a lista `imgList` que vai guarda todas as imagens do quebra cabeça. Então finalmente pego a imagem completa do quebra-cabeça e divido em 5 partes iguais e as salvo, depois crio uma lista com 5 objetos `imgObject`. 

```python
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
```

---

Essa linha em especifico é responsável por fazer a câmera virtual   

```python
with pyvirtualcam.Camera(width=1280, height=720, fps=24, fmt=PixelFormat.BGR) as cam:
```

---

Aqui que começa propriamente dito o código. Começo então pegando a imagem da webcam e já começo desenhando a minha mão no vídeo. Logo após pega a posição dos dedos. Dentro do `if` confiro a distancia entre os dedos indicador e médio, se for menos que 40 então eles estão não posição de `click`, segura a imagem e logo depois confiro se estão dentro da imagem, se estiver então eu atualizo a posição da imagem para a do meu cursor. 

```python
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
```

---

Por ultimo eu uso o `try` e `except`  para tentar plotar a imagem do quebra-cabeça na tela, usando os dados do `imgObject`, para isso uso o `imagem.copy()` 

```python
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
```
