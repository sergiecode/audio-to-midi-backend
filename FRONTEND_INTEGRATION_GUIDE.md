# 🎵 Audio to MIDI Backend - Integration Guide for Frontend Development

**Created by Sergie Code - AI Tools for Musicians**  
**Repository**: `audio-to-midi-backend`  
**Purpose**: Backend API integration guide for `audio-to-midi-frontend`

## 📋 Overview

This document provides comprehensive instructions for integrating with the `audio-to-midi-backend` API to create a web application that visualizes MIDI files and automatically generates sheet music using VexFlow or ABCJS.

## 🏗️ Backend Architecture

### Base URL
```
http://localhost:5000
```

### Core Functionality
The backend provides audio-to-MIDI transcription services with a RESTful API interface.

## 🔌 API Endpoints Reference

### 1. Health Check
**Endpoint**: `GET /health`
**Purpose**: Check if the backend service is running
**Response**:
```json
{
  "status": "healthy",
  "service": "audio-to-midi-backend",
  "timestamp": "2025-08-25T12:00:00.000Z"
}
```

**Frontend Integration**:
```javascript
// Check backend availability
const checkBackendHealth = async () => {
  try {
    const response = await fetch('http://localhost:5000/health');
    const data = await response.json();
    return data.status === 'healthy';
  } catch (error) {
    console.error('Backend unavailable:', error);
    return false;
  }
};
```

### 2. Supported Audio Formats
**Endpoint**: `GET /supported_formats`
**Purpose**: Get list of supported audio file formats
**Response**:
```json
{
  "supported_formats": ["wav", "mp3", "flac", "m4a"],
  "max_file_size_mb": 50
}
```

**Frontend Integration**:
```javascript
// Get supported formats for file validation
const getSupportedFormats = async () => {
  const response = await fetch('http://localhost:5000/supported_formats');
  const data = await response.json();
  return data;
};

// File validation example
const isValidAudioFile = (file, supportedFormats) => {
  const extension = file.name.split('.').pop().toLowerCase();
  return supportedFormats.includes(extension);
};
```

### 3. Audio to MIDI Transcription
**Endpoint**: `POST /transcribe`
**Content-Type**: `multipart/form-data`
**Purpose**: Convert audio file to MIDI
**Request**:
```javascript
const formData = new FormData();
formData.append('audio_file', audioFile);
```

**Response**: Binary MIDI file (`.mid`)
**Content-Type**: `audio/midi`

