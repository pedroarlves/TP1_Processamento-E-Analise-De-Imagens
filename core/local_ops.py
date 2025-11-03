# ./core/local_ops.py

import numpy as np

# máscaras clássicas:

MASKS = {
    "Média 3x3": np.ones((3,3))/9,
    "Laplaciano": np.array([[0, -1, 0],
                            [-1, 4, -1],
                            [0, -1, 0]])
}

# Operações Locais

#função de convolução genérica
def convolve(img, kernel):
    h, w = img.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    result = np.zeros_like(img, dtype=np.float32)
    for i in range(h):
        for j in range(w):
            region = padded[i:i+kh, j:j+kw]
            result[i, j] = np.sum(region * kernel)
    return np.clip(result, 0, 255).astype(np.uint8)
