"""
Quick Test Script for Audio to MIDI Backend
Created by Sergie Code

This script performs basic functionality tests.
"""

import requests
import json
import os
import tempfile
import wave
import numpy as np

def create_test_audio():
    """Create a simple test audio file."""
    print("🎵 Creating test audio file...")
    
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
    temp_file.close()
    
    with wave.open(temp_file.name, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    print(f"✅ Created test audio: {temp_file.name}")
    return temp_file.name

def test_health():
    """Test the health endpoint."""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   Service: {data['service']}")
            print(f"   Timestamp: {data['timestamp']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running on http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_supported_formats():
    """Test the supported formats endpoint."""
    print("📝 Testing supported formats endpoint...")
    try:
        response = requests.get('http://localhost:5000/supported_formats', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Supported formats: {', '.join(data['supported_formats'])}")
            print(f"   Max file size: {data['max_file_size_mb']}MB")
            return True
        else:
            print(f"❌ Failed to get formats: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Formats test error: {str(e)}")
        return False

def test_transcription():
    """Test the transcription endpoint with a simple audio file."""
    print("🎼 Testing transcription endpoint...")
    
    # Create test audio file
    audio_file = create_test_audio()
    
    try:
        print("   Uploading audio file for transcription...")
        with open(audio_file, 'rb') as f:
            files = {'audio_file': f}
            response = requests.post('http://localhost:5000/transcribe', files=files, timeout=30)
        
        if response.status_code == 200:
            # Save the MIDI file
            output_file = "test_output.mid"
            with open(output_file, 'wb') as midi_file:
                midi_file.write(response.content)
            print(f"✅ Transcription successful!")
            print(f"   MIDI file saved: {output_file}")
            print(f"   File size: {len(response.content)} bytes")
            
            # Check if it's a valid MIDI file
            if len(response.content) > 0 and response.content[:4] == b'MThd':
                print("✅ Valid MIDI file header detected")
            else:
                print("⚠️ MIDI file header not detected (but file was created)")
            
            return True
        else:
            try:
                error_data = response.json()
                print(f"❌ Transcription failed: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"❌ Transcription failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Transcription test error: {str(e)}")
        return False
    finally:
        # Cleanup
        try:
            os.unlink(audio_file)
        except:
            pass

def main():
    """Run all tests."""
    print("🎵 Audio to MIDI Backend - Quick Test")
    print("Created by Sergie Code\n")
    
    tests = [
        ("Health Check", test_health),
        ("Supported Formats", test_supported_formats),
        ("Audio Transcription", test_transcription)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print('='*60)
        
        if test_func():
            passed += 1
        
        print()
    
    print("="*60)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Audio to MIDI Backend is working correctly!")
        print("\n📋 Next steps:")
        print("   • Open http://localhost:5000/health in your browser")
        print("   • Use Postman or similar tool to test file uploads")
        print("   • Build a frontend application")
        print("   • Integrate real ML models")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    print("\n✨ Testing complete!")

if __name__ == "__main__":
    main()
