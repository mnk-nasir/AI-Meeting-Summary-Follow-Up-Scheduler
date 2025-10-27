#!/usr/bin/env python3
"""
AI Meeting Tool (Python v2)
---------------------------
Workflow:
1. Fetch a Google Calendar meeting + transcript (PDF)
2. Summarize it via OpenAI (goals, highlights, next steps)
3. Detect follow-up meeting suggestions
4. Create calendar events and invite attendees

Runs in MOCK mode automatically if API keys are missing.
"""

import os
import logging
from datetime import datetime, timedelta
import requests
from openai import OpenAI
from config import Config

log = logging.getLogger("ai_meeting_tool")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
cfg = Config.load_from_env()


# -------- MOCK HELPERS --------
def mock_calendar_event():
    return {
        "id": "abc123",
        "summary": "Weekly AI Research Sync",
        "start": {"dateTime": "2025-10-25T10:00:00"},
        "end": {"dateTime": "2025-10-25T11:00:00"},
        "creator": {"displayName": "Alice", "email": "alice@example.com"},
        "attendees": [{"email": "bob@example.com", "displayName": "Bob"}],
    }


def mock_transcript_text():
    return """Alice: Let's schedule a follow-up meeting next Tuesday to finalize the model results.
Bob: Sure, 2 PM works for me."""


# -------- DATA RETRIEVAL --------
def get_calendar_event(event_id: str):
    if cfg.mock:
        log.info("[MOCK] Getting calendar event")
        return mock_calendar_event()

    url = f"https://www.googleapis.com/calendar/v3/calendars/{cfg.GOOGLE_CALENDAR_ID}/events/{event_id}"
    headers = {"Authorization": f"Bearer {cfg.GOOGLE_API_TOKEN}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()


def get_meet_transcript_file(conference_id: str):
    if cfg.mock:
        log.info("[MOCK] Retrieving transcript PDF and parsing text")
        return mock_transcript_text()

    # Real logic placeholder
    raise NotImplementedError("Real Google Meet transcript API call not implemented yet.")


# -------- OPENAI ANALYSIS --------
def analyze_meeting(event, transcript):
    if cfg.mock:
        log.info("[MOCK] Analyzing transcript")
        return {
            "summary": "Follow-up meeting required to finalize results.",
            "highlights": [{"attendee": "Alice", "message": "Schedule follow-up next Tuesday"}],
            "next_steps": ["Organize follow-up meeting", "Prepare presentation slides"],
            "meetings_created": [
                {"event_title": "Follow-up: Model Results", "event_invite_url": "https://mock.calendar/event123"}
            ],
        }

    client = OpenAI(api_key=cfg.OPENAI_API_KEY)
    prompt = f"""
You are an AI meeting assistant.
Meeting summary:
Creator: {event['creator']['displayName']} <{event['creator']['email']}>
Attendees: {', '.join(a['email'] for a in event.get('attendees', []))}
Transcript:
\"\"\"{transcript}\"\"\"

1. Summarize key points.
2. Extract highlights per attendee.
3. List next steps.
4. If transcript mentions a follow-up, propose event details.
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return {"summary": res.choices[0].message.content}


# -------- CALENDAR EVENT CREATION --------
def create_followup_event(title, start_time, attendees):
    if cfg.mock:
        log.info(f"[MOCK] Creating calendar event '{title}' at {start_time}")
        return {"id": "event123", "htmlLink": "https://calendar.google.com/mock"}

    url = f"https://www.googleapis.com/calendar/v3/calendars/{cfg.GOOGLE_CALENDAR_ID}/events"
    headers = {
        "Authorization": f"Bearer {cfg.GOOGLE_API_TOKEN}",
        "Content-Type": "application/json",
    }
    body = {
        "summary": title,
        "start": {"dateTime": start_time.isoformat()},
        "end": {"dateTime": (start_time + timedelta(hours=1)).isoformat()},
        "attendees": [{"email": a} for a in attendees],
    }
    r = requests.post(url, headers=headers, json=body)
    return r.json()


# -------- MAIN WORKFLOW --------
def main():
    log.info("🤖 Starting AI Meeting Tool")

    event_id = os.getenv("EVENT_ID", "abc123")
    event = get_calendar_event(event_id)
    transcript = get_meet_transcript_file(event["id"])
    analysis = analyze_meeting(event, transcript)

    log.info(f"Summary:\n{analysis.get('summary')}")
    log.info(f"Next steps: {analysis.get('next_steps')}")

    # Auto-create follow-up if mentioned
    if analysis.get("next_steps"):
        start_time = datetime.now() + timedelta(days=3)
        attendees = [a["email"] for a in event.get("attendees", [])]
        created = create_followup_event("Follow-up: Meeting Outcomes", start_time, attendees)
        log.info(f"📅 Follow-up created: {created.get('htmlLink')}")

    log.info("✅ Workflow complete.")


if __name__ == "__main__":
    main()
