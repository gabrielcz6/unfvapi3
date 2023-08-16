import requests
from PIL import Image
import io
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np
import uuid

def get_image_from_firebase(url):
    response = requests.get(url)
    return response.content  # Esto es un objeto de bytes de la imagen


def reg_rostro(img):
    pixeles = np.array(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    data = np.array(img)
    for i in range(len(caras)):
        x1,y1,ancho, alto = caras[i]['box']
        x2,y2 = x1 + ancho, y1 + alto
        #pyplot.subplot(1, len(caras), i+1)
        #pyplot.axis('off')
        cara_reg = data[y1:y2, x1:x2]
        cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC)
        
        # Codifica la imagen en memoria en lugar de escribirla en el disco
        is_success, im_buf_arr = cv2.imencode(".jpg", cara_reg)
        byte_im = io.BytesIO(im_buf_arr)
        # Guardar la imagen codificada en un archivo JPG
        with open(f'rostro_{i}.jpg', 'wb') as f:
            f.write(im_buf_arr)

        # Convierte el objeto BytesIO en un objeto PIL Image
        img_pil = Image.open(byte_im)
        
        #print(type(img_pil))
    return img_pil 


def compare_images(image1, image2):
 try:     
     image1=reg_rostro(image1)
     if os.path.isfile("test.jpg"):
       os.remove("test.jpg")

     image2=reg_rostro(image2)

     
     def orb_sim(img1, img2):
        orb = cv2.ORB_create()  # Creamos el objeto de comparación
        
        img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
        img2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)
        kpa, descr_a = orb.detectAndCompute(img1, None)  # Creamos descriptor 1 y extraemos puntos claves
        kpb, descr_b = orb.detectAndCompute(img2, None)  # Creamos descriptor 2 y extraemos puntos claves
        
        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) # Creamos comparador de fuerza

        matches = comp.match(descr_a, descr_b)  # Aplicamos el comparador a los descriptores

        regiones_similares = [i for i in matches if i.distance < 70] # Extraemos las regiones similares en base a los puntos claves
        if len(matches) == 0:
            return 0
        return len(regiones_similares) / len(matches)  # Exportamos el porcentaje de similitud
     
     # Usamos el método de la aplicación anterior para comparar las imágenes
     similitud = orb_sim(image1, image2)
     return similitud
 except Exception as e:
    # Esto capturará cualquier otro error que no fue capturado por los except anteriores
    print(f'Error inesperado: {e}')
    return 0
