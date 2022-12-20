import numpy as np


def plume_mask(image: np.array, sensitivity=2):
    average = np.average(image)
    threshold = average * sensitivity

    mask = image > threshold

    return mask
