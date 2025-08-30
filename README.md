# 🎵 Audio to MIDI Backend

**Created by Sergie Code - AI Tools for Musicians**

A powerful Flask-based backend service that converts audio recordings (WAV/MP3) into MIDI files using machine learning transcription models. This project serves as a foundation for building AI-powered music tools and can be easily integrated into frontend applications or used as a standalone service.

## 🚀 Features

- **Audio Format Support**: WAV, MP3, FLAC, M4A
- **RESTful API**: Clean and simple endpoints for audio transcription
- **Machine Learning Ready**: Built to integrate with models like Magenta's Onsets and Frames
- **Production Ready**: Includes error handling, logging, and file validation
- **Test Coverage**: Comprehensive test suite included
- **Scalable Architecture**: Modular design for easy extension

## 🎯 How It Works

The audio-to-midi conversion follows this workflow:

1. **Upload Audio** → Client uploads an audio file via the `/transcribe` endpoint
2. **Audio Processing** → The system loads and preprocesses the audio using librosa
3. **ML Analysis** → Audio is analyzed to extract musical features (notes, timing, velocity)
4. **MIDI Generation** → A MIDI file is created from the extracted features using pretty_midi
5. **Download MIDI** → The generated MIDI file is returned to the client

```
Audio File → Audio Processing → ML Analysis → MIDI Generation → MIDI File
    ↓              ↓               ↓              ↓            ↓
   WAV/MP3      Librosa      AI Model       pretty_midi    Download
```

*Note: The current implementation includes a placeholder transcription model that generates a simple C major scale for testing purposes. This can be replaced with actual ML models like Magenta's Onsets and Frames.*

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/audio-to-midi-backend.git
cd audio-to-midi-backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

## 📡 API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
    "status": "healthy",
    "service": "audio-to-midi-backend",
    "timestamp": "2024-01-01T12:00:00"
}
```

### Get Supported Formats
```http
GET /supported_formats
```

**Response:**
```json
{
    "supported_formats": ["wav", "mp3", "flac", "m4a"],
    "max_file_size_mb": 50
}
```

### Transcribe Audio to MIDI
```http
POST /transcribe
Content-Type: multipart/form-data
```

**Request:**
- `audio_file`: Audio file (WAV, MP3, FLAC, M4A)

**Response:**
- Success: MIDI file download
- Error: JSON with error message

## 🧪 Testing the API

### Using cURL

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test audio transcription
curl -X POST \
  -F "audio_file=@path/to/your/audio.wav" \
  http://localhost:5000/transcribe \
  --output result.mid
```

### Using Python

```python
import requests

# Upload and transcribe audio file
with open('audio.wav', 'rb') as f:
    files = {'audio_file': f}
    response = requests.post('http://localhost:5000/transcribe', files=files)
    
    if response.status_code == 200:
        with open('output.mid', 'wb') as midi_file:
            midi_file.write(response.content)
        print("MIDI file saved as output.mid")
    else:
        print(f"Error: {response.json()}")
```

### Using Postman

1. Open Postman
2. Create a new POST request to `http://localhost:5000/transcribe`
3. Go to Body → form-data
4. Add key `audio_file` with type `File`
5. Select your audio file and send the request

## 🔧 Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_api.py
```

### Code Formatting

```bash
# Format code with black
black .

# Lint with flake8
flake8 src/ tests/
```

### Project Structure

```
audio-to-midi-backend/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                      # This file
├── src/                           # Source code
│   ├── __init__.py
│   └── transcription/             # Transcription logic
│       ├── __init__.py
│       └── transcriber.py         # Main transcription module
├── tests/                         # Test suite
│   ├── conftest.py               # Test configuration
│   ├── test_api.py               # API endpoint tests
│   └── test_transcriber.py       # Transcription logic tests
├── uploads/                       # Temporary upload directory
└── output/                        # Generated MIDI files
```

## 🤖 Integrating Real ML Models

The current implementation uses a placeholder transcription model. To integrate real ML models:

### Option 1: Magenta's Onsets and Frames

```python
# In src/transcription/transcriber.py
import magenta.models.onsets_frames_transcription.infer_util as infer_util

