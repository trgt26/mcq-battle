from app.models import  Contests, Problems
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

async def _create_contest(db: AsyncSession, name: str, start_date: datetime):
    contest = Contests( 
                name=name, 
                start_date=start_date
            )
    db.add(contest)
    await db.commit()
    await db.refresh(contest)
    return contest

async def _get_contest(db: AsyncSession):
    result = await db.execute(select(Contests))
    return result.scalars().all()

async def _create_problem(db: AsyncSession, question: str, option_a: str, option_b: str, option_c: str, option_d: str, correct_answer: str):
    problem = Problems(
                question=question,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_answer=correct_answer
            )
    db.add(problem)
    await db.commit()
    await db.refresh(problem)
    return problem

async def _get_problem(db: AsyncSession):
    result = await db.execute(select(Problems))
    return result.scalars().all()

