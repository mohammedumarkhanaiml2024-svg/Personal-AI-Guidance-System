# Personal AI Guidance System 🤖

A comprehensive AI-powered personal guidance system that tracks your habits, analyzes your behavior, and provides personalized recommendations to help you achieve your goals.

## 📋 Table of Contents
- [Features Overview](#features-overview)
- [AI Model Features Explained](#ai-model-features-explained)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Security](#security)

---

## 🌟 Features Overview

This system implements a complete AI guidance solution with two main types of features:

### 1️⃣ Input Features (Data Collection)
These are the attributes and data points the system tracks about you:

| Category | Features |
|----------|----------|
| **Personal Info** | Age, gender, occupation, lifestyle |
| **Daily Routine** | Sleep hours, wake/sleep times, work/study hours, exercise |
| **Habits** | Reading, social media, gaming, meditation, water intake |
| **Behavior Traits** | Personality type (introvert/extrovert), discipline level, consistency |
| **Mood Tracking** | Stress, happiness, energy, motivation, anxiety levels |
| **Productivity** | Tasks completed/planned, deadlines, focus time, distractions |
| **Goals** | Short-term and long-term goals with progress tracking |

### 2️⃣ AI Capabilities (What the AI Does)
These are the intelligent features powered by machine learning and AI:

| Capability | Description |
|------------|-------------|
| **User Profiling** | Analyzes behavior to identify strengths, weaknesses, and patterns |
| **Personalized Recommendations** | Suggests habits, schedules, workouts based on your routine |
| **Routine Prediction** | Predicts your most productive hours and habit likelihood |
| **Habit Analytics** | Tracks trends, streaks, and provides actionable insights |
| **Conversational AI** | AI mentor chatbot for guidance, motivation, and support |
| **Adaptive Learning** | System learns from your feedback and improves over time |

---

## 🧠 AI Model Features Explained

### Input Features → How Data is Used

The system collects comprehensive data about your daily life:

```python
# Example: Daily Habit Tracking
{
  "date": "2025-10-01",
  "sleep_hours": 7.5,
  "wake_up_time": "06:30",
  "work_study_hours": 6.0,
  "exercise_minutes": 45,
  "reading_minutes": 30,
  "social_media_minutes": 120,
  "meditation_minutes": 15,
  "procrastination_level": 3
}
```

This data becomes **input features** for AI models that:
- Profile your behavior patterns
- Predict future habits
- Generate personalized recommendations
- Identify areas for improvement

### AI Capabilities → What You Get

#### 1. **User Profiling**
```
Profile Analysis for john_doe:
Consistency Score: 7.2/10

Key Strengths:
✓ Maintains healthy sleep schedule
✓ High task completion rate (78%)

Areas for Improvement:
⚠ Insufficient sleep (avg 6.2h/night)
⚠ Inconsistent exercise (30% of days)

Behavioral Patterns:
• Sleep deprivation pattern detected
```

#### 2. **Personalized Recommendations**
```json
{
  "recommendation_type": "schedule",
  "title": "Improve Sleep Schedule",
  "description": "You're averaging 6.2 hours of sleep. Try shifting your bedtime 30 minutes earlier.",
  "priority": "high",
  "actionable_steps": [
    "Set a bedtime alarm 30 minutes before target sleep time",
    "Avoid screens 1 hour before bed",
    "Create a calming bedtime routine"
  ]
}
```

#### 3. **Routine Prediction**
Predicts when you'll be most productive and which habits you're likely to maintain:
```json
{
  "predicted_productive_hours": ["09:00-10:00", "14:00-15:00"],
  "habit_predictions": {
    "exercise": 0.65,  // 65% chance you'll exercise
    "meditation": 0.85, // 85% chance you'll meditate
    "reading": 0.45
  }
}
```

#### 4. **Habit Analytics**
Comprehensive analytics with trends and insights:
```
Period: Last 30 Days

✓ Great sleep habits! You're averaging 7.5h/night
✓ Exercise routine is improving over time!
🔥 Amazing meditation streak of 14 days!
⚠ Social media usage increasing (avg 2.5h/day)
```

#### 5. **Conversational AI Mentor**
Chat with an AI that knows your context:
```
You: "I'm feeling stressed about work deadlines"

AI: "I can see your stress levels have been high lately (7.5/10). 
Here's what might help:
1. Your productivity peaks at 9-10 AM - schedule important tasks then
2. You've been skipping meditation - even 10 minutes can help
3. Your exercise streak was great last week - getting back to it 
   can reduce stress significantly.

Remember, you completed 78% of tasks last month. You've got this! 💪"
```

---

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLAlchemy + SQLite
- **AI**: Google Gemini API
- **Security**: 
  - JWT Authentication (jose)
  - Password Hashing (Argon2)
  - AES-256 Encryption (cryptography)
- **Data Validation**: Pydantic

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Personal-AI-Guidance-System.git
cd Personal-AI-Guidance-System
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn sqlalchemy pydantic python-jose[cryptography] passlib[argon2] cryptography requests
```

4. **Run the application**
```bash
# Use the enhanced version with all AI features
python -m uvicorn main_enhanced:app --reload
```

The API will be available at `http://localhost:8000`

5. **Access API documentation**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /register
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePass123"
}
```

#### Login
```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=SecurePass123
```

Returns JWT token for authenticated requests.

### Input Feature Endpoints (Data Collection)

#### 1. User Profile
```http
# Get profile
GET /profile
Authorization: Bearer <token>

# Update profile
PUT /profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "age": 28,
  "occupation": "Software Engineer",
  "personality_type": "introvert",
  "discipline_level": 7,
  "sleep_goal_hours": 8.0,
  "exercise_preference": "gym"
}
```

#### 2. Goals
```http
# Create goal
POST /goals
Authorization: Bearer <token>

