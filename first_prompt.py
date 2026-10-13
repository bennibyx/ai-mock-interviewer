import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY not found. Check your .env file.")

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
client = genai.Client(api_key=api_key)

RETRYABLE = (429, 500, 503)  # errors that can fix themselves


def ask(prompt: str, retries: int = 4):
    """Send a prompt; retry with exponential backoff on temporary errors."""
    for attempt in range(retries):
        try:
            return client.models.generate_content(model=MODEL, contents=prompt)
        except errors.APIError as e:
            if e.code not in RETRYABLE:
                raise  # your bug (bad key, bad model): retrying won't help
            wait = 2 ** attempt  # 1s, 2s, 4s, 8s
            print(f"Got {e.code}. Retry {attempt + 1}/{retries} in {wait}s...")
            time.sleep(wait)
    raise SystemExit("Still unavailable. Try later or switch GEMINI_MODEL in .env.")


prompt = (
    "You are a technical interviewer. "
    "Ask me one interview question for an entry-level AI/ML engineer role."
)

start = time.time()
response = ask(prompt)
elapsed = time.time() - start

print(response.text)
print(f"\n[model={MODEL} | latency={elapsed:.2f}s]")
