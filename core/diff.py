# ./core/diff.py

import numpy as np

# Diferença entre Imagens

def image_difference(img1, img2):
    return np.abs(img1.astype(int) - img2.astype(int)).astype(np.uint8)
