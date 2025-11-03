#./core/image_io.py
import numpy as np
# Leitura e gravação RAW de imagens

def read_raw(path, width, height):
    with open(path, 'rb') as f:
        data = np.frombuffer(f.read(), dtype=np.uint8)
    return data.reshape((height, width))

def write_raw(image, path):
    image.astype(np.uint8).tofile(path)

def to_qimage(image):
    """Converte numpy array (grayscale) em QImage."""
    from PyQt6.QtGui import QImage
    h, w = image.shape
    return QImage(image.data, w, h, w, QImage.Format.Format_Grayscale8)





