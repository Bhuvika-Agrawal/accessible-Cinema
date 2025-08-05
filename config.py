"""
Configuration settings for the Accessible Cinema system.
"""

import os
from pathlib import Path

class Config:
    """Configuration class for the Accessible Cinema system."""
    
    # AI Model Settings
    AI_MODEL = "gemini-2.0-flash-lite"
    AI_TEMPERATURE = 0.8
    
    # Video Processing Settings
    DEFAULT_SIMILARITY_THRESHOLD = 0.75
    FRAME_RESIZE_WIDTH = 256
    FRAME_RESIZE_HEIGHT = 144
    FRAME_FORMAT = "JPEG"
    
    # Audio Processing Settings
    AUDIO_SAMPLE_RATE = 16000
    AUDIO_DIFFERENCE_THRESHOLD = 0.01
    
    # Speech Recognition Settings
    VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"
    
    # File Paths
    OUTPUT_DIR = Path("output")
    TEMP_DIR = Path("temp")
    
    # System Messages
    SYSTEM_PROMPT = """You are an AI integrated into an audio description application. 
    Your job is to generate audio descriptions for the given video, which will be given to you as a sequence of frames. 
    Each frame is given to you as a base64 encoding string of a JPEG format. 
    Your job is to generate a detailed and accurate description of the video based on the frames. 
    Please make sure to include all relevant details and context in your description. 
    Note that we are not asking you for frame-wise description, but we are asking you to interpret the given sequence of frames as a video, 
    interpret what is going on, and then generate a description of the video. 
    Please don't include phrases like "here is the description", just jump into the description, 
    as the text which you will give is directly used in the audio describer application."""
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.TEMP_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def get_google_api_key(cls):
        """Get Google API key from environment variable."""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable not set. "
                "Please set your Google API key: export GOOGLE_API_KEY='your-api-key'"
            )
        return api_key 