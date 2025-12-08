# ./core/local_ops.py

import numpy as np

# máscaras clássicas:
MASKS = {
    "Média 3x3": np.ones((3,3))/9,
    "Média 5x5": np.ones((5,5))/25,
    "Laplaciano": np.array([[0, -1, 0],
                            [-1, 4, -1],
                            [0, -1, 0]]),
    "Laplaciano Alternativo": np.array([[-1, -1, -1],
                                        [-1, 8, -1],
                                        [-1, -1, -1]]),
    "Sobel X": np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]]),
    "Sobel Y": np.array([[-1, -2, -1],
                         [0, 0, 0],
                         [1, 2, 1]]),
    "Sharpen": np.array([[0, -1, 0],
                         [-1, 5, -1],
                         [0, -1, 0]]),
    "Gaussiano 3x3": np.array([[1, 2, 1],
                               [2, 4, 2],
                               [1, 2, 1]]) / 16
}

# Operações Locais

# função de convolução genérica
def convolve(img, kernel):
    # Pega dimensões da imagem e do kernel
    h, w = img.shape
    kh, kw = kernel.shape

    # Calcula padding para bordas
    pad_h, pad_w = kh // 2, kw // 2

    # Adiciona borda à imagem
    padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')

    # Cria imagem resultado vazia
    result = np.zeros_like(img, dtype=np.float32)

    for i in range(h):
        for j in range(w):
            # Pega região 3x3 ao redor do pixel (i,j)
            region = padded[i:i+kh, j:j+kw]
            # FAZ A CONVOLUÇÃO: multiplicação + soma
            result[i, j] = np.sum(region * kernel)
            # region * kernel: multiplica elemento por elemento
            # np.sum(): soma todos os 9 valores resultantes
    return np.clip(result, 0, 255).astype(np.uint8)