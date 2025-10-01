from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    daily_logs = relationship("DailyLog", back_populates="user")
    chat_history = relationship("ChatHistory", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    habit_tracking = relationship("HabitTracking", back_populates="user")
    productivity_logs = relationship("ProductivityLog", back_populates="user")
    mood_tracking = relationship("MoodTracking", back_populates="user")


class UserProfile(Base):
    """
    1️⃣ Features as Inputs - Personal Information & Behavior Traits
    Stores user demographics, lifestyle, and personality traits
    """
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Personal Info
    age = Column(Integer)
    gender = Column(String)
    occupation = Column(String)
    lifestyle = Column(String)  # e.g., "student", "working professional", "freelancer"
    
    # Behavior Traits
    personality_type = Column(String)  # e.g., "introvert", "extrovert", "ambivert"
    discipline_level = Column(Integer)  # 1-10 scale
    consistency_score = Column(Float, default=0.0)  # Calculated from habit tracking
    
    # Preferences
    preferred_work_hours = Column(String)  # e.g., "morning", "night", "flexible"
    sleep_goal_hours = Column(Float, default=8.0)
    exercise_preference = Column(String)  # e.g., "gym", "yoga", "running", "none"
    
    # Metadata
    strengths = Column(JSON)  # List of identified strengths
    weaknesses = Column(JSON)  # List of identified weaknesses
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="profile")


class Goal(Base):
    """
    1️⃣ Features as Inputs - User Goals
    Short-term and long-term goals for tracking and recommendations
    """
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    title = Column(String, nullable=False)
    description = Column(Text)
    goal_type = Column(String)  # "short-term", "long-term"
    category = Column(String)  # "fitness", "study", "habit", "career", etc.
    target_value = Column(Float)  # e.g., "2" for 2 hours/day
    current_progress = Column(Float, default=0.0)
    unit = Column(String)  # "hours", "days", "count", etc.
    
    start_date = Column(DateTime, default=datetime.utcnow)
    target_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    
    user = relationship("User", back_populates="goals")


class HabitTracking(Base):
    """
    1️⃣ Features as Inputs - Daily Habits
    Track user habits like reading, social media, gaming, meditation, etc.
    """
    __tablename__ = "habit_tracking"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    
    # Daily Routine
    sleep_hours = Column(Float)
    wake_up_time = Column(String)  # e.g., "06:30"
    sleep_time = Column(String)  # e.g., "22:00"
    work_study_hours = Column(Float)
    exercise_minutes = Column(Integer)
    
    # Habits (minutes/day)
    reading_minutes = Column(Integer, default=0)
    social_media_minutes = Column(Integer, default=0)
    gaming_minutes = Column(Integer, default=0)
    meditation_minutes = Column(Integer, default=0)
    
    # Eating patterns
    meals_count = Column(Integer)  # Number of meals
    water_intake_liters = Column(Float)
    healthy_eating_score = Column(Integer)  # 1-10 scale
    
    # Procrastination tracking
    procrastination_level = Column(Integer)  # 1-10 scale
    
    # Notes
    notes = Column(Text)
    
    user = relationship("User", back_populates="habit_tracking")


class ProductivityLog(Base):
    """
    1️⃣ Features as Inputs - Productivity Data
    Track tasks, deadlines, focus time, and productivity metrics
    """
    __tablename__ = "productivity_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    
    # Task tracking
    tasks_planned = Column(Integer, default=0)
    tasks_completed = Column(Integer, default=0)
    tasks_pending = Column(Integer, default=0)
    deadlines_met = Column(Integer, default=0)
    deadlines_missed = Column(Integer, default=0)
    
    # Focus & productivity
    focus_time_minutes = Column(Integer, default=0)  # Deep work time
    distraction_count = Column(Integer, default=0)
    productivity_score = Column(Integer)  # 1-10 scale
    
    # Peak performance tracking
    most_productive_hour = Column(String)  # e.g., "09:00-10:00"
    energy_level = Column(Integer)  # 1-10 scale
    
    notes = Column(Text)
    
    user = relationship("User", back_populates="productivity_logs")


class MoodTracking(Base):
    """
    1️⃣ Features as Inputs - Mood & Emotional State
    Daily mood logs for stress, happiness, energy tracking
    """
    __tablename__ = "mood_tracking"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Mood metrics (1-10 scale)
    stress_level = Column(Integer)
    happiness_level = Column(Integer)
    energy_level = Column(Integer)
    motivation_level = Column(Integer)
    anxiety_level = Column(Integer)
    
    # Context
    mood_triggers = Column(JSON)  # List of triggers (work, personal, health, etc.)
    mood_note = Column(Text)
    
    user = relationship("User", back_populates="mood_tracking")


class DailyLog(Base):
    """Legacy daily logs - kept for backward compatibility"""
    __tablename__ = "daily_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime)
    habits = Column(Text)
    mood = Column(String)
    activities = Column(Text)
    encrypted = Column(Text)  # For AES-256 encrypted log

    user = relationship("User", back_populates="daily_logs")


class ChatHistory(Base):
    """Conversational AI chat history"""
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String)  # "user" or "assistant"
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # AI metadata
    intent = Column(String)  # detected intent (motivation, advice, analytics, etc.)
    sentiment = Column(String)  # positive, negative, neutral

    user = relationship("User", back_populates="chat_history")