{
  "title": "Daily Exercise",
  "goal_type": "short-term",
  "category": "fitness",
  "target_value": 30,
  "unit": "minutes",
  "target_date": "2025-12-31T00:00:00"
}

# Get goals
GET /goals?completed=false
Authorization: Bearer <token>
```

#### 3. Habit Tracking
```http
POST /habits
Authorization: Bearer <token>

{
  "date": "2025-10-01T00:00:00",
  "sleep_hours": 7.5,
  "wake_up_time": "06:30",
  "sleep_time": "23:00",
  "work_study_hours": 6.0,
  "exercise_minutes": 45,
  "reading_minutes": 30,
  "meditation_minutes": 15,
  "social_media_minutes": 90,
  "procrastination_level": 3
}
```

#### 4. Productivity Logs
```http
POST /productivity
Authorization: Bearer <token>

{
  "date": "2025-10-01T00:00:00",
  "tasks_planned": 8,
  "tasks_completed": 6,
  "deadlines_met": 2,
  "focus_time_minutes": 180,
  "productivity_score": 7,
  "most_productive_hour": "09:00-10:00"
}
```

#### 5. Mood Tracking
```http
POST /mood
Authorization: Bearer <token>

{
  "stress_level": 5,
  "happiness_level": 7,
  "energy_level": 6,
  "motivation_level": 8,
  "anxiety_level": 4,
  "mood_triggers": ["work", "exercise"],
  "mood_note": "Feeling good after morning workout"
}
```

### AI Capability Endpoints

#### 1. User Profile Analysis
```http
GET /ai/profile-analysis
Authorization: Bearer <token>

Response:
{
  "user_id": 1,
  "profile_summary": "Profile Analysis for john_doe...",
  "identified_strengths": [...],
  "identified_weaknesses": [...],
  "behavioral_patterns": [...],
  "consistency_score": 7.2,
  "recommendations": [...]
}
```

#### 2. Personalized Recommendations
```http
GET /ai/recommendations
Authorization: Bearer <token>