**Frontend Integration**:
```javascript
// Complete transcription workflow
const transcribeAudio = async (audioFile) => {
  try {
    const formData = new FormData();
    formData.append('audio_file', audioFile);
    
    const response = await fetch('http://localhost:5000/transcribe', {
      method: 'POST',
      body: formData
    });
    
    if (response.ok) {
      const midiBlob = await response.blob();
      return {
        success: true,
        midiFile: midiBlob,
        filename: `${audioFile.name.split('.')[0]}.mid`
      };
    } else {
      const error = await response.json();
      return { success: false, error: error.error };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

## 🎼 MIDI File Processing for Frontend

### Converting MIDI Blob to Useful Formats

#### For VexFlow Integration:
```javascript
// Convert MIDI blob to array buffer for processing
const processMidiForVexFlow = async (midiBlob) => {
  const arrayBuffer = await midiBlob.arrayBuffer();
  const midiArray = new Uint8Array(arrayBuffer);
  
  // Use a MIDI parser library (like @tonejs/midi or midi-parser-js)
  // to convert to VexFlow format
  const midi = new Midi(midiArray);
  
  // Convert to VexFlow notation format
  const notes = [];
  midi.tracks.forEach(track => {
    track.notes.forEach(note => {
      notes.push({
        keys: [note.name + note.octave],
        duration: 'q', // Quarter note (adjust based on note duration)
        pitch: note.midi
      });
    });
  });
  
  return notes;
};
```

#### For ABCJS Integration:
```javascript
// Convert MIDI to ABC notation
const processMidiForABCJS = async (midiBlob) => {
  const arrayBuffer = await midiBlob.arrayBuffer();
  const midiArray = new Uint8Array(arrayBuffer);
  
  // Parse MIDI and convert to ABC notation string
  const midi = new Midi(midiArray);
  
  let abcNotation = 'X:1\nT:Transcribed Audio\nM:4/4\nL:1/4\nK:C\n';
  
  midi.tracks.forEach(track => {
    track.notes.forEach(note => {
      // Convert note to ABC format (simplified example)
      const abcNote = convertMidiNoteToABC(note);
      abcNotation += abcNote + ' ';
    });
  });
  
  return abcNotation;
};
```

## 🚀 Frontend Implementation Recommendations

### 1. Technology Stack
- **Framework**: React, Vue.js, or Vanilla JavaScript
- **Music Notation**: VexFlow or ABCJS
- **MIDI Processing**: @tonejs/midi, midi-parser-js, or MidiPlayerJS
- **File Handling**: HTML5 File API
- **UI Components**: Material-UI, Tailwind CSS, or custom CSS

### 2. Core Components Structure

#### Main Application Component
```javascript
// React example
const AudioToMidiApp = () => {
  const [backendHealth, setBackendHealth] = useState(false);
  const [audioFile, setAudioFile] = useState(null);
  const [midiData, setMidiData] = useState(null);
  const [isTranscribing, setIsTranscribing] = useState(false);
  
  useEffect(() => {
    checkBackendHealth().then(setBackendHealth);
  }, []);
  
  const handleFileUpload = async (file) => {
    setIsTranscribing(true);
    const result = await transcribeAudio(file);
    
    if (result.success) {
      const processedMidi = await processMidiForVexFlow(result.midiFile);
      setMidiData(processedMidi);
    }
    
    setIsTranscribing(false);
  };
  
  return (
    <div className="app">
      <StatusIndicator healthy={backendHealth} />
      <FileUploader onUpload={handleFileUpload} />
      {isTranscribing && <LoadingIndicator />}
      {midiData && <SheetMusicViewer data={midiData} />}
    </div>
  );
};
```

#### File Upload Component
```javascript
const FileUploader = ({ onUpload }) => {
  const [supportedFormats, setSupportedFormats] = useState([]);
  
  useEffect(() => {
    getSupportedFormats().then(data => {
      setSupportedFormats(data.supported_formats);
    });
  }, []);
  
  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && isValidAudioFile(file, supportedFormats)) {
      onUpload(file);
    } else {
      alert('Please select a valid audio file');
    }
  };
  
  return (
    <div className="file-uploader">
      <input
        type="file"
        accept={supportedFormats.map(format => `.${format}`).join(',')}
        onChange={handleFileSelect}
      />
      <p>Supported formats: {supportedFormats.join(', ')}</p>
    </div>
  );
};
```

#### Sheet Music Viewer Component
```javascript
const SheetMusicViewer = ({ data }) => {
  const containerRef = useRef();
  
  useEffect(() => {
    if (data && containerRef.current) {
      renderSheetMusic(data, containerRef.current);
    }
  }, [data]);
  
  const renderSheetMusic = (midiData, container) => {
    // VexFlow implementation
    const vf = new Vex.Flow.Factory({
      renderer: { elementId: container.id, width: 800, height: 400 }
    });
    
    const score = vf.EasyScore();
    const system = vf.System();
    
    // Convert MIDI data to VexFlow notation
    midiData.forEach(note => {
      system.addStave({ voices: [score.voice(score.notes(note.keys[0]))] });
    });
    
    vf.draw();
  };
  
  return <div ref={containerRef} id="sheet-music-container" />;
};
```

### 3. Error Handling Strategy

```javascript
// Comprehensive error handling
const handleTranscriptionError = (error) => {
  const errorMessages = {
    'File too large': 'Please select a smaller audio file (max 50MB)',
    'File type not supported': 'Please use WAV, MP3, FLAC, or M4A files',
    'Internal server error': 'Transcription service unavailable. Please try again.',
    'No audio file provided': 'Please select an audio file first'
  };
  
  const userMessage = errorMessages[error] || 'An unexpected error occurred';
  
  // Display user-friendly error message
  showNotification(userMessage, 'error');
  
  // Log technical details for debugging
  console.error('Transcription error:', error);
};
```

### 4. User Experience Enhancements

#### Progress Indicators
```javascript
const TranscriptionProgress = ({ isActive }) => {
  const steps = [
    'Uploading audio file',
    'Analyzing audio content',
    'Generating MIDI data',
    'Rendering sheet music'
  ];
  
  const [currentStep, setCurrentStep] = useState(0);
  
  useEffect(() => {
    if (isActive) {
      const interval = setInterval(() => {
        setCurrentStep(prev => (prev + 1) % steps.length);
      }, 2000);
      
      return () => clearInterval(interval);
    }
  }, [isActive]);
  
  return (
    <div className="progress-indicator">
      {steps.map((step, index) => (
        <div
          key={step}
          className={`step ${index <= currentStep ? 'active' : ''}`}
        >
          {step}
        </div>
      ))}
    </div>
  );
};
```

#### Real-time Backend Status
```javascript
const BackendStatusMonitor = () => {
  const [status, setStatus] = useState('checking');
  
  useEffect(() => {
    const checkStatus = async () => {
      const isHealthy = await checkBackendHealth();
      setStatus(isHealthy ? 'online' : 'offline');
    };
    
    checkStatus();
    const interval = setInterval(checkStatus, 30000); // Check every 30 seconds
    
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div className={`status-indicator ${status}`}>
      Backend: {status}
    </div>
  );
};
```

## 🔧 Development Setup Integration

### Environment Variables
```javascript
// Frontend configuration
const config = {
  BACKEND_URL: process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000',
  MAX_FILE_SIZE: 50 * 1024 * 1024, // 50MB
  SUPPORTED_FORMATS: ['wav', 'mp3', 'flac', 'm4a'],
  POLLING_INTERVAL: 30000 // 30 seconds
};
```

### CORS Configuration
The backend already handles CORS, but ensure your frontend requests include proper headers:

```javascript
const apiRequest = async (endpoint, options = {}) => {
  const response = await fetch(`${config.BACKEND_URL}${endpoint}`, {
    ...options,
    headers: {
      ...options.headers,
      // Add any required headers
    }
  });
  
  return response;
};
```

## 📱 Mobile Responsiveness Considerations

### File Upload on Mobile
```javascript
const MobileFileUploader = () => {
  return (
    <div className="mobile-uploader">
      <input
        type="file"
        accept="audio/*"
        capture="microphone" // Allows direct recording on mobile
        onChange={handleFileUpload}
      />
      <button onClick={startRecording}>
        Record Audio Directly
      </button>
    </div>
  );
};
```

### Touch-friendly Sheet Music Viewer
```javascript
const TouchSheetMusicViewer = ({ data }) => {
  const [zoom, setZoom] = useState(1);
  
  const handlePinchZoom = (event) => {
    // Implement pinch-to-zoom for mobile
    setZoom(prevZoom => Math.max(0.5, Math.min(3, prevZoom * event.scale)));
  };
  
  return (
    <div
      className="sheet-music-viewer"
      style={{ transform: `scale(${zoom})` }}
      onTouchStart={handlePinchZoom}
    >
      {/* Sheet music content */}
    </div>
  );
};
```

## 🧪 Testing Integration

### API Testing
```javascript
// Test backend connectivity
describe('Backend Integration', () => {
  test('health endpoint responds correctly', async () => {
    const isHealthy = await checkBackendHealth();
    expect(isHealthy).toBe(true);
  });
  
  test('transcription endpoint accepts valid files', async () => {
    const mockFile = new File([''], 'test.wav', { type: 'audio/wav' });
    const result = await transcribeAudio(mockFile);
    expect(result.success).toBeDefined();
  });
});
```

### MIDI Processing Testing
```javascript
// Test MIDI data processing
describe('MIDI Processing', () => {
  test('converts MIDI blob to VexFlow format', async () => {
    const mockMidiBlob = new Blob([/* mock MIDI data */]);
    const vexFlowData = await processMidiForVexFlow(mockMidiBlob);
    expect(vexFlowData).toHaveProperty('notes');
  });
});
```

## 🚀 Deployment Configuration

### Production Backend URL
```javascript
// Update for production deployment
const config = {
  BACKEND_URL: process.env.NODE_ENV === 'production'
    ? 'https://your-backend-domain.com'
    : 'http://localhost:5000'
};
```

### Build Optimization
```json
{
  "scripts": {
    "build": "react-scripts build",
    "build:analyze": "npm run build && npx webpack-bundle-analyzer build/static/js/*.js"
  }
}
```

## 📚 Required Dependencies

### Core Dependencies
```json
{
  "dependencies": {
    "@tonejs/midi": "^2.0.28",
    "vexflow": "^4.0.3",
    "abcjs": "^6.2.3",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^5.16.5"
  }
}
```

### Optional Enhancements
```json
{
  "dependencies": {
    "midi-player-js": "^2.0.14",
    "web-audio-api": "^0.2.2",
    "react-dropzone": "^14.2.3",
    "react-audio-player": "^0.17.0"
  }
}
```

## 🎯 Feature Implementation Priorities

### Phase 1 - Core Functionality
1. ✅ Backend health monitoring
2. ✅ File upload with validation
3. ✅ Audio to MIDI transcription
4. ✅ Basic sheet music rendering

### Phase 2 - Enhanced UX
1. 🔄 Real-time progress indicators
2. 🔄 Audio playback controls
3. 🔄 MIDI playback functionality
4. 🔄 Download options (MIDI, PDF)

### Phase 3 - Advanced Features
1. 🚀 Real-time audio recording
2. 🚀 Multiple instrument support
3. 🚀 Collaborative editing
4. 🚀 Cloud storage integration

## 🤝 Backend Communication Best Practices

### Request Timeout Handling
```javascript
const transcribeWithTimeout = async (audioFile, timeout = 30000) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  
  try {
    const response = await fetch('/transcribe', {
      method: 'POST',
      body: formData,
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('Transcription timeout - please try a shorter audio file');
    }
    throw error;
  }
};
```

### Retry Logic
```javascript
const transcribeWithRetry = async (audioFile, maxRetries = 3) => {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await transcribeAudio(audioFile);
    } catch (error) {
      if (attempt === maxRetries) throw error;
      
      // Exponential backoff
      await new Promise(resolve => 
        setTimeout(resolve, Math.pow(2, attempt) * 1000)
      );
    }
  }
};
```

---

## 📋 Summary for AI Agent

**Use this backend repository (`audio-to-midi-backend`) to create a frontend application (`audio-to-midi-frontend`) that:**

1. **Integrates with the provided REST API** for audio-to-MIDI transcription
2. **Visualizes MIDI files** using VexFlow or ABCJS for sheet music rendering
3. **Provides real-time audio-to-sheet music rendering** with live preview
4. **Implements comprehensive error handling** and user feedback
5. **Supports mobile and desktop** with responsive design
6. **Includes audio playback controls** and MIDI download functionality

**Backend Repository**: `https://github.com/sergiecode/audio-to-midi-backend`  
**API Base URL**: `http://localhost:5000` (development)  
**Key Endpoints**: `/health`, `/supported_formats`, `/transcribe`

---

**Created by Sergie Code - AI Tools for Musicians**  
*Ready for frontend development! 🎵→🎼*
