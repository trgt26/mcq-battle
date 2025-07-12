from fastapi import FastAPI, Depends, HTTPException, status
from app.database import get_db
from app.crud import _create_contest, _get_contest, _create_problem, _get_problem
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from datetime import datetime
from app.models import ProblemContestMappersCreate, ProblemContestMappers, User, Results, Contests, Problems
from typing import Annotated, List
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .database import engine



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



# Add these to your existing imports
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    async with AsyncSession(engine) as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if user is None:
            raise credentials_exception
        return user

@app.get("/contests/{contest_id}/problems", response_model=List[Problems])
async def get_contest_problems(
    contest_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user)  # This enforces JWT auth
):
    """Get all problems for a specific contest (JWT required)"""
    # Verify contest exists
    contest = await db.get(Contests, contest_id)
    if not contest:
        raise HTTPException(status_code=404, detail="Contest not found")
    
    # Get all problem IDs for this contest
    mapper_query = select(ProblemContestMappers).where(
        ProblemContestMappers.contest_id == contest_id
    )
    mapper_result = await db.execute(mapper_query)
    mappers = mapper_result.scalars().all()
    
    if not mappers:
        return []
    
    # Get all problems for these IDs
    problem_ids = [mapper.problem_id for mapper in mappers]
    problems_query = select(Problems).where(Problems.id.in_(problem_ids))
    problems_result = await db.execute(problems_query)
    problems = problems_result.scalars().all()
    
    return problems

# Route to create new user
@app.post("/register")
async def register_user(
    username: str,
    email: str,
    password: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Check if username or email already exists
    result = await db.execute(
        select(User).where((User.username == username) | (User.email == email))
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    # Create new user
    new_user = User(
        username=username,
        email=email,
        password=password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {"message": "User created successfully", "user_id": new_user.id}

# Token creation function
SECRET_KEY = "SECRET_KEY"  # Change this!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Modified login route with JWT
@app.post("/login")
async def login_user(
    username: str,
    password: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Find user by username
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Plain text password comparison (INSECURE - development only)
    if user.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@app.post("/results/", response_model=Results)
async def create_result(
    user_id: int,
    contest_id: str,
    score: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Create new result entry
    new_result = Results(
        user_id=user_id,
        contest_id=contest_id,
        score=score
    )
    
    # Optional: Verify user exists
    from .models import User  # Import your User model
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Add and commit
    db.add(new_result)
    await db.commit()
    await db.refresh(new_result)
    
    return new_result


