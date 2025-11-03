# ./core/histogram.py
import numpy as np
import matplotlib.pyplot as plt

def plot_histogram(img):
    plt.figure()
    plt.title("Histograma")
    plt.hist(img.ravel(), bins=256, range=[0,256])
    plt.show()

