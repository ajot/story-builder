# Story Builder

A tiny bedtime story tool for kids. Type in what the story should be about, and it generates a short bedtime story — both the text and an audio narration.

**[Try it live →](https://story.curiousmints.com)**

<img src="https://postbox.nyc3.cdn.digitaloceanspaces.com/404a4881-CleanShot_2026-01-16_at_12.54.042x.png" width="600" alt="Story Builder">

## How it works

Enter a character, a rough plot, and hit generate. The app creates a short, kid-friendly bedtime story and reads it aloud. If you like it, listen. If not, regenerate and try again.

<img src="https://postbox.nyc3.cdn.digitaloceanspaces.com/261a1b76-CleanShot_2026-01-16_at_12.54.412x.png" width="600" alt="Generated Story">

### Supports English and Hindi

Generate stories in either language. Useful if you're teaching your kid a second language — they hear the words in context and pick up phrases naturally.

<img src="https://postbox.nyc3.cdn.digitaloceanspaces.com/a17a966b-Screenshot_2026-01-16_at_2.23.37_PM.png" width="400" alt="Hindi Support">

### Background music

Optionally generate a short, gentle intro track to set the mood. It's like a little theme song for the story.

<img src="https://postbox.nyc3.cdn.digitaloceanspaces.com/d4dcc6d7-CleanShot_2026-01-16_at_13.27.102x.png" width="600" alt="Music Generation">

## Features

- **AI Story Generation** — Age-appropriate bedtime stories
- **Text-to-Speech** — 21 voice options via ElevenLabs
- **Multilingual** — English and Hindi support
- **Background Music** — AI-generated ambient tracks
- **Voice Preview** — Listen to samples before generating
- **Download** — Save narration and music as MP3 files
- **PWA-ready** — Add to your phone's home screen

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Single HTML page with Tailwind CSS
- **Deployment**: [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform)
- **AI Models** via [DigitalOcean Inference API](https://www.digitalocean.com/products/ai-ml):
  - Story generation: Llama 3.3 70B
  - Text-to-speech: [ElevenLabs Multilingual v2](https://fal.ai/models/fal-ai/elevenlabs/tts/multilingual-v2)
  - Music generation: [Stable Audio 2.5](https://fal.ai/models/fal-ai/stable-audio-25/text-to-audio)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ajot/story-builder.git
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

### 6. Run the app

```bash
python app.py
```

Visit `http://localhost:8080`

## Deployment

### DigitalOcean App Platform

1. Push your code to GitHub
2. Create a new App in [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform)
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
