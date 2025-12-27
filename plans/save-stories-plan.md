# Plan: Save Stories to PostgreSQL with Library View

## Overview
Add ability to save stories to a DigitalOcean PostgreSQL database. Include a library view to browse and replay past stories.

## User Requirements
- Save full story data: prompt, story text, voice, audio/music URLs, timestamps, title, favorite flag
- Library view to browse past stories and replay them

## Database Schema

**Table: `stories`**
```sql
CREATE TABLE stories (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    prompt TEXT NOT NULL,
    story_text TEXT NOT NULL,
    voice VARCHAR(50) DEFAULT 'Rachel',
    narration_url TEXT,
    music_url TEXT,
    music_prompt TEXT,
    is_favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Implementation

### 1. Backend: Database Setup

**New file:** `db.py`
```python
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))
```

**Update:** `requirements.txt`
- Add `psycopg2-binary`

**Update:** `.env.example`
- Add `DATABASE_URL=postgresql://user:pass@host:port/dbname?sslmode=require`

### 2. Backend: New API Endpoints

**File:** `app.py`

```python
# POST /save-story - Save a story
@app.route("/save-story", methods=["POST"])
def save_story():
    # Accepts: title, prompt, story_text, voice, narration_url, music_url, music_prompt
    # Returns: {id, success}

# GET /stories - List all stories
@app.route("/stories", methods=["GET"])
def list_stories():
    # Returns: [{id, title, prompt, created_at, is_favorite}, ...]

# GET /stories/<id> - Get full story details
@app.route("/stories/<int:story_id>", methods=["GET"])
def get_story(story_id):
    # Returns: full story object

# PUT /stories/<id>/favorite - Toggle favorite
@app.route("/stories/<int:story_id>/favorite", methods=["PUT"])
def toggle_favorite(story_id):
    # Toggles is_favorite flag

# DELETE /stories/<id> - Delete story
@app.route("/stories/<int:story_id>", methods=["DELETE"])
def delete_story(story_id):
    # Deletes story
```

### 3. Frontend: Save Button

**File:** `templates/index.html`

Add "Save Story" button after story is generated and audio is ready:
```html
<button onclick="saveStory()">💾 Save Story</button>
```

Add title input modal/prompt when saving.

### 4. Frontend: Library View

**Option A: Same page with toggle**
- Add "📚 Library" button in header
- Toggle between story builder and library view
- Library shows grid/list of saved stories

**Option B: Separate page**
- New route `/library` → `library.html`
- Navigate between pages

**Recommended: Option A** (simpler, single-page feel)

**Library UI:**
```
┌─────────────────────────────────────┐
│ 📚 My Stories                [Back] │
├─────────────────────────────────────┤
│ ⭐ The Brave Bunny    Dec 26, 2024  │
│    "a bunny who finds a star"       │
│    [▶ Play] [🗑️]                    │
├─────────────────────────────────────┤
│    Forest Adventure   Dec 25, 2024  │
│    "animals in the magical forest"  │
│    [▶ Play] [🗑️]                    │
└─────────────────────────────────────┘
```

### 5. Database Initialization Script

**New file:** `scripts/init_db.py`
```python
# Creates the stories table if not exists
# Run once on first deploy
```

## Files to Create/Modify

1. **`db.py`** - Database connection helper
2. **`scripts/init_db.py`** - Table creation script
3. **`app.py`** - Add 5 new endpoints (save, list, get, favorite, delete)
4. **`templates/index.html`** - Add save button, library toggle, library view
5. **`requirements.txt`** - Add `psycopg2-binary`
6. **`.env.example`** - Add `DATABASE_URL`

## Execution Order

1. Add `psycopg2-binary` to requirements.txt
2. Create `db.py` with connection helper
3. Create `scripts/init_db.py` and run to create table
4. Add API endpoints to `app.py`
5. Update frontend with save button and library view
6. Test locally with DO database connection

## Environment Variable

User needs to set `DATABASE_URL` from their DigitalOcean database:
```
DATABASE_URL=postgresql://doadmin:password@db-postgresql-xxx.ondigitalocean.com:25060/defaultdb?sslmode=require
```
