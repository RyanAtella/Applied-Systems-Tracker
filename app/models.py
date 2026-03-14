from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.schemas import ApplicationStatus


#__tablename__ -> SQL table name
#id -> primary key, auto-incrementing integer
#name -> string column for user's name
#email -> unique string column for user's email address
#index -> makes searching by ID faster
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    applications = relationship("Application", back_populates="user", cascade="all, delete")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    status = Column(Enum(ApplicationStatus), nullable=False)
    date_applied = Column(Date, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id")) #links to user table
    user = relationship("User", back_populates="applications")

