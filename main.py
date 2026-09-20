import random

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, get_db, Base
import models
import schemas
import auth

# Creates tables if they don't exist yet (fine for dev; use Alembic migrations for prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TrustVoice AI API")

# Allow the frontend (served from a different origin during dev) to call this API.
# Lock this down to your real domain before deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/signup", response_model=schemas.TokenResponse)
def signup(payload: schemas.SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        email=payload.email,
        password_hash=auth.hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": token}


@app.post("/api/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not auth.verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": token}


@app.get("/api/contacts", response_model=list[schemas.ContactOut])
def get_contacts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return (
        db.query(models.TrustedContact)
        .filter(models.TrustedContact.user_id == current_user.id)
        .all()
    )


@app.get("/api/history", response_model=list[schemas.HistoryOut])
def get_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return (
        db.query(models.CallHistory)
        .filter(models.CallHistory.user_id == current_user.id)
        .order_by(models.CallHistory.call_date.desc())
        .all()
    )


@app.post("/api/verify", response_model=schemas.VerifyResponse)
def verify_caller(
    payload: schemas.VerifyRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # Placeholder scoring — swap this block for your real voice/ML model call.
    risk_score = random.randint(0, 100)
    verdict = (
        "Blocked" if risk_score >= 80 else
        "Suspicious" if risk_score >= 50 else
        "Verified"
    )

    entry = models.CallHistory(
        user_id=current_user.id,
        caller_number=payload.caller_number,
        risk_score=risk_score,
        verdict=verdict,
    )
    db.add(entry)
    db.commit()

    return {"risk_score": risk_score, "verdict": verdict}


@app.get("/api/me")
def whoami(current_user: models.User = Depends(auth.get_current_user)):
    return {"id": current_user.id, "email": current_user.email}
