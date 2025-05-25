from fastapi import FastAPI, Depends
from app.database import get_db
from app.crud import _create_contest, _get_contest, _create_problem, _get_problem
from datetime import datetime
from app.models import ProblemContestMappersCreate, ProblemContestMappers

app = FastAPI()

@app.post("/contest/")
async def create_contest(name: str, start_date: datetime, db=Depends(get_db)):
    return await _create_contest(db, name, start_date)

@app.get("/contest/")
async def get_contest(db=Depends(get_db)):
    return await _get_contest(db)

@app.post("/problems/")
async def create_problem(
    question: str, option_a: str, option_b: str, option_c: str, option_d: str, correct_answer: str, db=Depends(get_db)
    ):
    return await _create_problem(
        db, question, option_a, option_b, option_c, option_d, correct_answer)

@app.get("/problems/")
async def get_problem(db=Depends(get_db)):
    return await _get_problem(db)

@app.post("/contest/{contest_id}/problems/")
async def add_problem_to_contest(
    contest_id: int, problem_ids: ProblemContestMappersCreate, db=Depends(get_db)
):
    # Logic to add a problem to a contest
    problemContest = []
    msg = 0
    for problem_id in problem_ids.problem_id:
        problemContest.append(
            ProblemContestMappers(
                contest_id=contest_id,
                problem_id=problem_id
            )
        )
    db.add_all(problemContest)
    await db.commit()
    # This is a placeholder implementation
    return problemContest
    # return {"message": f"Problem {contest_id} added to Contest {contest_id}"}
