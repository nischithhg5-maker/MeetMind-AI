# MeetMind AI

An AI-powered meeting research agent that delivers recent company insights and source-backed briefings to help users prepare for meetings.

## Current status

**Frontend prototype v0.1** — Streamlit UI with sample/demo content. Tavily, Bifrost, live AI generation, PDF export and persistent storage are not connected yet.

## Features represented in the UI

- Meeting context form
- Recent research workspace (integration pending)
- One-page briefing destination (integration pending)
- Source attribution / Evidence Explorer layout
- Open questions destination (briefing generation pending)
- Freshness tracking destination (live source dates pending)
- Smart question generation (AI integration pending)
- PDF export (planned)
- Briefing history (sample content only)

## Run locally

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

## Project structure

```text
MeetMind-AI/
├── app.py
├── demo_data.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── assets/
├── components/
├── pages/
└── services/
```

## Security

Never commit API keys, `.env` files, or Streamlit secrets to GitHub. Use environment variables or Streamlit secrets for integrations.

## Planned integrations

- Tavily for web research and source retrieval.
- Bifrost as the AI model gateway.
- An LLM accessed through Bifrost for summarisation and question generation.

## Important

Any sample companies, sources, counts, and briefing history shown in the prototype are illustrative placeholders, not real research.
# MeetMind-AI
An AI-powered meeting research agent that delivers real-time insights, company intelligence, and smart briefings to help you prepare for every meeting.
