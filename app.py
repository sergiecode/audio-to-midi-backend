"""
Audio to MIDI Backend Service
Created by Sergie Code

A Flask-based backend service that converts audio recordings (WAV/MP3) 
into MIDI files using machine learning transcription models.
"""

import os
import logging
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from src.transcription.transcriber import AudioTranscriber
from datetime import datetime, timezone
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'm4a'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_directories():
    """Ensure upload and output directories exist."""
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'audio-to-midi-backend',
        'timestamp': datetime.now(timezone.utc).isoformat()
    }), 200

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Transcribe audio file to MIDI.
    
    Accepts: multipart/form-data with 'audio_file' field
    Returns: MIDI file or error message
    """
    try:
        # Check if file was uploaded
        if 'audio_file' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio_file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'File type not supported. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        audio_filename = f"{file_id}.{file_extension}"
        midi_filename = f"{file_id}.mid"
        
        # Save uploaded file
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        file.save(audio_path)
        
        logger.info(f"Audio file saved: {audio_path}")
        
        # Initialize transcriber and convert to MIDI
        transcriber = AudioTranscriber()
        midi_path = os.path.join(app.config['OUTPUT_FOLDER'], midi_filename)
        
        success = transcriber.transcribe(audio_path, midi_path)
        
        if not success:
            # Clean up uploaded file
            if os.path.exists(audio_path):
                os.remove(audio_path)
            return jsonify({'error': 'Transcription failed'}), 500
        
        # Clean up uploaded file
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        logger.info(f"MIDI file generated: {midi_path}")
        
        # Return MIDI file
        return send_file(
            midi_path,
            as_attachment=True,
            download_name=f"{original_filename.rsplit('.', 1)[0]}.mid",
            mimetype='audio/midi'
        )
        
    except RequestEntityTooLarge:
        return jsonify({'error': 'File too large. Maximum size is 50MB'}), 413
    except Exception as e:
        logger.error(f"Error in transcribe_audio: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/supported_formats', methods=['GET'])
def get_supported_formats():
    """Get list of supported audio formats."""
    return jsonify({
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'max_file_size_mb': 50
    }), 200

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({'error': 'File too large. Maximum size is 50MB'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle not found error."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server error."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    ensure_directories()
    logger.info("Starting Audio to MIDI Backend Service")
    logger.info("Created by Sergie Code - AI Tools for Musicians")
    app.run(debug=True, host='0.0.0.0', port=5000)
