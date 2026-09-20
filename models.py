from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    contacts = relationship("TrustedContact", back_populates="owner")
    history = relationship("CallHistory", back_populates="owner")


class TrustedContact(Base):
    __tablename__ = "trusted_contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    phone = Column(String)
    verified = Column(Boolean, default=False)

    owner = relationship("User", back_populates="contacts")


class CallHistory(Base):
    __tablename__ = "call_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    caller_number = Column(String)
    call_date = Column(TIMESTAMP, server_default=func.now())
    risk_score = Column(Integer)
    verdict = Column(String)

    owner = relationship("User", back_populates="history")
