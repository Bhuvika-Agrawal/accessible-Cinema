from tqdm import tqdm
import numpy as np
import os
import cv2
from skimage.metrics import structural_similarity as ssim

def check_similarity(img1, img2, threshold=0.75):
    """
    Check if two images are similar based on a threshold.
    """
    if img1.shape != img2.shape:
        return False
    
    # Calculate the Structural Similarity Index (SSI)
    ssim_value, diff = ssim(img1, img2, multichannel=True, channel_axis=2, full=True)
    return ssim_value >= threshold

