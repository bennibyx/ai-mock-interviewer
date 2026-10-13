from fastapi import FastAPI, HTTPException, Query

from questions import QuestionSet, generate_questions

app = FastAPI(title="AI Mock Interviewer")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/questions", response_model=QuestionSet)
def get_questions(
    role: str = Query("AI/ML engineer", max_length=80),
    n: int = Query(5, ge=1, le=10),
):
    try:
        return generate_questions(role, n)
    except ValueError as e:  # model returned the wrong shape or count
        raise HTTPException(status_code=502, detail=str(e))
    except RuntimeError as e:  # API stayed unavailable after retries
        raise HTTPException(status_code=503, detail=str(e))
