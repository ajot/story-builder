# Story Builder

A magical bedtime story generator for children. Create personalized stories with AI-generated narration and background music.

## Features

- **AI Story Generation** - Creates age-appropriate bedtime stories for 4-year-olds
- **Multilingual Support** - Generate stories in English or Hindi
- **Text-to-Speech** - 21 voice options via ElevenLabs
- **Background Music** - AI-generated ambient music to accompany stories
- **Voice Preview** - Listen to voice samples before generating
- **Download** - Save narration and music as MP3 files

## Tech Stack

- **Backend**: Flask (Python)
- **AI Models**: DigitalOcean Inference API
  - Story generation: Llama 3.3 70B
  - Text-to-speech: ElevenLabs Multilingual v2
  - Music generation: Stable Audio
- **Frontend**: Tailwind CSS

## Prerequisites

- Python 3.11+
- DigitalOcean account with Inference API access

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/story-builder.git
cd story-builder
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```bash
DIGITAL_OCEAN_MODEL_ACCESS_KEY=your_api_key_here
```

Get your API key from the [DigitalOcean Control Panel](https://cloud.digitalocean.com/gen-ai/inference/endpoints).

### 5. Generate voice samples (optional)

Pre-generate voice preview samples:

```bash
python scripts/generate_samples.py
```

This creates MP3 samples for all 21 voices in both English and Hindi.

### 6. Run the app

```bash
python app.py
```

Visit `http://localhost:8080`

## Deployment

### DigitalOcean App Platform

1. Push your code to GitHub
2. Create a new App in DigitalOcean App Platform
3. Connect your GitHub repository
4. Add environment variable: `DIGITAL_OCEAN_MODEL_ACCESS_KEY`
5. Deploy

The included `Dockerfile` handles the build configuration.

## Project Structure

```
story-builder/
├── app.py                 # Flask application
├── prompts.py             # AI system prompts
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container configuration
├── templates/
│   └── index.html         # Frontend UI
├── static/
│   └── voice-samples/     # Pre-generated voice previews
└── scripts/
    └── generate_samples.py # Voice sample generator
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application UI |
| `/generate-story` | POST | Generate a bedtime story |
| `/generate-audio` | POST | Submit TTS job |
| `/audio-status/<id>` | GET | Check TTS job status |
| `/audio-result/<id>` | GET | Get TTS result |
| `/generate-music-prompt` | POST | Generate music description |
| `/generate-sound` | POST | Submit music generation job |

## License

MIT
