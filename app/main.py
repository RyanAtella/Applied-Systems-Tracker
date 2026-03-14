from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserResponse, ApplicationCreate, ApplicationResponse
from app import models, schemas
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import logging
import sys

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://appliedsystemstracker.vercel.app"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Applied Systems Project API is running"}

@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    """
    Simple endpoint to verify database connectivity.
    """
    return {"database": "connected"}

@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    #Check if email already exists
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    #Create new user
    new_user = models.User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/applications", response_model=ApplicationResponse)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    
    new_application = models.Application(
        company=application.company,
        role=application.role,
        status=application.status,
        date_applied=application.date_applied,
        user_id=application.user_id
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application

@app.get("/users/{user_id}/applications")
def get_user_applications(user_id: int, db: Session = Depends(get_db)):
    #First check if user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    #Then get all applications
    applications = db.query(models.Application).filter(models.Application.user_id == user_id).all()
    return applications

@app.get("/applications")
def get_applications(db: Session = Depends(get_db)):
    try:
        applications = db.query(models.Application).all()
        return applications
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise


@app.get("/applications/{application_id}")
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return application

@app.put("/applications/{application_id}")
def update_application(application_id: int, application: schemas.ApplicationCreate, db: Session = Depends(get_db)):

    db_application = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()

    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db_application.company = application.company
    db_application.role = application.role
    db_application.status = application.status
    db_application.date_applied = application.date_applied

    db.commit()
    db.refresh(db_application)

    return db_application

@app.delete("/applications/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):

    application = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.delete(application)
    db.commit()

    return {"detail": "Application deleted"}
