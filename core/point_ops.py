#   ./core/point_ops.py
#   Operações Pontuais
import numpy as np

#brilho
def adjust_brightness(img, value):
    return np.clip(img + value, 0, 255).astype(np.uint8)
 
#limiarização
def threshold_image(img, thresh):   
    return np.where(img >= thresh, 255, 0).astype(np.uint8) 
