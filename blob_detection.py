from math import sqrt
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import numpy as np


def plume_mask(image: np.array, sensitivity=2):

    flat = np.sort(image.flatten())
    print(flat)
    average = np.average(image)
    # threshold = flat[int(len(flat)*0.96)]
    threshold = average * sensitivity

    mask = image > threshold

    return mask
