from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


# ===== User Schemas =====
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


# ===== User Profile Schemas (Input Features) =====
class UserProfileCreate(BaseModel):
    age: Optional[int] = Field(None, ge=1, le=120)
    gender: Optional[str] = None
    occupation: Optional[str] = None
    lifestyle: Optional[str] = None
    personality_type: Optional[str] = Field(None, description="introvert, extrovert, or ambivert")
    discipline_level: Optional[int] = Field(None, ge=1, le=10)
    preferred_work_hours: Optional[str] = None
    sleep_goal_hours: Optional[float] = Field(8.0, ge=4.0, le=12.0)
    exercise_preference: Optional[str] = None
    strengths: Optional[List[str]] = []
    weaknesses: Optional[List[str]] = []

class UserProfileUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=1, le=120)
    gender: Optional[str] = None
    occupation: Optional[str] = None
    lifestyle: Optional[str] = None
    personality_type: Optional[str] = None
    discipline_level: Optional[int] = Field(None, ge=1, le=10)
    preferred_work_hours: Optional[str] = None
    sleep_goal_hours: Optional[float] = Field(None, ge=4.0, le=12.0)
    exercise_preference: Optional[str] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None

class UserProfileOut(BaseModel):
    id: int
    user_id: int
    age: Optional[int]
    gender: Optional[str]
    occupation: Optional[str]
    lifestyle: Optional[str]
    personality_type: Optional[str]
    discipline_level: Optional[int]
    consistency_score: float
    preferred_work_hours: Optional[str]
    sleep_goal_hours: float
    exercise_preference: Optional[str]
    strengths: Optional[List[str]]
    weaknesses: Optional[List[str]]
    updated_at: datetime

    class Config:
        from_attributes = True


# ===== Goal Schemas (Input Features) =====
class GoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    goal_type: str = Field(..., description="short-term or long-term")
    category: str = Field(..., description="fitness, study, habit, career, etc.")
    target_value: float
    unit: str = Field(..., description="hours, days, count, etc.")
    target_date: Optional[datetime] = None

    @validator('goal_type')
    def validate_goal_type(cls, v):
        if v not in ['short-term', 'long-term']:
            raise ValueError('goal_type must be either short-term or long-term')
        return v

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    current_progress: Optional[float] = None
    completed: Optional[bool] = None

class GoalOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    goal_type: str
    category: str
    target_value: float
    current_progress: float
    unit: str
    start_date: datetime
    target_date: Optional[datetime]
    completed: bool
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


# ===== Habit Tracking Schemas (Input Features) =====
class HabitTrackingCreate(BaseModel):
    date: datetime
    sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    wake_up_time: Optional[str] = None
    sleep_time: Optional[str] = None
    work_study_hours: Optional[float] = Field(None, ge=0, le=24)
    exercise_minutes: Optional[int] = Field(None, ge=0)
    reading_minutes: Optional[int] = Field(0, ge=0)
    social_media_minutes: Optional[int] = Field(0, ge=0)
    gaming_minutes: Optional[int] = Field(0, ge=0)
    meditation_minutes: Optional[int] = Field(0, ge=0)
    meals_count: Optional[int] = Field(None, ge=0)
    water_intake_liters: Optional[float] = Field(None, ge=0)
    healthy_eating_score: Optional[int] = Field(None, ge=1, le=10)
    procrastination_level: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None

class HabitTrackingOut(BaseModel):
    id: int
    user_id: int
    date: datetime
    sleep_hours: Optional[float]
    wake_up_time: Optional[str]
    sleep_time: Optional[str]
    work_study_hours: Optional[float]
    exercise_minutes: Optional[int]
    reading_minutes: int
    social_media_minutes: int
    gaming_minutes: int
    meditation_minutes: int
    meals_count: Optional[int]
    water_intake_liters: Optional[float]
    healthy_eating_score: Optional[int]
    procrastination_level: Optional[int]
    notes: Optional[str]

    class Config:
        from_attributes = True


# ===== Productivity Log Schemas (Input Features) =====
class ProductivityLogCreate(BaseModel):
    date: datetime
    tasks_planned: int = Field(0, ge=0)
    tasks_completed: int = Field(0, ge=0)
    tasks_pending: int = Field(0, ge=0)
    deadlines_met: int = Field(0, ge=0)
    deadlines_missed: int = Field(0, ge=0)
    focus_time_minutes: int = Field(0, ge=0)
    distraction_count: int = Field(0, ge=0)
    productivity_score: Optional[int] = Field(None, ge=1, le=10)
    most_productive_hour: Optional[str] = None
    energy_level: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None

class ProductivityLogOut(BaseModel):
    id: int
    user_id: int
    date: datetime
    tasks_planned: int
    tasks_completed: int
    tasks_pending: int
    deadlines_met: int
    deadlines_missed: int
    focus_time_minutes: int
    distraction_count: int
    productivity_score: Optional[int]
    most_productive_hour: Optional[str]
    energy_level: Optional[int]
    notes: Optional[str]

    class Config:
        from_attributes = True


# ===== Mood Tracking Schemas (Input Features) =====
class MoodTrackingCreate(BaseModel):
    stress_level: int = Field(..., ge=1, le=10)
    happiness_level: int = Field(..., ge=1, le=10)
    energy_level: int = Field(..., ge=1, le=10)
    motivation_level: int = Field(..., ge=1, le=10)
    anxiety_level: int = Field(..., ge=1, le=10)
    mood_triggers: Optional[List[str]] = []
    mood_note: Optional[str] = None

class MoodTrackingOut(BaseModel):
    id: int
    user_id: int
    timestamp: datetime
    stress_level: int
    happiness_level: int
    energy_level: int
    motivation_level: int
    anxiety_level: int
    mood_triggers: Optional[List[str]]
    mood_note: Optional[str]

    class Config:
        from_attributes = True


# ===== Legacy Daily Log Schemas =====
class DailyLogCreate(BaseModel):
    date: str
    habits: str
    mood: str
    activities: str

class DailyLogOut(BaseModel):
    id: int
    date: str
    habits: str
    mood: str
    activities: str

    class Config:
        from_attributes = True


# ===== Chat Schemas =====
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    intent: Optional[str] = None
    timestamp: datetime


# ===== AI Model Capability Schemas (Outputs) =====
class UserProfileAnalysis(BaseModel):
    """2️⃣ AI Capability: User Profiling Output"""
    user_id: int
    profile_summary: str
    identified_strengths: List[str]
    identified_weaknesses: List[str]
    behavioral_patterns: List[str]
    consistency_score: float
    recommendations: List[str]

class PersonalizedRecommendation(BaseModel):
    """2️⃣ AI Capability: Personalized Recommendations"""
    recommendation_type: str  # habit, schedule, workout, relaxation
    title: str
    description: str
    reasoning: str
    priority: str  # high, medium, low
    actionable_steps: List[str]

class RoutinePrediction(BaseModel):
    """2️⃣ AI Capability: Routine Prediction"""
    date: datetime
    predicted_productive_hours: List[str]
    predicted_energy_levels: dict  # hour -> energy_level
    habit_predictions: dict  # habit_name -> likelihood (0-1)
    recommendations: List[str]

class HabitAnalytics(BaseModel):
    """2️⃣ AI Capability: Habit Analytics"""
    period: str  # week, month, year
    habits_summary: dict
    trends: dict  # improving, declining, stable
    streaks: dict  # habit -> streak_days
    insights: List[str]
    visualizations_data: Optional[dict] = None