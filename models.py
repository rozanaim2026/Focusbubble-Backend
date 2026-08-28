from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    login_type = Column(String, nullable=True)       # "google" or "guest"
    updated_at = Column(DateTime, nullable=True)
    schedules = relationship("Schedule", back_populates="owner", cascade="all,delete")
    sessions = relationship("FocusSession", back_populates="owner", cascade="all,delete")
    block_rules = relationship("BlockedApp", back_populates="owner", cascade="all,delete")

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    label = Column(String, default="Focus")
    duration_minutes = Column(Integer, default=25)
    apps_csv = Column(Text, default="")  # comma separated package names
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="schedules")


class FocusSession(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    paused = Column(Boolean, default=False)
    paused_at = Column(DateTime, nullable=True)
    remaining_seconds = Column(Integer, nullable=True)  # when paused
    status = Column(String, default="running")  # running, paused, finished, stopped

    owner = relationship("User", back_populates="sessions")


class BlockedApp(Base):
    __tablename__ = "blocked_apps"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    package_name = Column(String, nullable=False, index=True)
    app_name = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    owner = relationship("User", back_populates="block_rules")

class FocusStats(Base):
    __tablename__ = "focus_stats"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    all_time_minutes = Column(Integer, default=0)
    weekly_minutes = Column(Integer, default=0)
    completed_sessions = Column(Integer, default=0)
    last_week_reset = Column(DateTime, default=datetime.utcnow)

class UserStreak(Base):
    __tablename__ = "user_streak"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    current_streak = Column(Integer, default=0)
    last_session_date = Column(DateTime, nullable=True)


class SessionApp(Base):
    __tablename__ = "session_apps"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, index=True)
    app_id = Column(Integer, ForeignKey("apps.id"), nullable=False, index=True)
    app = relationship("App")
