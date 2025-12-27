#!/usr/bin/env python3
"""
One-time script to generate voice samples for all ElevenLabs voices.
Run this locally, then commit the generated MP3s to the repo.
"""

import os
import time
import requests
from dotenv import load_dotenv

# Load environment from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

DO_API_KEY = os.environ.get("DIGITAL_OCEAN_MODEL_ACCESS_KEY")

if not DO_API_KEY:
    print("Error: DIGITAL_OCEAN_MODEL_ACCESS_KEY not found in .env")
    exit(1)

# All available ElevenLabs voices
VOICES = [
    "Rachel", "Aria", "Roger", "Sarah", "Laura", "Charlie", "George",
    "Callum", "River", "Liam", "Charlotte", "Alice", "Matilda", "Will",
    "Jessica", "Eric", "Chris", "Brian", "Daniel", "Lily", "Bill"
]

# Languages with sample text
LANGUAGES = {
    "en": "Hi, I'm {name}. Let me tell you a story.",
    "hi": "नमस्ते, मैं {name} हूं। आइए, एक कहानी सुनते हैं।"
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'voice-samples')

headers = {
    "Authorization": f"Bearer {DO_API_KEY}",
    "Content-Type": "application/json"
}


def submit_audio_job(voice: str, text: str, language: str = "en") -> str:
    """Submit async TTS job, return request_id."""
    payload = {
        "model_id": "fal-ai/elevenlabs/tts/multilingual-v2",
        "input": {
            "text": text,
            "voice": voice,
            "language": language
        }
    }

    response = requests.post(
        "https://inference.do-ai.run/v1/async-invoke",
        headers=headers,
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    return response.json().get("request_id")


def poll_until_complete(request_id: str, max_attempts: int = 60) -> bool:
    """Poll status until complete or failed."""
    for attempt in range(max_attempts):
        response = requests.get(
            f"https://inference.do-ai.run/v1/async-invoke/{request_id}/status",
            headers={"Authorization": f"Bearer {DO_API_KEY}"},
            timeout=10
        )
        status = response.json().get("status")
        print(f"  Status: {status} (attempt {attempt + 1})")

        if status == "COMPLETED":
            return True
        if status == "FAILED":
            return False

        time.sleep(2)

    return False


def get_audio_url(request_id: str) -> str:
    """Get the audio URL from completed job."""
    response = requests.get(
        f"https://inference.do-ai.run/v1/async-invoke/{request_id}",
        headers={"Authorization": f"Bearer {DO_API_KEY}"},
        timeout=30
    )
    result = response.json()
    output = result.get("output", {})
    return (
        output.get("audio_url") or
        output.get("audio", {}).get("url") or
        output.get("url")
    )


def download_audio(url: str, filepath: str):
    """Download audio file from URL."""
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    with open(filepath, 'wb') as f:
        f.write(response.content)


def generate_sample(voice: str, language: str = "en"):
    """Generate and save voice sample."""
    text = LANGUAGES[language].format(name=voice)
    filename = f"{voice.lower()}_{language}.mp3" if language != "en" else f"{voice.lower()}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Skip if already exists
    if os.path.exists(filepath):
        print(f"[{voice}/{language}] Already exists, skipping")
        return True

    print(f"[{voice}/{language}] Generating sample...")

    try:
        # Submit job
        request_id = submit_audio_job(voice, text, language)
        print(f"  Request ID: {request_id}")

        # Poll until complete
        if not poll_until_complete(request_id):
            print(f"  FAILED!")
            return False

        # Get audio URL
        audio_url = get_audio_url(request_id)
        if not audio_url:
            print(f"  No audio URL found!")
            return False

        print(f"  Downloading: {audio_url}")
        download_audio(audio_url, filepath)
        print(f"  Saved: {filename}")
        return True

    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    total = len(VOICES) * len(LANGUAGES)
    print(f"Generating voice samples for {len(VOICES)} voices x {len(LANGUAGES)} languages = {total} samples")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    success = 0
    failed = 0

    for voice in VOICES:
        for lang in LANGUAGES:
            if generate_sample(voice, lang):
                success += 1
            else:
                failed += 1
            print()

    print(f"Done! Success: {success}, Failed: {failed}")


if __name__ == "__main__":
    main()
