import time

from llm import ask

SYSTEM = (
    "You are a strict technical interviewer for entry-level AI/ML roles. "
    "Ask exactly ONE question. No greeting, no markdown. Maximum 40 words."
)
PROMPT = "Ask me one question about machine learning fundamentals."
RUNS = 5

for temp in (1.0, 0.0):
    print(f"\n=== temperature={temp} ===")
    answers = []
    for i in range(RUNS):
        start = time.time()
        text = ask(PROMPT, system=SYSTEM, temperature=temp).strip()
        answers.append(text)
        print(f"{i + 1}. ({time.time() - start:.1f}s) {text}")
    print(f"--> {len(set(answers))} unique questions out of {RUNS}")
