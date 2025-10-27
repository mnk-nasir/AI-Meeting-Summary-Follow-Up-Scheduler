# AI-Meeting-Summary-Follow-Up-Scheduler# 🤖 AI Meeting Tool (Python v2)

Rebuilt from the n8n workflow **AI Meeting Tool**.

---

## 🧩 Features
- Fetches Google Calendar events + Meet transcripts  
- Summarizes and analyzes using OpenAI  
- Detects and auto-creates follow-up meetings  
- Works fully offline in **mock mode**

---

## 🚀 Quick Start
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
Then edit .env with your keys (or leave blank for mock mode) and run:

bash
Copy code
python ai_meeting_tool.py
⚙️ Mock Mode
If any key is missing, mock data is used:

Fake transcript and meeting

AI summary simulated

Calendar event creation logged only

Perfect for testing logic safely.

🧠 Real Integrations (To Add)
Google Calendar API (v3)

Google Drive API for Meet transcripts

OpenAI Chat Completions API

🕓 Automation
Run automatically after each meeting:

bash
Copy code
0 * * * * /usr/bin/python /path/to/ai_meeting_tool.py
Or connect via GitHub Actions for daily summaries.

🪪 License
MIT License © 2025

markdown
Copy code

---

✅ **All 5 files complete**:
1. `ai_meeting_tool.py`  
2. `config.py`  
3. `requirements.txt`  
4. `.env.example`  
5. `README.md`  

Would you like me to add a **GitHub Actions workflow** (`.github/workflows/ai_meeting.yml`) that runs 
