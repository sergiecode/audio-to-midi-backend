"""
Generate sample audio files for testing
Created by Sergie Code
"""

import numpy as np
import wave
import os

def generate_test_audio(filename="test_audio.wav", duration=3, frequency=440, sample_rate=44100):
    """
    Generate a simple sine wave audio file for testing.
    
    Args:
        filename (str): Output filename
        duration (float): Duration in seconds
        frequency (float): Frequency in Hz (440 = A4 note)
        sample_rate (int): Sample rate in Hz
    """
    print(f"🎵 Generating test audio: {filename}")
    print(f"   Duration: {duration}s, Frequency: {frequency}Hz, Sample Rate: {sample_rate}Hz")
    
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate sine wave
    wave_data = np.sin(2 * np.pi * frequency * t)
    
    # Add some harmonics to make it more interesting
    wave_data += 0.3 * np.sin(2 * np.pi * frequency * 2 * t)  # Octave
    wave_data += 0.2 * np.sin(2 * np.pi * frequency * 3 * t)  # Fifth
    
    # Apply envelope to avoid clicks
    envelope = np.ones_like(wave_data)
    fade_samples = int(0.1 * sample_rate)  # 0.1 second fade
    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
    wave_data *= envelope
    
    # Normalize and convert to 16-bit integers
    wave_data = wave_data / np.max(np.abs(wave_data))
    wave_data = (wave_data * 32767).astype(np.int16)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    print(f"✅ Generated {filename} ({os.path.getsize(filename)} bytes)")

def generate_chord_progression(filename="chord_progression.wav", duration=8, sample_rate=44100):
    """
    Generate a simple chord progression for testing.
    
    Args:
        filename (str): Output filename
        duration (float): Duration in seconds
        sample_rate (int): Sample rate in Hz
    """
    print(f"🎵 Generating chord progression: {filename}")
    
    # C major chord progression: C - Am - F - G
    chords = [
        [261.63, 329.63, 392.00],  # C major (C-E-G)
        [220.00, 261.63, 329.63],  # A minor (A-C-E)
        [174.61, 220.00, 261.63],  # F major (F-A-C)
        [196.00, 246.94, 293.66],  # G major (G-B-D)
    ]
    
    chord_duration = duration / len(chords)
    t_chord = np.linspace(0, chord_duration, int(sample_rate * chord_duration), False)
    
    full_audio = np.array([])
    
    for i, chord in enumerate(chords):
        print(f"   Chord {i+1}: {len(chord)} notes")
        
        # Generate chord
        chord_audio = np.zeros_like(t_chord)
        for frequency in chord:
            chord_audio += np.sin(2 * np.pi * frequency * t_chord)
        
        # Normalize chord
        chord_audio = chord_audio / len(chord)
        
        # Add envelope
        envelope = np.ones_like(chord_audio)
        fade_samples = int(0.05 * sample_rate)  # 0.05 second fade
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        chord_audio *= envelope
        
        full_audio = np.concatenate([full_audio, chord_audio])
    
    # Normalize and convert to 16-bit integers
    full_audio = full_audio / np.max(np.abs(full_audio))
    full_audio = (full_audio * 32767).astype(np.int16)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(full_audio.tobytes())
    
    print(f"✅ Generated {filename} ({os.path.getsize(filename)} bytes)")

def main():
    """Generate test audio files."""
    print("🎵 Audio to MIDI Backend - Test Audio Generator")
    print("Created by Sergie Code\n")
    
    # Create test directory
    test_dir = "test_audio"
    os.makedirs(test_dir, exist_ok=True)
    
    # Generate different test files
    test_files = [
        ("simple_note.wav", 2, 440),     # A4 note
        ("high_note.wav", 2, 880),       # A5 note
        ("low_note.wav", 2, 220),        # A3 note
        ("long_note.wav", 5, 523.25),    # C5 note
    ]
    
    for filename, duration, frequency in test_files:
        filepath = os.path.join(test_dir, filename)
        generate_test_audio(filepath, duration, frequency)
    
    # Generate chord progression
    chord_file = os.path.join(test_dir, "chord_progression.wav")
    generate_chord_progression(chord_file)
    
    print(f"\n✅ All test files generated in '{test_dir}' directory!")
    print("\n📋 You can now test the API with these files:")
    print(f"   python example_usage.py {test_dir}/simple_note.wav")
    print(f"   python example_usage.py {test_dir}/chord_progression.wav")

if __name__ == "__main__":
    main()
