# 🎼 Frontend Development Brief - Audio to MIDI Web Application

**For AI Agent**: Create `audio-to-midi-frontend` repository

## 🎯 Project Overview

Create a modern web application that integrates with the existing `audio-to-midi-backend` API to provide:
- Audio file upload and transcription to MIDI
- Real-time sheet music visualization using VexFlow or ABCJS  
- Live audio-to-sheet music rendering
- MIDI playback and download functionality

## 🔌 Backend Integration Points

**Repository**: `sergiecode/audio-to-midi-backend`  
**API Base URL**: `http://localhost:5000`

### Core API Endpoints:
```
GET  /health              - Check backend status
GET  /supported_formats   - Get audio format info  
POST /transcribe          - Upload audio, get MIDI file
```

### Integration Example:
```javascript
// Upload audio and get MIDI
const formData = new FormData();
formData.append('audio_file', audioFile);

const response = await fetch('http://localhost:5000/transcribe', {
  method: 'POST',
  body: formData
});

const midiBlob = await response.blob(); // Returns .mid file
```

## 🛠️ Technical Requirements

### Frontend Tech Stack:
- **Framework**: React, Vue.js, or modern vanilla JavaScript
- **Sheet Music**: VexFlow or ABCJS for notation rendering
- **MIDI Processing**: @tonejs/midi or midi-parser-js
- **Styling**: Modern CSS framework (Tailwind, Material-UI, etc.)
- **File Handling**: HTML5 File API with drag-and-drop

### Core Components Needed:
1. **File Uploader** - Audio file selection with format validation
2. **Transcription Progress** - Real-time processing indicators  
3. **Sheet Music Viewer** - VexFlow/ABCJS integration for notation display
4. **Audio Player** - Playback controls for original audio
5. **MIDI Player** - Playback controls for generated MIDI
6. **Download Manager** - Export MIDI, PDF, or other formats

## 🎵 Key Features to Implement

### Phase 1 - Core Functionality:
- ✅ Audio file upload (WAV, MP3, FLAC, M4A)
- ✅ Real-time transcription status
- ✅ MIDI file generation and download
- ✅ Basic sheet music rendering
- ✅ Responsive design (mobile + desktop)

### Phase 2 - Enhanced UX:
- 🎼 Audio playback with waveform visualization
- 🎼 MIDI playback with note highlighting
- 🎼 Zoom and pan controls for sheet music
- 🎼 Multiple export formats (PDF, MusicXML)

### Phase 3 - Advanced Features:
- 🚀 Real-time audio recording
- 🚀 Live transcription (if backend supports)
- 🚀 Multi-track MIDI support
- 🚀 Collaborative sharing features

## 🎨 UI/UX Guidelines

### Design Principles:
- **Clean, modern interface** with music-focused aesthetics
- **Intuitive workflow**: Upload → Transcribe → View → Download
- **Real-time feedback** for all operations
- **Mobile-first responsive design**
- **Accessibility** for musicians with disabilities

### Color Scheme Suggestions:
- Primary: Music-inspired blues/purples
- Accent: Gold/yellow for active states  
- Background: Clean whites/light grays
- Text: High contrast for readability

## 🔧 Integration Code Examples

### Backend Health Check:
```javascript
const checkBackend = async () => {
  try {
    const response = await fetch('http://localhost:5000/health');
    const data = await response.json();
    return data.status === 'healthy';
  } catch (error) {
    return false;
  }
};
```

### MIDI to VexFlow Conversion:
```javascript
import { Midi } from '@tonejs/midi';
import Vex from 'vexflow';

const renderSheetMusic = async (midiBlob) => {
  const arrayBuffer = await midiBlob.arrayBuffer();
  const midi = new Midi(arrayBuffer);
  
  const VF = Vex.Flow;
  const div = document.getElementById('sheet-music');
  const renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);
  
  // Convert MIDI notes to VexFlow notation
  midi.tracks.forEach(track => {
    track.notes.forEach(note => {
      // Render individual notes
    });
  });
};
```

### File Upload with Validation:
```javascript
const handleFileUpload = async (file) => {
  // Validate file type and size
  const supportedFormats = await getSupportedFormats();
  
  if (!isValidAudioFile(file, supportedFormats)) {
    throw new Error('Invalid file format');
  }
  
  // Upload and transcribe
  const result = await transcribeAudio(file);
  return result;
};
```

## 📁 Suggested Project Structure

```
audio-to-midi-frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── FileUploader.jsx
│   │   ├── SheetMusicViewer.jsx
│   │   ├── AudioPlayer.jsx
│   │   ├── MidiPlayer.jsx
│   │   └── ProgressIndicator.jsx
│   ├── services/
│   │   ├── apiService.js
│   │   ├── midiProcessor.js
│   │   └── sheetMusicRenderer.js
│   ├── hooks/
│   │   ├── useBackendStatus.js
│   │   └── useTranscription.js
│   ├── utils/
│   │   ├── fileValidation.js
│   │   └── errorHandling.js
│   └── App.jsx
├── package.json
└── README.md
```

## 🧪 Testing Requirements

### Unit Tests:
- API service functions
- MIDI processing utilities
- File validation logic
- Component rendering

### Integration Tests:
- Backend API connectivity
- File upload workflow
- MIDI to sheet music conversion
- Error handling scenarios

### E2E Tests:
- Complete user workflow
- Cross-browser compatibility
- Mobile responsiveness

## 📚 Dependencies to Include

### Core:
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "@tonejs/midi": "^2.0.28",
    "vexflow": "^4.0.3",
    "react-dropzone": "^14.2.3"
  }
}
```

### Optional Enhancements:
```json
{
  "dependencies": {
    "abcjs": "^6.2.3",
    "midi-player-js": "^2.0.14",
    "wavesurfer.js": "^7.0.2",
    "react-audio-player": "^0.17.0"
  }
}
```

## 🚀 Deployment Considerations

- **Development**: Works with `http://localhost:5000` backend
- **Production**: Configure backend URL via environment variables
- **CORS**: Backend already configured for cross-origin requests
- **Performance**: Implement lazy loading for large MIDI files
- **PWA**: Consider Progressive Web App features for mobile

## 📖 Documentation to Include

1. **README.md** - Setup and usage instructions
2. **API_INTEGRATION.md** - Backend integration details  
3. **COMPONENTS.md** - Component library documentation
4. **DEPLOYMENT.md** - Production deployment guide

## 🎵 Success Criteria

The frontend should successfully:
1. ✅ Connect to the audio-to-midi-backend API
2. ✅ Upload audio files and receive MIDI responses
3. ✅ Render sheet music from MIDI data
4. ✅ Provide intuitive user experience
5. ✅ Handle errors gracefully
6. ✅ Work on both desktop and mobile devices

---

**Backend Repository**: `https://github.com/sergiecode/audio-to-midi-backend`  
**Full Integration Guide**: See `FRONTEND_INTEGRATION_GUIDE.md` in backend repo

**Created by Sergie Code - AI Tools for Musicians** 🎵
