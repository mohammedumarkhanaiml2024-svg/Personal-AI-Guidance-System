"""
Enhanced Personal AI Guidance System API
Implements comprehensive endpoints for all features (inputs & capabilities)
"""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

import models
import schemas
import auth
import database
import utils
from ai_service import AIGuidanceService
from brain_service import PersonalBrainService

# Initialize FastAPI app
app = FastAPI(
    title="Personal AI Guidance System",
    description="AI-powered personal guidance with habit tracking, analytics, and conversational support",
    version="2.0.0"
)

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # Allow all origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Global exception handler to ensure CORS headers on errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Ensure CORS headers are sent even on unhandled exceptions"""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
        }
    )

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Initialize services
brain_service = PersonalBrainService()

# Initialize privacy service for complete data isolation
from data_privacy_service import DataPrivacyService
privacy_service = DataPrivacyService()

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# For demo, use a static key. In production, generate/store per user.
DEMO_AES_KEY = "0lQj7QJOdAc5wC9wHTnyz6j0wW5e4LxYBCr3GQ1KQnA="  # 32-byte base64 key


# ========== Dependencies ==========
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Decode JWT token and return current user"""
    from jose import jwt, JWTError
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user


# ========== Root & Health Check Endpoints ==========
@app.get("/")
def root():
    """Root endpoint - API info"""
    return {
        "message": "Personal AI Guidance System API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cors_enabled": True
    }


# ========== Authentication Endpoints ==========
@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserRegistrationWithInfo, db: Session = Depends(get_db)):
    """Register a new user with private data space and optional personal information"""
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = auth.hash_password(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create default profile
    profile = models.UserProfile(user_id=new_user.id)
    db.add(profile)
    db.commit()
    
    # Create isolated private data space for the new user
    private_space = privacy_service.create_user_private_space(new_user.id)
    print(f"Created private data space for user {new_user.id}: {private_space}")
    
    # Store personal information in user's private brain file if provided
    if user.personal_info:
        brain_service = PersonalBrainService()
        brain = brain_service.get_user_brain(new_user.id)
        
        # Add personal information to brain
        brain["personal_info"] = {
            **user.personal_info.dict(exclude_unset=True),
            "collected_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        brain_service._save_brain(new_user.id, brain)
        print(f"Stored personal information for user {new_user.id}")
    
    return new_user
    
    return new_user


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token"""
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# ========== User Profile Endpoints (Input Features) ==========
@app.get("/profile", response_model=schemas.UserProfileOut)
def get_profile(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user profile"""
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@app.put("/profile", response_model=schemas.UserProfileOut)
def update_profile(
    profile_data: schemas.UserProfileUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Update fields
    for field, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    
    profile.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(profile)
    return profile


# ========== Personal Information Endpoints (Stored in Brain) ==========
@app.get("/profile/personal-info", response_model=schemas.PersonalInfoOut)
def get_personal_info(current_user: models.User = Depends(get_current_user)):
    """Get user's personal information from their private brain file"""
    brain_service = PersonalBrainService()
    brain = brain_service.get_user_brain(current_user.id)
    
    # Return personal info or empty dict if not set
    personal_info = brain.get("personal_info", {})
    return schemas.PersonalInfoOut(**personal_info)


@app.put("/profile/personal-info", response_model=schemas.PersonalInfoOut)
def update_personal_info(
    personal_data: schemas.PersonalInfoUpdate,
    current_user: models.User = Depends(get_current_user)
):
    """Update user's personal information in their private brain file"""
    brain_service = PersonalBrainService()
    brain = brain_service.get_user_brain(current_user.id)
    
    # Get existing personal info or create new
    if "personal_info" not in brain:
        brain["personal_info"] = {
            "collected_at": datetime.now().isoformat()
        }
    
    # Update with new data (only fields that are set)
    update_data = personal_data.dict(exclude_unset=True)
    brain["personal_info"].update(update_data)
    brain["personal_info"]["last_updated"] = datetime.now().isoformat()
    
    # Save brain
    brain_service._save_brain(current_user.id, brain)
    
    return schemas.PersonalInfoOut(**brain["personal_info"])


@app.post("/profile/personal-info", response_model=schemas.PersonalInfoOut)
def create_personal_info(
    personal_data: schemas.PersonalInfoCreate,
    current_user: models.User = Depends(get_current_user)
):
    """Create/overwrite user's personal information in their private brain file"""
    brain_service = PersonalBrainService()
    brain = brain_service.get_user_brain(current_user.id)
    
    # Create new personal info
    brain["personal_info"] = {
        **personal_data.dict(exclude_unset=True),
        "collected_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat()
    }
    
    # Save brain
    brain_service._save_brain(current_user.id, brain)
    
    return schemas.PersonalInfoOut(**brain["personal_info"])


# ========== Goals Endpoints (Input Features) ==========
@app.post("/goals", response_model=schemas.GoalOut)
def create_goal(
    goal: schemas.GoalCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new goal"""
    new_goal = models.Goal(
        user_id=current_user.id,
        **goal.dict()
    )
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal


@app.get("/goals", response_model=List[schemas.GoalOut])
def get_goals(
    completed: Optional[bool] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all user goals, optionally filter by completion status"""
    query = db.query(models.Goal).filter(models.Goal.user_id == current_user.id)
    
    if completed is not None:
        query = query.filter(models.Goal.completed == completed)
    
    return query.all()


@app.put("/goals/{goal_id}", response_model=schemas.GoalOut)
def update_goal(
    goal_id: int,
    goal_update: schemas.GoalUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a goal"""
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    for field, value in goal_update.dict(exclude_unset=True).items():
        setattr(goal, field, value)
    
    # If marked as completed, set completion timestamp
    if goal_update.completed and not goal.completed_at:
        goal.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(goal)
    return goal


# ========== Habit Tracking Endpoints (Input Features) ==========
@app.post("/habits", response_model=schemas.HabitTrackingOut)
def create_habit_log(
    habit: schemas.HabitTrackingCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log daily habits"""
    new_habit = models.HabitTracking(
        user_id=current_user.id,
        **habit.dict()
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    
    # Update user's personal brain with new habit data
    brain_service.update_brain_with_habit(current_user.id, habit.dict())
    
    return new_habit


@app.get("/habits", response_model=List[schemas.HabitTrackingOut])
def get_habits(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 30,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get habit logs with optional date filtering"""
    query = db.query(models.HabitTracking).filter(models.HabitTracking.user_id == current_user.id)
    
    if start_date:
        query = query.filter(models.HabitTracking.date >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(models.HabitTracking.date <= datetime.fromisoformat(end_date))
    
    return query.order_by(models.HabitTracking.date.desc()).limit(limit).all()


# ========== Productivity Endpoints (Input Features) ==========
@app.post("/productivity", response_model=schemas.ProductivityLogOut)
def create_productivity_log(
    productivity: schemas.ProductivityLogCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log productivity data"""
    new_log = models.ProductivityLog(
        user_id=current_user.id,
        **productivity.dict()
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    # Update user's personal brain with productivity data
    brain_service.update_brain_with_productivity(current_user.id, productivity.dict())
    
    return new_log


@app.get("/productivity", response_model=List[schemas.ProductivityLogOut])
def get_productivity_logs(
    limit: int = 30,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get productivity logs"""
    return db.query(models.ProductivityLog).filter(
        models.ProductivityLog.user_id == current_user.id
    ).order_by(models.ProductivityLog.date.desc()).limit(limit).all()


# ========== Mood Tracking Endpoints (Input Features) ==========
@app.post("/mood", response_model=schemas.MoodTrackingOut)
def create_mood_log(
    mood: schemas.MoodTrackingCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log current mood"""
    new_mood = models.MoodTracking(
        user_id=current_user.id,
        **mood.dict()
    )
    db.add(new_mood)
    db.commit()
    db.refresh(new_mood)
    
    # Update user's personal brain with mood data
    brain_service.update_brain_with_mood(current_user.id, mood.dict())
    
    return new_mood


@app.get("/mood", response_model=List[schemas.MoodTrackingOut])
def get_mood_logs(
    limit: int = 30,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get mood logs"""
    return db.query(models.MoodTracking).filter(
        models.MoodTracking.user_id == current_user.id
    ).order_by(models.MoodTracking.timestamp.desc()).limit(limit).all()


# ========== AI Capabilities Endpoints ==========

@app.get("/ai/profile-analysis", response_model=schemas.UserProfileAnalysis)
def get_profile_analysis(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    2️⃣ AI Capability: User Profiling
    Get comprehensive profile analysis with strengths, weaknesses, and patterns
    """
    ai_service = AIGuidanceService(db)
    return ai_service.generate_user_profile_analysis(current_user.id)


@app.get("/ai/recommendations", response_model=List[schemas.PersonalizedRecommendation])
def get_recommendations(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    2️⃣ AI Capability: Personalized Recommendations
    Get personalized recommendations for habits, schedules, and workouts
    """
    ai_service = AIGuidanceService(db)
    return ai_service.generate_personalized_recommendations(current_user.id)


@app.get("/ai/predict-routine", response_model=schemas.RoutinePrediction)
def predict_routine(
    date: Optional[str] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    2️⃣ AI Capability: Routine Prediction
    Predict productivity patterns and habit likelihood for a given date
    """
    prediction_date = datetime.fromisoformat(date) if date else datetime.now() + timedelta(days=1)
    ai_service = AIGuidanceService(db)
    return ai_service.predict_routine(current_user.id, prediction_date)


@app.get("/ai/habit-analytics", response_model=schemas.HabitAnalytics)
def get_habit_analytics(
    period: str = "month",
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    2️⃣ AI Capability: Habit Analytics
    Get comprehensive habit analytics with trends, streaks, and insights
    Period options: week, month, year
    """
    if period not in ["week", "month", "year"]:
        raise HTTPException(status_code=400, detail="Period must be 'week', 'month', or 'year'")
    
    ai_service = AIGuidanceService(db)
    return ai_service.generate_habit_analytics(current_user.id, period)


@app.post("/ai/chat", response_model=schemas.ChatResponse)
def chat_with_ai(
    message: schemas.ChatMessage,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    2️⃣ AI Capability: Conversational AI
    Chat with AI mentor for guidance, motivation, and support
    """
    ai_service = AIGuidanceService(db)
    
    # Get recent context for better responses
    recent_mood = db.query(models.MoodTracking).filter(
        models.MoodTracking.user_id == current_user.id
    ).order_by(models.MoodTracking.timestamp.desc()).first()
    
    context = {}
    if recent_mood:
        context["latest_mood"] = {
            "stress": recent_mood.stress_level,
            "happiness": recent_mood.happiness_level,
            "energy": recent_mood.energy_level
        }
    
    response = ai_service.chat_with_ai(current_user.id, message.message, context)
    
    # Save chat history
    user_chat = models.ChatHistory(
        user_id=current_user.id,
        role="user",
        message=message.message,
        timestamp=datetime.utcnow()
    )
    ai_chat = models.ChatHistory(
        user_id=current_user.id,
        role="assistant",
        message=response["response"],
        intent=response["intent"],
        timestamp=response["timestamp"]
    )
    db.add(user_chat)
    db.add(ai_chat)
    db.commit()
    
    return response


@app.get("/ai/chat-history")
def get_chat_history(
    limit: int = 50,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat history"""
    history = db.query(models.ChatHistory).filter(
        models.ChatHistory.user_id == current_user.id
    ).order_by(models.ChatHistory.timestamp.desc()).limit(limit).all()
    
    return [
        {
            "role": h.role,
            "message": h.message,
            "timestamp": h.timestamp,
            "intent": h.intent
        }
        for h in reversed(history)
    ]


# ========== Legacy Endpoints (Backward Compatibility) ==========
@app.post("/logs")
def create_log(
    log: schemas.DailyLogCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Legacy daily log endpoint with encryption"""
    log_plain = f"Habit: {log.habits}\nMood: {log.mood}\nActivities: {log.activities}"
    encrypted = utils.encrypt_data(DEMO_AES_KEY, log_plain)
    db_log = models.DailyLog(
        user_id=current_user.id,
        date=datetime.strptime(log.date, "%Y-%m-%d"),
        habits=log.habits,
        mood=log.mood,
        activities=log.activities,
        encrypted=encrypted,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return {"msg": "Log saved securely", "id": db_log.id}


@app.get("/logs/{log_id}")
def get_log(
    log_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Legacy get log endpoint with decryption"""
    db_log = db.query(models.DailyLog).filter_by(
        id=log_id, user_id=current_user.id
    ).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    decrypted = utils.decrypt_data(DEMO_AES_KEY, db_log.encrypted)
    return {"log": decrypted}


# ========== Health Check ==========
@app.get("/")
def root():
    """API health check"""
    return {
        "status": "online",
        "app": "Personal AI Guidance System",
        "version": "2.0.0",
        "features": {
            "input_features": [
                "User Profile",
                "Goals Tracking",
                "Habit Tracking",
                "Productivity Logs",
                "Mood Tracking"
            ],
            "ai_capabilities": [
                "User Profiling & Analysis",
                "Personalized Recommendations",
                "Routine Prediction",
                "Habit Analytics",
                "Conversational AI Mentor",
                "Personal Brain Learning System"
            ]
        }
    }


# ========== PERSONAL BRAIN ENDPOINTS (Privacy Enhanced) ==========

@app.get("/brain/summary")
def get_brain_summary(current_user: models.User = Depends(get_current_user)):
    """Get user's brain summary with complete data isolation"""
    return privacy_service.get_ai_brain_summary(current_user.id)


@app.get("/brain/context")
def get_brain_context(current_user: models.User = Depends(get_current_user)):
    """Get full brain context for debugging/viewing (user's private data only)"""
    return brain_service.get_user_brain(current_user.id)


@app.post("/brain/chat")
def chat_with_personal_brain(
    message: schemas.ChatMessage,
    current_user: models.User = Depends(get_current_user)
):
    """Chat using personal brain context - fully personalized responses with data isolation"""
    return privacy_service.chat_with_ai(current_user.id, message.message)
    
    # Save conversation to brain
    brain_service.update_brain_with_conversation(
        current_user.id,
        message.message,
        response
    )
    
    return {"response": response, "brain_powered": True}


@app.post("/brain/goal")
def set_personal_goal(
    goal: str,
    target: str,
    current_user: models.User = Depends(get_current_user)
):
    """Set a personal goal in brain"""
    brain = brain_service.set_user_goal(current_user.id, goal, target)
    return {"message": "Goal set in personal brain", "goals": brain["goals_progress"]}


@app.post("/brain/achievement")
def add_personal_achievement(
    achievement: str,
    current_user: models.User = Depends(get_current_user)
):
    """Add achievement to brain"""
    brain = brain_service.add_achievement(current_user.id, achievement)
    return {"message": "Achievement added", "achievements": brain["achievements"]}


@app.post("/brain/challenge")
def identify_personal_challenge(
    challenge: str,
    current_user: models.User = Depends(get_current_user)
):
    """Identify a challenge in brain"""
    brain = brain_service.identify_challenge(current_user.id, challenge)
    return {"message": "Challenge identified", "challenges": brain["challenges"]}


# ========== DATA PRIVACY & ISOLATION ENDPOINTS ==========

@app.get("/privacy/verification")
def verify_data_privacy(current_user: models.User = Depends(get_current_user)):
    """Verify that user's data is completely isolated and private"""
    return privacy_service.verify_user_data_isolation(current_user.id)


@app.get("/privacy/analytics")
def get_private_analytics(current_user: models.User = Depends(get_current_user)):
    """Get analytics from user's private data only (no mixing with other users)"""
    return privacy_service.get_user_analytics(current_user.id)


@app.get("/privacy/summary")
def get_privacy_implementation():
    """Get information about privacy implementation and data isolation"""
    return privacy_service.get_data_privacy_summary()


@app.delete("/privacy/delete-all-data")
def delete_all_user_data(current_user: models.User = Depends(get_current_user)):
    """GDPR Compliance: Completely delete all user data"""
    return privacy_service.delete_all_user_data(current_user.id)


@app.post("/privacy/create-space")
def create_private_space(current_user: models.User = Depends(get_current_user)):
    """Manually create/recreate private data space for user"""
    return privacy_service.create_user_private_space(current_user.id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
