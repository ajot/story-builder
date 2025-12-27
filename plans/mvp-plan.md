# Story Builder MVP Plan

## Overview
A web app to create and narrate bedtime stories for a 4-year-old. Users provide a simple prompt, AI generates an age-appropriate story, and the story is narrated aloud using text-to-speech.

## Tech Stack
- **Backend**: Python/Flask
- **Frontend**: HTML/CSS/JavaScript (Tailwind CSS)
- **Story Generation**: DigitalOcean Inference API (Llama 3.3 70B)
- **Text-to-Speech**: Fal ElevenLabs via DigitalOcean Async API
- **Deployment**: DigitalOcean App Platform

## User Flow
```
1. User enters a story prompt (e.g., "a brave bunny who finds a lost star")
         ↓
2. Click "Create Story" → AI generates child-friendly story
         ↓
3. Story displayed on screen → User can "Regenerate" if not satisfied
         ↓
4. Once happy, click "Read Aloud" → TTS generates narration
         ↓
5. Audio plays with play/pause controls
```

## API Integrations

### 1. Story Generation (DO Inference)
- **Endpoint**: `https://cluster-api.do-ai.run/v1/chat/completions`
- **Model**: `meta-llama/Llama-3.3-70B-Instruct`
- **Auth**: Bearer token (DO_API_KEY)
- **System Prompt**: Instructs AI to create age-appropriate, 3-5 paragraph stories with happy endings

### 2. Text-to-Speech (Fal ElevenLabs via DO)
- **Endpoint**: `https://inference.do-ai.run/v1/async-invoke`
- **Model**: `fal-ai/elevenlabs/tts/multilingual-v2`
- **Voice**: "Rachel" (friendly, clear voice)
- **Flow**: Submit job → Poll status → Retrieve audio URL

## File Structure
```
story-builder/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container config for DO App Platform
├── .env.example          # Environment variables template
├── templates/
│   └── index.html        # Main UI
└── plans/
    └── mvp-plan.md       # This file
```

## Implementation Tasks

### Phase 1: Core Backend
1. Create Flask app with basic routes:
   - `GET /` - Serve frontend
   - `POST /generate-story` - Generate story from prompt
   - `POST /generate-audio` - Convert story to speech

2. Implement story generation:
   - Call DO Inference API with child-friendly system prompt
   - Return generated story text
   - Handle errors gracefully

3. Implement TTS:
   - Submit async job to Fal ElevenLabs
   - Poll for completion (2-second intervals, 60 max attempts)
   - Return audio URL when ready

### Phase 2: Frontend
1. Simple, clean UI with:
   - Text input for story prompt
   - "Create Story" button
   - Story display area
   - "Regenerate" button (appears after story generated)
   - "Read Aloud" button
   - Audio player with controls

2. Visual feedback:
   - Loading spinners during generation
   - Disabled buttons while processing
   - Error messages if something fails

### Phase 3: Deployment
1. Create `requirements.txt`:
   - flask
   - gunicorn
   - requests

2. Create `Dockerfile`:
   - Python 3.11 base
   - Install dependencies
   - Expose port 8080
   - Run with gunicorn

3. Set up GitHub repo for DO App Platform deployment

## Environment Variables
```
DO_API_KEY=<your-digitalocean-api-key>
```

## UI Mockup (ASCII)
```
┌─────────────────────────────────────────────────────────┐
│                    Story Builder                         │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ What should the story be about?                    │ │
│  │                                                    │ │
│  │ [a brave bunny who finds a lost star            ] │ │
│  │                                                    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│              [ Create Story ]                            │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │                                                    │ │
│  │  Once upon a time, there was a little bunny       │ │
│  │  named Bella who loved to look at the stars...    │ │
│  │                                                    │ │
│  │  One night, Bella saw a tiny star fall from       │ │
│  │  the sky and land in her garden...                │ │
│  │                                                    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│         [ Regenerate ]    [ Read Aloud ]                │
│                                                          │
│         ▶ ━━━━━━━━━━━━━━━━━━━━━━━ 0:00 / 2:30           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Future Enhancements (Post-MVP)
- **v1.5**: Background music/ambient sounds (Fal Stable Audio)
- **v2.0**: Generated images per scene (Fal image models)
- **v2.5**: Save favorite stories locally
- **v3.0**: Interactive story choices ("What should Bella do next?")
- **v3.5**: Multiple character voices

## Deployment Checklist
- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Create DO App Platform app
- [ ] Configure DO_API_KEY environment variable
- [ ] Deploy and test