def analyze_audio_with_magenta(self, audio_data):
    # Load pre-trained model
    model_dir = 'path/to/onsets_frames_model'
    # Implement Magenta integration
    pass
```

### Option 2: Custom TensorFlow Model

```python
import tensorflow as tf

def load_custom_model(self):
    self.model = tf.keras.models.load_model('path/to/your/model')

def predict_notes(self, audio_features):
    predictions = self.model.predict(audio_features)
    return self.convert_predictions_to_midi(predictions)
```

## 🌐 Frontend Integration Ideas

This backend can power various frontend applications:

### Web Applications
- **React/Vue.js**: Upload interface with drag-and-drop
- **Next.js**: Full-stack music transcription app
- **Streamlit**: Quick prototyping and demos

### Mobile Applications
- **React Native**: Cross-platform mobile app
- **Flutter**: Native mobile experience
- **Progressive Web App**: Mobile-first web experience

### Desktop Applications
- **Electron**: Cross-platform desktop app
- **Tkinter/PyQt**: Python-based desktop interface
- **Tauri**: Rust-based lightweight desktop app

### Example Frontend Integration

```javascript
// React component example
const AudioTranscriber = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTranscribe = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('audio_file', file);
    
    try {
      const response = await fetch('/transcribe', {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        const blob = await response.blob();
        // Handle MIDI file download
        downloadMIDI(blob);
      }
    } catch (error) {
      console.error('Transcription failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleTranscribe} disabled={!file || loading}>
        {loading ? 'Transcribing...' : 'Convert to MIDI'}
      </button>
    </div>
  );
};
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Environment Variables
```bash
export FLASK_ENV=production
export UPLOAD_FOLDER=/path/to/uploads
export OUTPUT_FOLDER=/path/to/output
export MAX_FILE_SIZE_MB=50
```

## 📈 Performance Considerations

- **File Size Limits**: Currently set to 50MB per file
- **Concurrent Requests**: Use Gunicorn with multiple workers for production
- **Audio Processing**: Consider chunking large files for better memory management
- **MIDI Storage**: Implement cleanup for temporary files
- **Caching**: Add Redis for caching transcription results

## 🛣️ Roadmap

- [ ] **Real ML Integration**: Implement Magenta's Onsets and Frames
- [ ] **Polyphonic Support**: Handle multiple simultaneous notes
- [ ] **Drum Transcription**: Support for percussion instruments
- [ ] **Real-time Processing**: WebSocket support for live transcription
- [ ] **Audio Effects**: Preprocessing options (noise reduction, normalization)
- [ ] **Multiple Formats**: Support for more audio and MIDI formats
- [ ] **Batch Processing**: Handle multiple files simultaneously
- [ ] **User Authentication**: API key management and rate limiting
- [ ] **Cloud Integration**: AWS/GCP deployment templates
- [ ] **Monitoring**: Health checks and performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 👨‍💻 About the Creator

**Sergie Code** is a software engineer passionate about creating AI tools for musicians. Through YouTube tutorials and open-source projects, Sergie helps developers build innovative music technology solutions.

- 📸 Instagram: https://www.instagram.com/sergiecode

- 🧑🏼‍💻 LinkedIn: https://www.linkedin.com/in/sergiecode/

- 📽️Youtube: https://www.youtube.com/@SergieCode

- 😺 Github: https://github.com/sergiecode

- 👤 Facebook: https://www.facebook.com/sergiecodeok

- 🎞️ Tiktok: https://www.tiktok.com/@sergiecode

- 🕊️Twitter: https://twitter.com/sergiecode

- 🧵Threads: https://www.threads.net/@sergiecode

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-username/audio-to-midi-backend/issues) page
2. Create a new issue with detailed information
3. Join the discussion in the community forum
4. Watch Sergie Code's YouTube tutorials for walkthroughs

## 🙏 Acknowledgments

- **Magenta Team** for pioneering music AI research
- **Flask Community** for the excellent web framework
- **Pretty MIDI** developers for MIDI file handling
- **Librosa** team for audio processing tools
- **TensorFlow** team for machine learning infrastructure

---

**Made with ❤️ by Sergie Code for the music and developer community**

*Transform audio into MIDI with the power of AI! 🎵→🎹*

