from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    clerk_id = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    email_verified = Column(Boolean, default=False)
    image = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    token = Column(String, unique=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="sessions")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, nullable=False)         # Provider's account ID
    provider_id = Column(String, nullable=False)        # e.g., "google", "outlook"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    id_token = Column(String, nullable=True)

    access_token_expires_at = Column(DateTime, nullable=True)
    refresh_token_expires_at = Column(DateTime, nullable=True)

    scope = Column(String, nullable=True)               # e.g., "email profile"
    password = Column(String, nullable=True)            # if password-based account

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # relationship back to user
    user = relationship("User", back_populates="accounts")



class Verification(Base):
    __tablename__ = "verification"
    
    
    id = Column(Integer, primary_key=True, index=True)
    indentifier = Column(String, nullable=False)
    value = Column(String, nullable=False)
    expiresAt = Column(DateTime(timezone=True), nullable=False, onupdate=func.now())
    createdAt = Column(DateTime(timezone=True), nullable=False, onupdate=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=False, onupdate=func.now())