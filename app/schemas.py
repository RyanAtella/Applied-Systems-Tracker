from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from enum import Enum

class ApplicationStatus(str, Enum):
    Applied = "Applied"
    Interviewing = "Interviewing"
    Offered = "Offered"
    Rejected = "Rejected"
    Accepted = "Accepted"


class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: ApplicationStatus
    date_applied: date

class ApplicationResponse(BaseModel):
    id: int
    company: str
    role: str
    status: ApplicationStatus
    date_applied: date

    class Config:
        from_attributes = True

class UserWithApplications(UserResponse):
    applications: List[ApplicationResponse] = []

class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: ApplicationStatus
    date_applied: date

class ApplicationResponse(BaseModel):
    id: int
    company: str
    role: str
    status: ApplicationStatus
    date_applied: date

    class Config:
        from_attributes = True


