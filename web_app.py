#!/usr/bin/env python3
"""
Web interface for the Accessible Cinema system.
Provides a user-friendly web interface for video description generation.
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from pathlib import Path
from werkzeug.utils import secure_filename
import tempfile
import threading
from describer import generate_description
from config import Config

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Ensure directories exist
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(exist_ok=True)

# Global variable to store processing status
processing_status = {}

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a video file.'}), 400
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Get processing parameters
    threshold = float(request.form.get('threshold', 0.75))
    start_frame = int(request.form.get('start_frame', 0))
    end_frame = request.form.get('end_frame')
    if end_frame:
        end_frame = int(end_frame)
    
    # Start processing in background
    task_id = f"task_{len(processing_status)}"
    processing_status[task_id] = {
        'status': 'processing',
        'progress': 0,
        'message': 'Starting video analysis...'
    }
    
    thread = threading.Thread(
        target=process_video,
        args=(task_id, filepath, threshold, start_frame, end_frame)
    )
    thread.start()
    
    return jsonify({
        'task_id': task_id,
        'message': 'Processing started'
    })

def process_video(task_id, video_path, threshold, start_frame, end_frame):
    """Process video in background thread."""
    try:
        processing_status[task_id]['message'] = 'Generating descriptions...'
        
        descriptions, timestamps = generate_description(
            video_path=video_path,
            start_frame=start_frame,
            end_frame=end_frame,
            threshold=threshold
        )
        
        # Save results
        output_data = []
        for desc, timestamp in zip(descriptions, timestamps):
            output_data.append({
                'timestamp': timestamp,
                'description': desc.content if hasattr(desc, 'content') else str(desc)
            })
        
        output_file = os.path.join(app.config['OUTPUT_FOLDER'], f"{task_id}_descriptions.json")
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        processing_status[task_id] = {
            'status': 'completed',
            'progress': 100,
            'message': f'Generated {len(descriptions)} descriptions',
            'output_file': output_file,
            'descriptions': output_data
        }
        
    except Exception as e:
        processing_status[task_id] = {
            'status': 'error',
            'message': f'Error: {str(e)}'
        }

@app.route('/status/<task_id>')
def get_status(task_id):
    if task_id not in processing_status:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(processing_status[task_id])

@app.route('/download/<task_id>')
def download_results(task_id):
    if task_id not in processing_status:
        return jsonify({'error': 'Task not found'}), 404
    
    task = processing_status[task_id]
    if task['status'] != 'completed':
        return jsonify({'error': 'Task not completed'}), 400
    
    return send_file(
        task['output_file'],
        as_attachment=True,
        download_name=f"descriptions_{task_id}.json"
    )

@app.route('/api/descriptions/<task_id>')
def get_descriptions(task_id):
    if task_id not in processing_status:
        return jsonify({'error': 'Task not found'}), 404
    
    task = processing_status[task_id]
    if task['status'] != 'completed':
        return jsonify({'error': 'Task not completed'}), 400
    
    return jsonify(task['descriptions'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 