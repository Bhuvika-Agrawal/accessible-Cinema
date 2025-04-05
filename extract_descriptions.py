import sys
import tqdm
import os
import numpy as np
import csv
import librosa
from vosk import Model, KaldiRecognizer

def get_descriptions(original_audio_file, described_audio_file):
    """
    Compare the original audio file with the described audio file and return the descriptions.
    """
    # Load the original audio file
    print(f"Loading original audio file: {original_audio_file}")
    original_audio, original_sr = librosa.load(original_audio_file, sr=16000)

    # Load the described audio file
    print(f"Loading described audio file: {described_audio_file}")
    described_audio, described_sr = librosa.load(described_audio_file, sr=16000)

    # Check if the lengths of the audio files match
    if len(original_audio) != len(described_audio):
        raise ValueError("The lengths of the original and described audio files do not match.")
    if original_sr != described_sr:
        raise ValueError("The sample rates of the original and described audio files do not match.")

    # Calculate the differences between the two audio files
    description_audio=described_audio-original_audio

    # Threshold to determine significant differences
    threshold = 0.01

    # Get indices where differences exceed the threshold
    significant_differences = np.where(np.abs(description_audio) > threshold)[0]

    # Extract descriptions based on significant differences
    descriptions = []
    timestamps=[]
    prev=0
    start=0
    print("extracting description audios...")
    for index in tqdm.tqdm(significant_differences[1:]):
        if index - prev == 1: prev=index
        else:
            description=description_audio[start:prev]
            descriptions.append(description)
            timestamps.append((start/original_sr, prev/original_sr))
            start=index
            prev=index

    return descriptions, timestamps

def convert_descriptions_to_text(descriptions, sample_rate=16000):
    """
    Convert the extracted descriptions to text format.
    """
    # Initialize Vosk model for speech recognition
    model = Model("vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, sample_rate)

    text_descriptions = []
    print("Converting descriptions to text...")
    for description in tqdm.tqdm(descriptions):
        # Convert the audio description to text
        recognizer.AcceptWaveform(description.tobytes())
        result = recognizer.Result()
        text_descriptions.append(result)

    return text_descriptions

def main():
    if len(sys.argv) != 4:
        print("Usage: python extract_descriptions.py <original_audio_file> <described_audio_file> <output_csv_file>")
        sys.exit(1)

    original_audio_file = sys.argv[1]
    described_audio_file = sys.argv[2]

    # Get descriptions from the audio files
    descriptions, timestamps = get_descriptions(original_audio_file, described_audio_file)

    # Convert descriptions to text format
    text_descriptions = convert_descriptions_to_text(descriptions)

    # Save the descriptions and timestamps to a CSV file
    output_csv_file = sys.argv[3]
    with open(output_csv_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Start Time (s)', 'End Time (s)', 'Description'])
        print("Saving descriptions to CSV file...")
        for i in tqdm.tqdm(range(len(text_descriptions))):
            writer.writerow([timestamps[i][0], timestamps[i][1], text_descriptions[i]])
    
