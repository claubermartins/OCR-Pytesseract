import cv2

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

#CARREGAR IMAGEM
#img = cv2.imread("PlacaFinal.jpg")
img = cv2.imread("BD1/placa-carro5.jpg")
imgaux = cv2.resize(img, None, fx = 0.2, fy = 0.2)
cv2.imshow("Carro Original", imgaux)


#cv2.resizeWindow("Carro Original", 500, 500)

#CONVERTER IMAGEM EM ESCALA CINZA
imgCinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCinzaaux = cv2.resize(imgCinza, None, fx = 0.2, fy = 0.2)

cv2.imshow("Carro Cinza", imgCinzaaux)



#LIMIARIZAR IMAGEM - duas cores
#_, imgBin = cv2.threshold(imgCinza, 90, 255, cv2.THRESH_BINARY)
_, imgBin = cv2.threshold(imgCinza, 112, 255, cv2.THRESH_BINARY)
#_, imgBin = cv2.threshold(imgCinza, 135, 255, cv2.THRESH_BINARY)

imgBinaux = cv2.resize(imgBin, None, fx = 0.2, fy = 0.2)
cv2.imshow("Limiarizado Preto e Branco", imgBinaux)

_, imgBin1 = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
#cv2.imshow("Limiarizado Colorido", imgBin1)

#Para melhorar a detecção dos Contornos
desfoque = cv2.GaussianBlur(imgBin, (5, 5), 0)
#cv2.imshow("Desfoque", desfoque)

#Detectar os Contornos
contornos, hier = cv2.findContours(imgBin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#contornos1, hier = cv2.findContours(imgBin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#Comentado Pq aqui mostra todos os contornos, mas deseja-se apenas os 'retos'
#cv2.drawContours(img, contornos, -1, (0, 255, 0), 2)
#cv2.imshow("Contorno", img)

#Para solucionar o  problema...
for c in contornos:
    perimetro = cv2.arcLength(c, True)

    if perimetro > 120:
    #if perimetro > 900 and perimetro < 1200:

        aprox = cv2.approxPolyDP(c, 0.02 * perimetro, True)

        if len(aprox) == 4:
            (x, y, alt, lar) = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + alt, y + lar), (0, 255, 0), 2)
            aux = img[y:y + lar, x:x + alt]
            cv2.imwrite("PlacaFinal.jpg", aux)
            cv2.imshow("Placa do Carro", aux)

imgaux2 = cv2.resize(img, None, fx = 0.2, fy = 0.2)
cv2.imshow("Contornos Filtrados", imgaux2)

#Aumenta a imagem da placa recortada em 4 x 4, para melhor processamento
imagemAumentada = cv2.resize(aux, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
cv2.imwrite('aumentada2.jpg', imagemAumentada)

#conversão da imagem aumentada para escala de cinza
imagemAumentada = cv2.cvtColor(imagemAumentada, cv2.COLOR_BGR2GRAY)
 # Binariza imagem
ret, imagemAumentada = cv2.threshold(imagemAumentada, 105, 255, cv2.THRESH_BINARY)
cv2.imshow("Limiar", imagemAumentada)
#Aplicação do filtro gaussiano, com kernel de 5 x 5
imagemAumentada = cv2.GaussianBlur(imagemAumentada, (5, 5), 0)
cv2.imwrite('novaimg.jpg', imagemAumentada)
#Recuperação da imagem escrita, pelo atributo Image do PIL, pois o tesseract abre apenas arquivos dessa maneira
imagem = Image.open('novaimg.jpg')
#Seto o cmd do tesseract com o caminho de onde o mesmo está localizado
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
#Recupero a placa e faço a leitura da string da mesma e a printo
saida = pytesseract.image_to_string(imagem)
print(saida)

cv2.waitKey(0)
cv2.destroyAllWindows()
