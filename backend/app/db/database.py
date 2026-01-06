import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------
# Load .env explicitly from backend root
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not found. Check .env location.")

# -------------------------------------------------
# SQLAlchemy Engine
# -------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# -------------------------------------------------
# Session Factory
# -------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -------------------------------------------------
# Base Model
# -------------------------------------------------
Base = declarative_base()

# -------------------------------------------------
# ✅ FastAPI DB Dependency (THIS FIXES YOUR ERROR)
# -------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
