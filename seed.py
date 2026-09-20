"""
Run once after the server has started (so tables exist):
    python seed.py

Creates a demo user + sample contacts/history so the dashboard has data to show.
"""
from database import SessionLocal, engine, Base
import models
import auth

Base.metadata.create_all(bind=engine)
db = SessionLocal()

email = "admin@trustvoice.ai"
user = db.query(models.User).filter(models.User.email == email).first()
if not user:
    user = models.User(email=email, password_hash=auth.hash_password("admin123"))
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created user: {email} / admin123")
else:
    print("Demo user already exists")

if not db.query(models.TrustedContact).filter(models.TrustedContact.user_id == user.id).first():
    db.add_all([
        models.TrustedContact(user_id=user.id, name="Priya Sharma", phone="+91 98765 43210", verified=True),
        models.TrustedContact(user_id=user.id, name="Rahul Verma", phone="+91 87654 32109", verified=True),
        models.TrustedContact(user_id=user.id, name="Ananya Singh", phone="+91 76543 21098", verified=False),
        models.TrustedContact(user_id=user.id, name="Vikram Patel", phone="+91 65432 10987", verified=True),
    ])
    db.commit()
    print("Seeded trusted contacts")

if not db.query(models.CallHistory).filter(models.CallHistory.user_id == user.id).first():
    db.add_all([
        models.CallHistory(user_id=user.id, caller_number="+91 98765 43210", risk_score=94, verdict="Impersonation"),
        models.CallHistory(user_id=user.id, caller_number="+91 87654 32109", risk_score=62, verdict="Suspicious"),
        models.CallHistory(user_id=user.id, caller_number="+91 76543 21098", risk_score=22, verdict="Verified"),
    ])
    db.commit()
    print("Seeded call history")

db.close()
