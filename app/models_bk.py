from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Problems(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True)
    question = Column(String(255))   
    option_a = Column(String(255))           
    option_b = Column(String(255))           
    option_c = Column(String(255))           
    option_d = Column(String(255))   
    correct_answer = Column(String(255))   

class Contests(Base):
    __tablename__ = "contests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))   
    start_date = Column(DateTime, default=datetime.now(timezone.utc))

class Problem_contest_mappers(Base):
    __tablename__ = "problem_contest_mappers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    contest_id = Column(Integer, ForeignKey("contests.id"))   
    problem_id = Column(Integer, ForeignKey("problems.id"))

class submissions(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    contest_id = Column(Integer, ForeignKey("contests.id"))  


