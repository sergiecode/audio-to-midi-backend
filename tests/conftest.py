"""
Test Configuration
Created by Sergie Code
"""

import os
import sys
import pytest
import tempfile

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def app():
    """Create test Flask app."""
    # Import here to avoid circular imports
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from app import app as flask_app
    
    flask_app.config['TESTING'] = True
    flask_app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
    flask_app.config['OUTPUT_FOLDER'] = tempfile.mkdtemp()
    
    return flask_app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def test_audio_file():
    """Create a temporary test audio file."""
    import wave
    import numpy as np
    
    # Create a simple sine wave WAV file
    sample_rate = 44100
    duration = 2  # seconds
    frequency = 440  # A4 note
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_data = np.sin(2 * np.pi * frequency * t)
    
    # Convert to 16-bit integers
    wave_data = (wave_data * 32767).astype(np.int16)
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_file.close()  # Close file handle on Windows
    
    with wave.open(temp_file.name, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    yield temp_file.name
    
    # Cleanup - with better error handling for Windows
    try:
        os.unlink(temp_file.name)
    except (OSError, PermissionError):
        pass  # File might be in use, skip cleanup
