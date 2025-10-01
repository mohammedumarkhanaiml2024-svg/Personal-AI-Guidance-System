"""
Example Script: Personal AI Guidance System Demo
Demonstrates both Input Features and AI Capabilities
"""

import requests
from datetime import datetime, timedelta
import json

# Configuration
BASE_URL = "http://localhost:8000"
USERNAME = "demo_user"
PASSWORD = "DemoPass123"

class PersonalAIDemo:
    def __init__(self):
        self.token = None
        self.headers = {}
    
    def register_and_login(self):
        """Step 1: Register and authenticate"""
        print("=" * 60)
        print("STEP 1: REGISTRATION & AUTHENTICATION")
        print("=" * 60)
        
        # Register
        try:
            response = requests.post(f"{BASE_URL}/register", json={
                "username": USERNAME,
                "password": PASSWORD
            })
            print(f"✓ User registered: {response.json()}")
        except:
            print("ℹ User already exists, proceeding to login...")
        
        # Login
        response = requests.post(f"{BASE_URL}/token", data={
            "username": USERNAME,
            "password": PASSWORD
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
        print(f"✓ Logged in successfully! Token: {self.token[:30]}...")
        print()
    
    def setup_profile(self):
        """Step 2: Setup user profile (Input Features)"""
        print("=" * 60)
        print("STEP 2: USER PROFILE SETUP (1️⃣ Input Features)")
        print("=" * 60)
        
        profile_data = {
            "age": 28,
            "gender": "non-binary",
            "occupation": "Software Engineer",
            "lifestyle": "working professional",
            "personality_type": "introvert",
            "discipline_level": 7,
            "preferred_work_hours": "morning",
            "sleep_goal_hours": 8.0,
            "exercise_preference": "yoga",
            "strengths": ["analytical thinking", "problem solving"],
            "weaknesses": ["procrastination", "work-life balance"]
        }
        
        response = requests.put(f"{BASE_URL}/profile", headers=self.headers, json=profile_data)
        print("✓ Profile updated:")
        print(json.dumps(response.json(), indent=2))
        print()
    
    def create_goals(self):
        """Step 3: Set goals (Input Features)"""
        print("=" * 60)
        print("STEP 3: GOAL SETTING (1️⃣ Input Features)")
        print("=" * 60)
        
        goals = [
            {
                "title": "Daily Exercise",
                "description": "Exercise for at least 30 minutes",
                "goal_type": "short-term",
                "category": "fitness",
                "target_value": 30,
                "unit": "minutes",
                "target_date": (datetime.now() + timedelta(days=30)).isoformat()
            },
            {
                "title": "Learn AI/ML",
                "description": "Complete online AI course",
                "goal_type": "long-term",
                "category": "career",
                "target_value": 100,
                "unit": "hours",
                "target_date": (datetime.now() + timedelta(days=180)).isoformat()
            }
        ]
        
        for goal in goals:
            response = requests.post(f"{BASE_URL}/goals", headers=self.headers, json=goal)
            print(f"✓ Goal created: {goal['title']}")
        print()
    
    def log_daily_data(self):
        """Step 4: Log daily habits, productivity, mood (Input Features)"""
        print("=" * 60)
        print("STEP 4: DAILY DATA LOGGING (1️⃣ Input Features)")
        print("=" * 60)
        
        # Log habits for past 7 days to generate analytics
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            
            # Habit tracking
            habit_data = {
                "date": date.isoformat(),
                "sleep_hours": 7.0 + (i % 2) * 0.5,  # Varying sleep
                "wake_up_time": "06:30",
                "sleep_time": "23:00",
                "work_study_hours": 7.0,
                "exercise_minutes": 30 if i % 2 == 0 else 0,  # Exercise every other day
                "reading_minutes": 30,
                "social_media_minutes": 90,
                "meditation_minutes": 15 if i < 5 else 0,  # Meditation streak
                "meals_count": 3,
                "water_intake_liters": 2.5,
                "procrastination_level": 3 + (i % 3)
            }
            requests.post(f"{BASE_URL}/habits", headers=self.headers, json=habit_data)
            
            # Productivity log
            productivity_data = {
                "date": date.isoformat(),
                "tasks_planned": 8,
                "tasks_completed": 6 - (i % 3),  # Varying completion
                "deadlines_met": 2,
                "focus_time_minutes": 180,
                "productivity_score": 7 - (i % 2),
                "most_productive_hour": "09:00-10:00",
                "energy_level": 7
            }
            requests.post(f"{BASE_URL}/productivity", headers=self.headers, json=productivity_data)
            
            # Mood tracking
            mood_data = {
                "stress_level": 5 + (i % 4),
                "happiness_level": 7 - (i % 3),
                "energy_level": 6,
                "motivation_level": 7,
                "anxiety_level": 4,
                "mood_triggers": ["work", "exercise"],
                "mood_note": f"Day {i+1} mood log"
            }
            requests.post(f"{BASE_URL}/mood", headers=self.headers, json=mood_data)
        
        print("✓ Logged 7 days of habit data")
        print("✓ Logged 7 days of productivity data")
        print("✓ Logged 7 days of mood data")
        print()
    
    def get_ai_profile_analysis(self):
        """Step 5: AI Capability - User Profiling"""
        print("=" * 60)
        print("STEP 5: AI USER PROFILING (2️⃣ AI Capability)")
        print("=" * 60)
        
        response = requests.get(f"{BASE_URL}/ai/profile-analysis", headers=self.headers)
        analysis = response.json()
        
        print(f"Profile Summary:\n{analysis['profile_summary']}\n")
        print(f"Consistency Score: {analysis['consistency_score']}/10\n")
        
        print("Identified Strengths:")
        for strength in analysis['identified_strengths']:
            print(f"  ✓ {strength}")
        
        print("\nAreas for Improvement:")
        for weakness in analysis['identified_weaknesses']:
            print(f"  ⚠ {weakness}")
        
        print("\nRecommendations:")
        for rec in analysis['recommendations']:
            print(f"  → {rec}")
        print()
    
    def get_personalized_recommendations(self):
        """Step 6: AI Capability - Personalized Recommendations"""
        print("=" * 60)
        print("STEP 6: PERSONALIZED RECOMMENDATIONS (2️⃣ AI Capability)")
        print("=" * 60)
        
        response = requests.get(f"{BASE_URL}/ai/recommendations", headers=self.headers)
        recommendations = response.json()
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\nRecommendation {i}: {rec['title']}")
            print(f"Type: {rec['recommendation_type']} | Priority: {rec['priority']}")
            print(f"Description: {rec['description']}")
            print(f"Reasoning: {rec['reasoning']}")
            print("Actionable Steps:")
            for step in rec['actionable_steps']:
                print(f"  • {step}")
        print()
    
    def get_routine_prediction(self):
        """Step 7: AI Capability - Routine Prediction"""
        print("=" * 60)
        print("STEP 7: ROUTINE PREDICTION (2️⃣ AI Capability)")
        print("=" * 60)
        
        tomorrow = (datetime.now() + timedelta(days=1)).isoformat()
        response = requests.get(f"{BASE_URL}/ai/predict-routine?date={tomorrow}", headers=self.headers)
        prediction = response.json()
        
        print(f"Predictions for: {prediction['date']}\n")
        
        print("Predicted Productive Hours:")
        for hour in prediction['predicted_productive_hours']:
            print(f"  • {hour}")
        
        print("\nHabit Predictions (likelihood):")
        for habit, likelihood in prediction['habit_predictions'].items():
            percentage = likelihood * 100
            print(f"  • {habit.capitalize()}: {percentage:.0f}%")
        
        print("\nRecommendations:")
        for rec in prediction['recommendations']:
            print(f"  → {rec}")
        print()
    
    def get_habit_analytics(self):
        """Step 8: AI Capability - Habit Analytics"""
        print("=" * 60)
        print("STEP 8: HABIT ANALYTICS (2️⃣ AI Capability)")
        print("=" * 60)
        
        response = requests.get(f"{BASE_URL}/ai/habit-analytics?period=week", headers=self.headers)
        analytics = response.json()
        
        print(f"Analytics Period: {analytics['period']}\n")
        
        print("Habits Summary:")
        for key, value in analytics['habits_summary'].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        print("\nTrends:")
        for habit, trend in analytics['trends'].items():
            emoji = "📈" if trend == "improving" else "📉" if trend == "declining" else "➡️"
            print(f"  {emoji} {habit.capitalize()}: {trend}")
        
        print("\nCurrent Streaks:")
        for habit, days in analytics['streaks'].items():
            if days > 0:
                print(f"  🔥 {habit.capitalize()}: {days} days")
        
        print("\nInsights:")
        for insight in analytics['insights']:
            print(f"  {insight}")
        print()
    
    def chat_with_ai(self):
        """Step 9: AI Capability - Conversational AI"""
        print("=" * 60)
        print("STEP 9: CONVERSATIONAL AI MENTOR (2️⃣ AI Capability)")
        print("=" * 60)
        
        messages = [
            "How can I improve my productivity?",
            "I'm feeling stressed about work deadlines",
            "What's my progress on my fitness goals?"
        ]
        
        for msg in messages:
            print(f"\n👤 You: {msg}")
            response = requests.post(f"{BASE_URL}/ai/chat", headers=self.headers, json={
                "message": msg
            })
            ai_response = response.json()
            print(f"🤖 AI Mentor: {ai_response['response']}")
            print(f"   [Intent detected: {ai_response['intent']}]")
        print()
    
    def run_complete_demo(self):
        """Run all demo steps"""
        print("\n" + "=" * 60)
        print("PERSONAL AI GUIDANCE SYSTEM - COMPLETE DEMO")
        print("Demonstrating Input Features & AI Capabilities")
        print("=" * 60 + "\n")
        
        try:
            self.register_and_login()
            self.setup_profile()
            self.create_goals()
            self.log_daily_data()
            self.get_ai_profile_analysis()
            self.get_personalized_recommendations()
            self.get_routine_prediction()
            self.get_habit_analytics()
            self.chat_with_ai()
            
            print("=" * 60)
            print("DEMO COMPLETED SUCCESSFULLY! ✨")
            print("=" * 60)
            print("\nNext Steps:")
            print("1. Visit http://localhost:8000/docs for interactive API documentation")
            print("2. Explore all endpoints and customize your experience")
            print("3. Track your daily habits and watch the AI learn about you!")
            print("\n")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Make sure the server is running: python -m uvicorn main_enhanced:app --reload")


if __name__ == "__main__":
    demo = PersonalAIDemo()
    demo.run_complete_demo()
