from pydantic import BaseModel, ValidationError

from llm import ask


class Question(BaseModel):
    id: int
    topic: str
    question: str


class QuestionSet(BaseModel):
    questions: list[Question]


SYSTEM = (
    "You are a strict technical interviewer for entry-level AI/ML roles. "
    "Each question must be a single question of at most 40 words, "
    "with no greeting and no markdown."
)


def generate_questions(role: str, n: int = 5) -> QuestionSet:
    prompt = f"Generate exactly {n} different interview questions for an entry-level {role} role."
    text = ask(prompt, system=SYSTEM, temperature=0.7, schema=QuestionSet)
    try:
        result = QuestionSet.model_validate_json(text)
    except ValidationError as e:
        raise ValueError(f"Model returned invalid JSON shape: {e}") from e
    if len(result.questions) != n:
        raise ValueError(f"Expected {n} questions, got {len(result.questions)}")
    return result


if __name__ == "__main__":
    result = generate_questions("AI/ML engineer")
    for q in result.questions:
        print(f"{q.id}. [{q.topic}] {q.question}")
