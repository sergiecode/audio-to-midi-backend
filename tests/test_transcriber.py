"""
Test Transcription Module
Created by Sergie Code
"""

import os
import tempfile
import pytest
from src.transcription.transcriber import AudioTranscriber


class TestAudioTranscriber:
    """Test cases for AudioTranscriber class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.transcriber = AudioTranscriber()
        self.temp_dir = tempfile.mkdtemp()
    
    def test_transcriber_initialization(self):
        """Test transcriber initialization."""
        assert self.transcriber.sample_rate == 16000
    
    def test_load_audio_nonexistent_file(self):
        """Test loading a non-existent audio file."""
        result = self.transcriber.load_audio('nonexistent.wav')
        assert result is None
    
    def test_analyze_audio_empty_data(self):
        """Test analyzing empty audio data."""
        import numpy as np
        empty_audio = np.array([])
        result = self.transcriber.analyze_audio(empty_audio)
        
        assert result is not None
        assert result['duration'] == 0.0
        assert result['samples'] == 0
    
    def test_create_midi_from_analysis(self):
        """Test creating MIDI from analysis features."""
        features = {
            'duration': 4.0,
            'sample_rate': 16000,
            'samples': 64000
        }
        
        output_path = os.path.join(self.temp_dir, 'test.mid')
        success = self.transcriber.create_midi_from_analysis(features, output_path)
        
        assert success is True
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_create_midi_invalid_path(self):
        """Test creating MIDI with invalid output path."""
        features = {'duration': 4.0}
        invalid_path = '/invalid/path/test.mid'
        
        success = self.transcriber.create_midi_from_analysis(features, invalid_path)
        assert success is False
    
    def test_transcribe_nonexistent_file(self):
        """Test transcribing a non-existent audio file."""
        output_path = os.path.join(self.temp_dir, 'output.mid')
        success = self.transcriber.transcribe('nonexistent.wav', output_path)
        assert success is False
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
