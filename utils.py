from tqdm import tqdm
import numpy as np
import os
import cv2
from skimage.metrics import structural_similarity as ssim

def load_video(video_path, start_frame=0, end_frame=None):
    """
    Load a video file and return the frames as a list of numpy arrays.
    """
    video = cv2.VideoCapture(video_path)
    framerate= video.get(cv2.CAP_PROP_FPS)
    if not video.isOpened():
        raise ValueError(f"Could not open video file {video_path}")
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    frames = []
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if end_frame is None:
        end_frame = frame_count
    print("loading video...")
    for i in tqdm(range(start_frame, end_frame)):
        ret, frame = video.read()
        if not ret:
            break
        frames.append(frame)
    
    video.release()
    return frames, framerate

def check_similarity(img1, img2, threshold=0.75):
    """
    Check if two images are similar based on a threshold.
    """
    if img1.shape != img2.shape:
        return False
    
    # Calculate the Structural Similarity Index (SSI)
    ssim_value, diff = ssim(img1, img2, multichannel=True, channel_axis=2, full=True)
    return ssim_value >= threshold

def make_chunks(frames, frame_rate):
    """
    Split frames into chunks of frames based on the temperal similarity.
    """
    chunks = []
    timestamps=[]
    current_chunk = [frames[0]]
    current_timestamp = 0
    print("chunking video...")
    for i in tqdm(range(1, len(frames))):
        if check_similarity(frames[i], frames[i-1]):
            current_chunk.append(frames[i])
        else:
            chunks.append(current_chunk)
            timestamps.append(current_timestamp)
            current_chunk = [frames[i]]
            current_timestamp = i / frame_rate
    
    if current_chunk:
        chunks.append(current_chunk)
        timestamps.append(current_timestamp)
    return chunks, timestamps

