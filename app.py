import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from prompts import STORY_SYSTEM_PROMPT_EN, STORY_SYSTEM_PROMPT_HI, MUSIC_PROMPT_SYSTEM

load_dotenv()

app = Flask(__name__)

# Configuration
DEBUG_MODE = os.environ.get("DEBUG_MODE", "false").lower() == "true"
DO_API_KEY = os.environ.get("DIGITAL_OCEAN_MODEL_ACCESS_KEY")

# OpenAI client for DO Inference
client = OpenAI(
    base_url="https://inference.do-ai.run/v1/",
    api_key=DO_API_KEY,
) if DO_API_KEY else None

# Story generation model
STORY_MODEL = "llama3.3-70b-instruct"


@app.route("/")
def index():
    return render_template("index.html", debug_mode=DEBUG_MODE)


@app.route("/generate-story", methods=["POST"])
def generate_story():
    """Generate a story using DigitalOcean Inference API."""
    data = request.json
    prompt = data.get("prompt", "")
    language = data.get("language", "en")

    if not prompt:
        return jsonify({"error": "Please provide a story idea!"}), 400

    if not client:
        return jsonify({"error": "DIGITAL_OCEAN_MODEL_ACCESS_KEY not configured"}), 500

    # Select system prompt based on language
    system_prompt = STORY_SYSTEM_PROMPT_HI if language == "hi" else STORY_SYSTEM_PROMPT_EN
    user_prompt = f"कृपया इस विषय पर एक छोटी सी कहानी बनाएं: {prompt}" if language == "hi" else f"Please create a short bedtime story about: {prompt}"

    try:
        response = client.chat.completions.create(
            model=STORY_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000,
            temperature=0.8
        )
        story = response.choices[0].message.content
        return jsonify({"story": story})
    except Exception as e:
        return jsonify({"error": f"Story generation failed: {str(e)}"}), 500


@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    """Submit audio job using Fal ElevenLabs through DO async-invoke."""
    data = request.json
    text = data.get("text", "")
    voice = data.get("voice", "Rachel")
    language = data.get("language", "en")

    if not text:
        return jsonify({"error": "No text provided for narration"}), 400

    if not DO_API_KEY:
        return jsonify({"error": "DIGITAL_OCEAN_MODEL_ACCESS_KEY not configured"}), 500

    headers = {
        "Authorization": f"Bearer {DO_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": "fal-ai/elevenlabs/tts/multilingual-v2",
        "input": {
            "text": text,
            "voice": voice,
            "language": language
        }
    }

    try:
        response = requests.post(
            "https://inference.do-ai.run/v1/async-invoke",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        job = response.json()
        request_id = job.get("request_id")

        if not request_id:
            return jsonify({"error": "No request ID received"}), 500

        return jsonify({"request_id": request_id, "status": "SUBMITTED"})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Audio job submission failed: {str(e)}"}), 500


@app.route("/audio-status/<request_id>", methods=["GET"])
def audio_status(request_id):
    """Check status of audio generation job."""
    if not DO_API_KEY:
        return jsonify({"error": "DIGITAL_OCEAN_MODEL_ACCESS_KEY not configured"}), 500

    headers = {
        "Authorization": f"Bearer {DO_API_KEY}",
    }

    try:
        status_response = requests.get(
            f"https://inference.do-ai.run/v1/async-invoke/{request_id}/status",
            headers=headers,
            timeout=10
        )
        status_response.raise_for_status()
        status_data = status_response.json()

        return jsonify(status_data)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Status check failed: {str(e)}"}), 500


@app.route("/audio-result/<request_id>", methods=["GET"])
def audio_result(request_id):
    """Get result of completed audio generation job."""
    if not DO_API_KEY:
        return jsonify({"error": "DIGITAL_OCEAN_MODEL_ACCESS_KEY not configured"}), 500

    headers = {
        "Authorization": f"Bearer {DO_API_KEY}",
    }

    try:
        result_response = requests.get(
            f"https://inference.do-ai.run/v1/async-invoke/{request_id}",
            headers=headers,
            timeout=30
        )
        result_response.raise_for_status()
        result = result_response.json()

        # Extract audio URL from result
        output = result.get("output", {})
        audio_url = (
            output.get("audio_url") or
            output.get("audio", {}).get("url") or
            output.get("url")
        )

        return jsonify({"audio_url": audio_url})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Result fetch failed: {str(e)}"}), 500


@app.route("/generate-music-prompt", methods=["POST"])
def generate_music_prompt():
    """Generate a music prompt based on the story content."""
    data = request.json
    story = data.get("story", "")

    if not story:
        return jsonify({"error": "No story provided"}), 400

    if not client:
        return jsonify({"error": "DIGITAL_OCEAN_MODEL_ACCESS_KEY not configured"}), 500

    try:
        response = client.chat.completions.create(
            model=STORY_MODEL,
            messages=[
                {"role": "system", "content": MUSIC_PROMPT_SYSTEM},
                {"role": "user", "content": f"Suggest background music for this children's story:\n\n{story}"}
            ],
            max_tokens=100,
            temperature=0.7
        )
        music_prompt = response.choices[0].message.content.strip()
        return jsonify({"prompt": music_prompt})
    except Exception as e:
        return jsonify({"error": f"Music prompt generation failed: {str(e)}"}), 500


@app.route("/generate-sound", methods=["POST"])
def generate_sound():
    """Submit sound generation job using Fal Stable Audio through DO async-invoke."""
    data = request.json
    prompt = data.get("prompt", "")
    duration = data.get("duration", 10)

    if not prompt:
        return jsonify({"error": "No prompt provided for sound generation"}), 400

    if not DO_API_KEY:
        return jsonify({"error": "DIGITAL_OCEAN_MODEL_ACCESS_KEY not configured"}), 500

    headers = {
        "Authorization": f"Bearer {DO_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": "fal-ai/stable-audio-25/text-to-audio",
        "input": {
            "prompt": prompt,
            "seconds_total": duration
        }
    }

    try:
        response = requests.post(
            "https://inference.do-ai.run/v1/async-invoke",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        job = response.json()
        request_id = job.get("request_id")

        if not request_id:
            return jsonify({"error": "No request ID received"}), 500

        return jsonify({"request_id": request_id, "status": "SUBMITTED"})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Sound job submission failed: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
