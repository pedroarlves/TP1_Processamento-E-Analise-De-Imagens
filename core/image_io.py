import os
import numpy as np
from PyQt6.QtGui import QImage

def read_raw(path, width, height):
    """Lê uma imagem RAW (8 bits, escala de cinza)."""
    with open(path, "rb") as f:
        data = np.frombuffer(f.read(), dtype=np.uint8)
    return data.reshape((height, width))

def write_raw(image, path):
    """Grava imagem numpy em arquivo RAW (8 bits, escala de cinza)."""
    image.astype(np.uint8).tofile(path)

def to_qimage(image):
    """Converte numpy array (grayscale) em QImage."""
    h, w = image.shape
    return QImage(image.data, w, h, w, QImage.Format.Format_Grayscale8)

def auto_detect_raw_shape(path):
    """
    Detecta automaticamente largura e altura de uma imagem RAW (8 bits, grayscale).
    Prioriza imagens quadradas (muito comuns em bases de teste).
    """
    size = os.path.getsize(path)

    # Tenta raiz quadrada (imagens quadradas)
    root = int(np.sqrt(size))
    if root * root == size:
        return root, root

    # Testa outras combinações padrão
    possible_sizes = [64, 128, 256, 512, 1024, 2048, 4096]
    for w in possible_sizes:
        h = size // w
        if w * h == size:
            return w, h

    return None, None
