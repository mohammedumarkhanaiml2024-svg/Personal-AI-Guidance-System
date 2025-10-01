# Quick Start Guide 🚀

## Get Started in 3 Minutes!

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python -m uvicorn main_enhanced:app --reload
```

Server will start at: http://localhost:8000

### 3. Run the Demo
In a new terminal:
```bash
python demo_example.py
```

This will:
- Create a demo user
- Set up a profile
- Log sample data
- Demonstrate all AI capabilities

### 4. Explore the API
Visit http://localhost:8000/docs for interactive API documentation (Swagger UI)

---

## What You Get

### 1️⃣ Input Features (What You Track)
- ✅ Personal profile (age, occupation, personality)
- ✅ Daily habits (sleep, exercise, meditation, reading)
- ✅ Productivity (tasks, focus time, deadlines)
- ✅ Mood tracking (stress, happiness, energy)
- ✅ Goals (short-term & long-term)

### 2️⃣ AI Capabilities (What You Get)
- 🤖 **User Profiling** - AI analyzes your behavior
- 💡 **Personalized Recommendations** - Custom advice based on your data
- 🔮 **Routine Prediction** - Predict your productive hours
- 📊 **Habit Analytics** - Trends, streaks, and insights
- 💬 **AI Mentor Chatbot** - Talk to an AI that knows you

---

## Quick API Test

```python
import requests

# 1. Register
requests.post("http://localhost:8000/register", json={
    "username": "testuser",
    "password": "test123"
})

# 2. Login
response = requests.post("http://localhost:8000/token", data={
    "username": "testuser",
    "password": "test123"
})
token = response.json()["access_token"]

# 3. Get AI Recommendations
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/ai/recommendations", headers=headers)
print(response.json())
```

---

## File Structure

```
Personal-AI-Guidance-System/
├── models.py              # Database models (Input Features)
├── schemas.py             # Pydantic schemas (Validation)
├── ai_service.py          # AI capabilities implementation
├── main_enhanced.py       # FastAPI app with all endpoints
├── auth.py                # Authentication
├── database.py            # Database configuration
├── utils.py               # Encryption utilities
├── demo_example.py        # Complete demo script
├── requirements.txt       # Dependencies
└── README.md              # Full documentation
```

---

## Next Steps

1. **Customize Your Profile** - Update `/profile` with your real info
2. **Start Tracking** - Log your daily habits via `/habits`
3. **Set Goals** - Create goals using `/goals`
4. **Get Insights** - Check `/ai/profile-analysis` for insights
5. **Chat with AI** - Use `/ai/chat` for personalized guidance

---

## Common Issues

**Q: Import errors?**
```bash
pip install --upgrade -r requirements.txt
```

**Q: Database errors?**
- Delete `app.db` file and restart the server

**Q: JWT token expired?**
- Get a new token via `/token` endpoint

---

**Happy tracking! 🎯**
