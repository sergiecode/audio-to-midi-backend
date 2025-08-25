"""
Test API Endpoints
Created by Sergie Code
"""

import json
import io


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'audio-to-midi-backend'
    assert 'timestamp' in data


def test_supported_formats_endpoint(client):
    """Test the supported formats endpoint."""
    response = client.get('/supported_formats')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'supported_formats' in data
    assert 'wav' in data['supported_formats']
    assert 'mp3' in data['supported_formats']
    assert data['max_file_size_mb'] == 50


def test_transcribe_no_file(client):
    """Test transcribe endpoint with no file."""
    response = client.post('/transcribe')
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert 'error' in data
    assert 'No audio file provided' in data['error']


def test_transcribe_empty_filename(client):
    """Test transcribe endpoint with empty filename."""
    data = {'audio_file': (io.BytesIO(b''), '')}
    response = client.post('/transcribe', data=data)
    assert response.status_code == 400
    
    response_data = json.loads(response.data)
    assert 'error' in response_data
    assert 'No file selected' in response_data['error']


def test_transcribe_invalid_file_type(client):
    """Test transcribe endpoint with invalid file type."""
    data = {'audio_file': (io.BytesIO(b'test data'), 'test.txt')}
    response = client.post('/transcribe', data=data)
    assert response.status_code == 400
    
    response_data = json.loads(response.data)
    assert 'error' in response_data
    assert 'File type not supported' in response_data['error']


def test_transcribe_valid_file(client, test_audio_file):
    """Test transcribe endpoint with valid audio file."""
    with open(test_audio_file, 'rb') as f:
        data = {'audio_file': (f, 'test.wav')}
        response = client.post('/transcribe', data=data)
    
    # Should return a MIDI file
    assert response.status_code == 200
    assert 'audio/midi' in response.headers['Content-Type']
    
    # Check that response contains MIDI data
    assert len(response.data) > 0


def test_404_endpoint(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['error'] == 'Endpoint not found'