Response: [
  {
    "recommendation_type": "schedule",
    "title": "Improve Sleep Schedule",
    "description": "...",
    "reasoning": "...",
    "priority": "high",
    "actionable_steps": [...]
  }
]
```

#### 3. Routine Prediction
```http
GET /ai/predict-routine?date=2025-10-02T00:00:00
Authorization: Bearer <token>

Response:
{
  "date": "2025-10-02T00:00:00",
  "predicted_productive_hours": ["09:00-10:00", "14:00-15:00"],
  "predicted_energy_levels": {...},
  "habit_predictions": {
    "exercise": 0.65,
    "meditation": 0.85
  },
  "recommendations": [...]
}
```

#### 4. Habit Analytics
```http
GET /ai/habit-analytics?period=month
Authorization: Bearer <token>

Response:
{
  "period": "month",
  "habits_summary": {...},
  "trends": {...},
  "streaks": {...},
  "insights": [...],
  "visualizations_data": {...}
}
```

#### 5. Conversational AI Chat
```http
POST /ai/chat
Authorization: Bearer <token>

{
  "message": "I'm feeling stressed about work"
}

Response:
{
  "response": "I can see your stress levels...",
  "intent": "emotional_support",
  "timestamp": "2025-10-01T12:00:00"
}

# Get chat history
GET /ai/chat-history?limit=50
Authorization: Bearer <token>
```

---

## 💡 Usage Examples

### Complete User Journey

1. **Register and Login**
```python
import requests

# Register
response = requests.post("http://localhost:8000/register", json={
    "username": "alice",
    "password": "SecurePass123"
})

# Login
response = requests.post("http://localhost:8000/token", data={
    "username": "alice",
    "password": "SecurePass123"
})
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
```

2. **Set Up Profile**
```python
requests.put("http://localhost:8000/profile", headers=headers, json={
    "age": 25,
    "occupation": "Student",
    "personality_type": "ambivert",
    "discipline_level": 6,
    "exercise_preference": "yoga"
})
```

3. **Track Daily Habits**
```python
requests.post("http://localhost:8000/habits", headers=headers, json={
    "date": "2025-10-01T00:00:00",
    "sleep_hours": 7.0,
    "exercise_minutes": 30,
    "meditation_minutes": 20,
    "reading_minutes": 45
})
```

4. **Get AI Recommendations**
```python
response = requests.get("http://localhost:8000/ai/recommendations", headers=headers)
print(response.json())
```

5. **Chat with AI Mentor**
```python
response = requests.post("http://localhost:8000/ai/chat", headers=headers, json={
    "message": "How can I be more productive?"
})
print(response.json()["response"])
```

---

## 🔒 Security

### Authentication
- JWT tokens for secure API access
- Argon2 password hashing (industry standard)

### Data Protection
- AES-256 encryption for sensitive logs
- Encrypted data storage
- Per-user encryption keys

### Best Practices
- Change default encryption keys in production
- Use environment variables for API keys
- Enable HTTPS in production
- Implement rate limiting

---

## 📊 Database Schema

```
Users
├── UserProfile (1:1)
├── Goals (1:Many)
├── HabitTracking (1:Many)
├── ProductivityLog (1:Many)
├── MoodTracking (1:Many)
├── DailyLog (1:Many) [Legacy]
└── ChatHistory (1:Many)
```

---

## 🎯 Future Enhancements

- [ ] Machine learning models for better predictions
- [ ] Social features (compare with friends)
- [ ] Mobile app integration
- [ ] Wearable device integration (Fitbit, Apple Watch)
- [ ] Advanced visualizations and dashboards
- [ ] Export data to CSV/PDF
- [ ] Notification system for reminders
- [ ] Multi-language support

---

## 📝 License

MIT License - feel free to use this project for learning and personal use.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

## 🙏 Acknowledgments

- Google Gemini API for conversational AI
- FastAPI framework
- SQLAlchemy ORM
- The open-source community

---

**Built with ❤️ for better personal growth and self-improvement**