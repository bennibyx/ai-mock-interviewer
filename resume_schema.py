from typing import Literal
from pydantic import BaseModel, Field


class Skill(BaseModel):
    name: str
    level: Literal["listed_only", "used_in_project", "used_in_work"]
    evidence: str = Field(description="Project or job where it was used, or 'none'")


class Project(BaseModel):
    name: str
    tech: list[str]
    what_they_did: str
    stated_results: list[str] = Field(description="Numbers/outcomes written in the resume, else empty")


class Experience(BaseModel):
    role: str
    organization: str
    duration: str | None = None
    responsibilities: list[str]
    stated_results: list[str] = Field(description="Outcomes written in the resume, else empty")


class ParsedResume(BaseModel):
    name: str | None = None
    skills: list[Skill]
    projects: list[Project]
    experience: list[Experience]
    education: str | None = None
    certifications: list[str] = []
