#!/usr/bin/env python3
"""
Main interface for the Accessible Cinema system.
Provides a command-line interface for video description generation and audio extraction.
"""

import argparse
import sys
import os
from pathlib import Path
from describer import generate_description
from extract_descriptions import get_descriptions, convert_descriptions_to_text
import csv

def main():
    parser = argparse.ArgumentParser(
        description="Accessible Cinema - AI-Powered Video Description System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate descriptions for a video
  python main.py describe video.mp4 --output descriptions.json

  # Extract descriptions from audio files
  python main.py extract original.wav described.wav --output descriptions.csv

  # Process video with custom settings
  python main.py describe video.mp4 --threshold 0.8 --start-frame 100 --end-frame 1000
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Describe command
    describe_parser = subparsers.add_parser('describe', help='Generate descriptions for a video')
    describe_parser.add_argument('video_path', help='Path to the input video file')
    describe_parser.add_argument('--output', '-o', default='descriptions.json', 
                               help='Output file for descriptions (default: descriptions.json)')
    describe_parser.add_argument('--threshold', '-t', type=float, default=0.75,
                               help='Similarity threshold for frame grouping (default: 0.75)')
    describe_parser.add_argument('--start-frame', '-s', type=int, default=0,
                               help='Starting frame (default: 0)')
    describe_parser.add_argument('--end-frame', '-e', type=int, default=None,
                               help='Ending frame (default: process entire video)')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract descriptions from audio files')
    extract_parser.add_argument('original_audio', help='Path to original audio file')
    extract_parser.add_argument('described_audio', help='Path to audio file with descriptions')
    extract_parser.add_argument('--output', '-o', default='extracted_descriptions.csv',
                               help='Output CSV file (default: extracted_descriptions.csv)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'describe':
            print(f"Processing video: {args.video_path}")
            print(f"Output file: {args.output}")
            print(f"Threshold: {args.threshold}")
            
            descriptions, timestamps = generate_description(
                video_path=args.video_path,
                start_frame=args.start_frame,
                end_frame=args.end_frame,
                threshold=args.threshold
            )
            
            # Save descriptions to JSON
            import json
            output_data = []
            for desc, timestamp in zip(descriptions, timestamps):
                output_data.append({
                    'timestamp': timestamp,
                    'description': desc.content if hasattr(desc, 'content') else str(desc)
                })
            
            with open(args.output, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            print(f"Generated {len(descriptions)} descriptions")
            print(f"Results saved to: {args.output}")
            
        elif args.command == 'extract':
            print(f"Extracting descriptions from audio files...")
            print(f"Original audio: {args.original_audio}")
            print(f"Described audio: {args.described_audio}")
            print(f"Output file: {args.output}")
            
            descriptions, timestamps = get_descriptions(args.original_audio, args.described_audio)
            text_descriptions = convert_descriptions_to_text(descriptions)
            
            with open(args.output, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Start Time (s)', 'End Time (s)', 'Description'])
                for i, text_desc in enumerate(text_descriptions):
                    writer.writerow([timestamps[i][0], timestamps[i][1], text_desc])
            
            print(f"Extracted {len(text_descriptions)} descriptions")
            print(f"Results saved to: {args.output}")
    
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 