#   ./core/point_ops.py
#   Operações Pontuais
import numpy as np



#brilho
def adjust_brightness(img, value):
    """
    Ajusta o brilho da imagem (8 bits, grayscale).
    value pode variar de -255 a +255.
    """
    result = img.astype(np.int16) + value
    result = np.clip(result, 0, 255)
    return result.astype(np.uint8)

 
#limiarização
def threshold_image(img, thresh):   
    return np.where(img >= thresh, 255, 0).astype(np.uint8) 
