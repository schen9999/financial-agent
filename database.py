import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ResearchBrief(Base):
    __tablename__ = "research_briefs"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    brief = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    job_id = Column(String(100), nullable=True)


def init_db():
    """Creates all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_brief(ticker: str, brief: str, job_id: str = None):
    """Saves a research brief to the database."""
    db = SessionLocal()
    try:
        record = ResearchBrief(
            ticker=ticker.upper(),
            brief=brief,
            job_id=job_id
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_briefs_by_ticker(ticker: str) -> list:
    """Retrieves all past research briefs for a given ticker."""
    db = SessionLocal()
    try:
        return db.query(ResearchBrief)\
            .filter(ResearchBrief.ticker == ticker.upper())\
            .order_by(ResearchBrief.created_at.desc())\
            .all()
    finally:
        db.close()


def get_recent_briefs(limit: int = 10) -> list:
    """Retrieves the most recent research briefs."""
    db = SessionLocal()
    try:
        return db.query(ResearchBrief)\
            .order_by(ResearchBrief.created_at.desc())\
            .limit(limit)\
            .all()
    finally:
        db.close()