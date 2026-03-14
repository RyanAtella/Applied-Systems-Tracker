from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1. Database connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

#2. Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

#3. Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#4. Base class for models
Base = declarative_base()

#5. Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:        
        db.close()
