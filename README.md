# AI Mock Interviewer

Upload your resume, get interview questions tailored to it, answer them,
and receive rubric-based scores and feedback.

**Status:** Work in progress (Week 1 of 8)

## Planned stack
Python, FastAPI, Streamlit, SQLite, Docker, GitHub Actions

## Setup
Coming soon.

## Setup

1. Create and activate a virtual environment:
   python3 -m venv .venv && source .venv/bin/activate
2. Install dependencies:
   pip install -r requirements.txt
3. Copy the env template and add your Gemini API key:
   cp .env.example .env
4. Run the API:
   python -m uvicorn main:app --reload
5. Open http://127.0.0.1:8000/docs for interactive API docs.

## Status

Week 1 complete: LLM calls with retry/backoff, schema-validated JSON output (Pydantic),
and a FastAPI `/questions` endpoint.

Measured so far (small samples, single machine):
- Gemini Flash-Lite averaged ~1.9s per call vs ~15.8s for the larger Flash model (3 runs each).
- JSON output valid in 10/10 runs with schema-constrained generation.
- `/questions` endpoint typically responds in 1.5 to 3.1s (5 requests).
