# Jarvis 1.0 (voice-agent-projects)

Personal voice assistant built with LiveKit Agents and OpenAI real-time model (gpt-realtime-mini)

## Overview

- `agent.py`: main server and agent setup.
- `prompts.py`: agent and session instruction prompts.
- `tools.py`: function tools exposed to the agent:
  - `get_weather(city)` via wttr.in
  - `web_search(query)` via DuckDuckGo
  - `send_email(recipient, subject, body, cc_email?)` via Gmail SMTP

The assistant persona is `Friday`, a sarcastic classy butler that replies in one sentence.

## Requirements

- Python 3.8+
- `pip install -r requirements.txt`
- LiveKit Agents SDK, OpenAI, dotenv, requests, langchain-community, etc.

## Environment variables

Create a `.env` file in the project root with:

```env
OPENAI_API_KEY=your_openai_api_key
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_secret
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

## Run locally

```bash
python agent.py
```

This starts an `AgentServer` and offers `my_agent` realtime session handler.

## Agent behavior

- Uses voice `shimmer`, model `gpt-realtime-mini`, temperature `0.8`.
- Starts conversation with: "Hi my name is Friday, your personal assistant, how may I help you?"
- Performs actions through tools when requested.

## Notes

- Ensure `GMAIL_APP_PASSWORD` is set up for SMTP.
- For audio input noise cancellation, it uses LiveKit `BVC` or `BVCTelephony` depending on participant type.

## Extending

- Add additional tools in `tools.py` and include in `Assistant` class `tools=[...]`.
- Modify persona in `prompts.py`.
