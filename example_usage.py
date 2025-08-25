"""
Example script showing how to use the Audio to MIDI Backend API
Created by Sergie Code
"""

import requests
import os
import sys

def test_health():
    """Test the health endpoint."""
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running on http://localhost:5000")
        return False

def get_supported_formats():
    """Get supported audio formats."""
    try:
        response = requests.get('http://localhost:5000/supported_formats')
        if response.status_code == 200:
            data = response.json()
            print(f"📝 Supported formats: {', '.join(data['supported_formats'])}")
            print(f"📏 Max file size: {data['max_file_size_mb']}MB")
            return True
        else:
            print(f"❌ Failed to get formats: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False

def transcribe_audio(audio_file_path, output_path=None):
    """Transcribe an audio file to MIDI."""
    if not os.path.exists(audio_file_path):
        print(f"❌ Audio file not found: {audio_file_path}")
        return False
    
    if output_path is None:
        base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
        output_path = f"{base_name}_transcribed.mid"
    
    print(f"🎵 Transcribing: {audio_file_path}")
    
    try:
        with open(audio_file_path, 'rb') as f:
            files = {'audio_file': f}
            response = requests.post('http://localhost:5000/transcribe', files=files)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as midi_file:
                midi_file.write(response.content)
            print(f"✅ MIDI file saved: {output_path}")
            print(f"📊 File size: {len(response.content)} bytes")
            return True
        else:
            try:
                error_data = response.json()
                print(f"❌ Transcription failed: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"❌ Transcription failed with status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {audio_file_path}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main function to demonstrate API usage."""
    print("🎵 Audio to MIDI Backend - API Test Script")
    print("Created by Sergie Code\n")
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    if not test_health():
        sys.exit(1)
    print()
    
    # Test 2: Get supported formats
    print("2. Getting supported formats...")
    if not get_supported_formats():
        sys.exit(1)
    print()
    
    # Test 3: Transcribe audio (if file provided)
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        print("3. Transcribing audio file...")
        if transcribe_audio(audio_file, output_file):
            print("🎉 All tests passed!")
        else:
            print("❌ Transcription test failed")
            sys.exit(1)
    else:
        print("3. Skipping transcription test (no audio file provided)")
        print("   Usage: python example_usage.py <audio_file> [output_file]")
        print("   Example: python example_usage.py sample.wav output.mid")
    
    print("\n✨ API testing complete!")

if __name__ == "__main__":
    main()
