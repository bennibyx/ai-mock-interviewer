import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY not found. Check your .env file.")

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
client = genai.Client(api_key=api_key)

RETRYABLE = (429, 500, 503)  # temporary errors worth retrying


def ask(prompt, system=None, temperature=None, schema=None, retries=4):
    """Send a prompt. If schema (a Pydantic class) is given, request JSON in that shape."""
    options = {"system_instruction": system, "temperature": temperature}
    if schema is not None:
        options["response_mime_type"] = "application/json"
        options["response_schema"] = schema
    config = types.GenerateContentConfig(**options)

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL, contents=prompt, config=config
            )
            return response.text or ""
        except errors.APIError as e:
            if e.code not in RETRYABLE:
                raise  # client error (bad key/model): retrying won't help
            wait = 2 ** attempt
            print(f"Got {e.code}. Retry {attempt + 1}/{retries} in {wait}s...")
            time.sleep(wait)
    raise RuntimeError("LLM unavailable after retries")
