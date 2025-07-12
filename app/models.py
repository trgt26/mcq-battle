from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Relationship


class Problems(SQLModel, table=True):
    __tablename__ = "problems"

    id: Optional[int] = Field(default=None, primary_key=True)
    question: str = Field(max_length=255)
    option_a: str = Field(max_length=255)
    option_b: str = Field(max_length=255)
    option_c: str = Field(max_length=255)
    option_d: str = Field(max_length=255)
    correct_answer: str = Field(max_length=255)


class Contests(SQLModel, table=True):
    __tablename__ = "contests"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    start_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProblemContestMappers(SQLModel, table=True):
    __tablename__ = "problem_contest_mappers"

    id: Optional[int] = Field(default=None, primary_key=True)
    contest_id: int = Field(foreign_key="contests.id")
    problem_id: int = Field(foreign_key="problems.id")


class ProblemContestMappersCreate(SQLModel):
    problem_id: List[int]


class Submissions(SQLModel, table=True):
    __tablename__ = "submissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    contest_id: int = Field(foreign_key="contests.id")


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, nullable=False)
    email: str = Field(max_length=100, unique=True, nullable=False)
    password: str = Field(max_length=100, unique=False, nullable=False)


class Results(SQLModel, table=True):
    __tablename__ = "results"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    contest_id: str = Field(max_length=100, nullable=False)
    score: int = Field(nullable=False)
