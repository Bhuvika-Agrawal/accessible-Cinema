# Accessible Cinema - AI-Powered Video Description System

An intelligent system that generates audio descriptions for videos to make them accessible to visually impaired users.

## Features

- **Video Analysis**: Automatically extracts key frames from videos using similarity detection
- **AI Description Generation**: Uses Google's Gemini AI to generate detailed descriptions of video content
- **Audio Description Extraction**: Extracts descriptions from audio files using speech recognition
- **Timestamp Synchronization**: Maintains precise timing information for descriptions

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd accessible-Cinema
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download required models:
```bash
# Download Vosk model for speech recognition
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.tar.gz
tar -xzf vosk-model-small-en-us-0.15.tar.gz
```

## Usage

### Generating Video Descriptions

```python
from describer import generate_description

# Generate descriptions for a video
descriptions, timestamps = generate_description(
    video_path="path/to/video.mp4",
    start_frame=0,
    end_frame=None,  # Process entire video
    threshold=0.75   # Similarity threshold
)
```

### Extracting Descriptions from Audio

```bash
python extract_descriptions.py original_audio.wav described_audio.wav output.csv
```

## Configuration

- **Similarity Threshold**: Adjust the `threshold` parameter in `generate_description()` to control frame grouping sensitivity
- **AI Model**: Currently uses Gemini 2.0 Flash Lite for description generation
- **Speech Recognition**: Uses Vosk model for audio-to-text conversion

## Project Structure

- `describer.py`: Main video processing and description generation
- `extract_descriptions.py`: Audio description extraction and conversion
- `utils.py`: Utility functions for image similarity detection
- `requirements.txt`: Project dependencies

## Next Steps

See the project roadmap for planned enhancements and features.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.
