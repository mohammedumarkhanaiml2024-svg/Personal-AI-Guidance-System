"""
Personal Brain Service - Individual AI Learning System
Each user has their own private brain file that learns and adapts from their data only.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
import models

class PersonalBrainService:
    """Manages individual user brain files for personalized AI responses"""
    
    BRAIN_DIR = "user_brains"
    
    def __init__(self):
        # Create brain directory if it doesn't exist
        os.makedirs(self.BRAIN_DIR, exist_ok=True)
    
    def _get_brain_path(self, user_id: int) -> str:
        """Get the file path for a user's brain file"""
        return os.path.join(self.BRAIN_DIR, f"user_{user_id}_brain.json")
    
    def get_user_brain(self, user_id: int) -> Dict:
        """Load user's brain file or create new one if doesn't exist"""
        brain_path = self._get_brain_path(user_id)
        
        if os.path.exists(brain_path):
            with open(brain_path, 'r') as f:
                return json.load(f)
        else:
            # Create new brain for user
            new_brain = {
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "learning_history": [],
                "personality_insights": {},
                "behavior_patterns": {},
                "preferences": {},
                "goals_progress": {},
                "habit_memory": {},
                "conversation_context": [],
                "achievements": [],
                "challenges": [],
                "growth_areas": []
            }
            self._save_brain(user_id, new_brain)
            return new_brain
    
    def _save_brain(self, user_id: int, brain_data: Dict):
        """Save user's brain file"""
        brain_path = self._get_brain_path(user_id)
        brain_data["last_updated"] = datetime.now().isoformat()
        
        with open(brain_path, 'w') as f:
            json.dump(brain_data, f, indent=2)
    
    def update_brain_with_habit(self, user_id: int, habit_data: Dict):
        """Update brain with new habit data"""
        brain = self.get_user_brain(user_id)
        
        # Add to learning history
        brain["learning_history"].append({
            "type": "habit",
            "timestamp": datetime.now().isoformat(),
            "data": habit_data
        })
        
        # Update habit memory
        habit_key = habit_data.get("date", "")
        brain["habit_memory"][habit_key] = {
            "sleep_hours": habit_data.get("sleep_hours"),
            "exercise_minutes": habit_data.get("exercise_minutes"),
            "meditation_minutes": habit_data.get("meditation_minutes"),
            "reading_minutes": habit_data.get("reading_minutes")
        }
        
        # Analyze patterns
        self._analyze_habit_patterns(brain)
        
        self._save_brain(user_id, brain)
        return brain
    
    def update_brain_with_mood(self, user_id: int, mood_data: Dict):
        """Update brain with mood data"""
        brain = self.get_user_brain(user_id)
        
        brain["learning_history"].append({
            "type": "mood",
            "timestamp": datetime.now().isoformat(),
            "data": mood_data
        })
        
        # Track emotional patterns
        if "emotional_patterns" not in brain["behavior_patterns"]:
            brain["behavior_patterns"]["emotional_patterns"] = []
        
        brain["behavior_patterns"]["emotional_patterns"].append({
            "date": datetime.now().isoformat(),
            "stress": mood_data.get("stress_level"),
            "happiness": mood_data.get("happiness_level"),
            "energy": mood_data.get("energy_level")
        })
        
        self._save_brain(user_id, brain)
        return brain
    
    def update_brain_with_productivity(self, user_id: int, productivity_data: Dict):
        """Update brain with productivity data"""
        brain = self.get_user_brain(user_id)
        
        brain["learning_history"].append({
            "type": "productivity",
            "timestamp": datetime.now().isoformat(),
            "data": productivity_data
        })
        
        # Track productivity patterns
        if "productivity_patterns" not in brain["behavior_patterns"]:
            brain["behavior_patterns"]["productivity_patterns"] = []
        
        brain["behavior_patterns"]["productivity_patterns"].append({
            "date": datetime.now().isoformat(),
            "tasks_completed": productivity_data.get("tasks_completed"),
            "completion_rate": productivity_data.get("tasks_completed", 0) / max(productivity_data.get("tasks_planned", 1), 1),
            "focus_time": productivity_data.get("focus_time_minutes")
        })
        
        self._save_brain(user_id, brain)
        return brain
    
    def update_brain_with_conversation(self, user_id: int, user_message: str, ai_response: str):
        """Update brain with conversation context"""
        brain = self.get_user_brain(user_id)
        
        # Keep only last 20 conversations for context
        if len(brain["conversation_context"]) >= 20:
            brain["conversation_context"].pop(0)
        
        brain["conversation_context"].append({
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "ai": ai_response
        })
        
        self._save_brain(user_id, brain)
        return brain
    
    def _analyze_habit_patterns(self, brain: Dict):
        """Analyze habit patterns and update insights"""
        habits = brain["habit_memory"]
        
        if len(habits) < 3:
            return
        
        # Calculate averages
        total_sleep = sum(h.get("sleep_hours", 0) for h in habits.values() if h.get("sleep_hours"))
        total_exercise = sum(h.get("exercise_minutes", 0) for h in habits.values())
        
        count = len(habits)
        
        brain["behavior_patterns"]["average_sleep"] = total_sleep / count if count > 0 else 0
        brain["behavior_patterns"]["average_exercise"] = total_exercise / count if count > 0 else 0
        
        # Identify trends
        recent_habits = list(habits.values())[-7:]  # Last 7 days
        if len(recent_habits) >= 3:
            sleep_trend = "improving" if recent_habits[-1].get("sleep_hours", 0) > recent_habits[0].get("sleep_hours", 0) else "declining"
            brain["behavior_patterns"]["sleep_trend"] = sleep_trend
    
    def get_brain_context_for_ai(self, user_id: int) -> str:
        """Generate context string from brain for AI prompts"""
        brain = self.get_user_brain(user_id)
        
        context = f"""
USER BRAIN CONTEXT (Private & Personalized):
User ID: {brain['user_id']}
Member Since: {brain['created_at']}
Last Updated: {brain['last_updated']}

BEHAVIOR PATTERNS:
{json.dumps(brain['behavior_patterns'], indent=2)}

RECENT HABITS (Last 7 days):
{json.dumps(list(brain['habit_memory'].values())[-7:], indent=2)}

CONVERSATION HISTORY (Last 5):
{json.dumps(brain['conversation_context'][-5:], indent=2)}

GOALS & PROGRESS:
{json.dumps(brain['goals_progress'], indent=2)}

ACHIEVEMENTS:
{json.dumps(brain['achievements'], indent=2)}

CHALLENGES:
{json.dumps(brain['challenges'], indent=2)}

GROWTH AREAS:
{json.dumps(brain['growth_areas'], indent=2)}
"""
        return context
    
    def generate_personalized_response(self, user_id: int, user_query: str) -> str:
        """Generate AI response using user's personal brain context"""
        brain_context = self.get_brain_context_for_ai(user_id)
        
        # Build personalized prompt
        prompt = f"""
You are a personal AI mentor with access to this user's complete history and patterns.
Use ONLY this user's data to provide personalized guidance.

{brain_context}

USER QUESTION: {user_query}

Provide a personalized response based on:
1. Their specific behavior patterns and habits
2. Their historical data and trends
3. Their personal goals and challenges
4. Previous conversations and context

Be specific, actionable, and reference their actual data.
"""
        
        # Here you would call your AI model (Gemini, GPT, etc.)
        # For now, return a structured response based on brain data
        
        brain = self.get_user_brain(user_id)
        behavior = brain.get("behavior_patterns", {})
        
        response = f"""Based on your personal data and patterns:

📊 Your Patterns:
- Average Sleep: {behavior.get('average_sleep', 'N/A')} hours
- Average Exercise: {behavior.get('average_exercise', 'N/A')} minutes
- Sleep Trend: {behavior.get('sleep_trend', 'N/A')}

💡 Personalized Advice:
"""
        
        # Add context-aware advice
        if behavior.get('average_sleep', 0) < 7:
            response += "\n- You're averaging less than 7 hours of sleep. Consider prioritizing rest for better productivity."
        
        if behavior.get('average_exercise', 0) < 30:
            response += "\n- Your exercise routine could be improved. Even 30 minutes daily can boost your energy levels."
        
        # Reference conversation history
        if brain["conversation_context"]:
            response += f"\n\n📝 Continuing from our last conversation about your {brain['conversation_context'][-1].get('user', 'goals')}..."
        
        return response
    
    def set_user_goal(self, user_id: int, goal: str, target: str):
        """Set a personal goal in user's brain"""
        brain = self.get_user_brain(user_id)
        
        brain["goals_progress"][goal] = {
            "target": target,
            "set_date": datetime.now().isoformat(),
            "status": "active",
            "progress": 0
        }
        
        self._save_brain(user_id, brain)
        return brain
    
    def add_achievement(self, user_id: int, achievement: str):
        """Add achievement to user's brain"""
        brain = self.get_user_brain(user_id)
        
        brain["achievements"].append({
            "achievement": achievement,
            "date": datetime.now().isoformat()
        })
        
        self._save_brain(user_id, brain)
        return brain
    
    def identify_challenge(self, user_id: int, challenge: str):
        """Identify a challenge in user's brain"""
        brain = self.get_user_brain(user_id)
        
        brain["challenges"].append({
            "challenge": challenge,
            "identified_date": datetime.now().isoformat(),
            "status": "active"
        })
        
        self._save_brain(user_id, brain)
        return brain
    
    def get_brain_summary(self, user_id: int) -> Dict:
        """Get a summary of user's brain state"""
        brain = self.get_user_brain(user_id)
        
        return {
            "user_id": user_id,
            "data_points": len(brain["learning_history"]),
            "habits_tracked": len(brain["habit_memory"]),
            "conversations": len(brain["conversation_context"]),
            "active_goals": len([g for g in brain["goals_progress"].values() if g.get("status") == "active"]),
            "achievements": len(brain["achievements"]),
            "challenges": len([c for c in brain["challenges"] if c.get("status") == "active"]),
            "last_updated": brain["last_updated"],
            "behavior_insights": brain["behavior_patterns"]
        }
