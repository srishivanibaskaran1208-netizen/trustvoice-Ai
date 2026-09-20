from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class ContactOut(BaseModel):
    id: int
    name: str
    phone: str
    verified: bool

    class Config:
        from_attributes = True


class HistoryOut(BaseModel):
    id: int
    caller_number: str
    call_date: datetime
    risk_score: int
    verdict: str

    class Config:
        from_attributes = True


class VerifyRequest(BaseModel):
    caller_number: str


class VerifyResponse(BaseModel):
    risk_score: int
    verdict: str
