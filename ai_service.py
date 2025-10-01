"""
AI Service Module - Implements 2️⃣ Features (AI Model Capabilities)

This module provides:
1. User Profiling - Analyze user behavior and identify patterns
2. Personalized Recommendations - Suggest habits, schedules, workouts
3. Routine Prediction - Predict productivity patterns and habits
4. Habit Analytics - Track trends and provide insights
5. Conversational AI - Gemini-powered chatbot for guidance
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from collections import defaultdict, Counter
import statistics
import json

from models import User, UserProfile, Goal, HabitTracking, ProductivityLog, MoodTracking
from schemas import (
    UserProfileAnalysis, PersonalizedRecommendation, 
    RoutinePrediction, HabitAnalytics
)


# Gemini API Configuration
GEMINI_API_KEY = "AIzaSyBiLiAIDlqzmZ6-9JA6cG9t46-EERksj3I"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


class AIGuidanceService:
    """
    Core AI service that implements all AI capabilities
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    # ========== 1. USER PROFILING ==========
    def generate_user_profile_analysis(self, user_id: int) -> UserProfileAnalysis:
        """
        2️⃣ AI Capability: User Profiling
        Analyzes user data to identify strengths, weaknesses, and patterns
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        profile = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        
        # Gather historical data
        habits = self.db.query(HabitTracking).filter(
            HabitTracking.user_id == user_id
        ).order_by(HabitTracking.date.desc()).limit(30).all()
        
        productivity = self.db.query(ProductivityLog).filter(
            ProductivityLog.user_id == user_id
        ).order_by(ProductivityLog.date.desc()).limit(30).all()
        
        moods = self.db.query(MoodTracking).filter(
            MoodTracking.user_id == user_id
        ).order_by(MoodTracking.timestamp.desc()).limit(30).all()
        
        # Analyze patterns
        strengths = []
        weaknesses = []
        patterns = []
        
        # Sleep analysis
        if habits:
            avg_sleep = statistics.mean([h.sleep_hours for h in habits if h.sleep_hours])
            if avg_sleep >= 7:
                strengths.append("Maintains healthy sleep schedule")
            else:
                weaknesses.append("Insufficient sleep (avg {:.1f}h/night)".format(avg_sleep))
                patterns.append("Sleep deprivation pattern detected")
        
        # Exercise analysis
        if habits:
            exercise_days = sum(1 for h in habits if h.exercise_minutes and h.exercise_minutes > 0)
            exercise_ratio = exercise_days / len(habits)
            if exercise_ratio >= 0.5:
                strengths.append("Regular exercise routine ({:.0f}% of days)".format(exercise_ratio * 100))
            else:
                weaknesses.append("Inconsistent exercise ({:.0f}% of days)".format(exercise_ratio * 100))
        
        # Productivity analysis
        if productivity:
            completion_rates = [
                p.tasks_completed / p.tasks_planned if p.tasks_planned > 0 else 0 
                for p in productivity
            ]
            avg_completion = statistics.mean(completion_rates) if completion_rates else 0
            
            if avg_completion >= 0.7:
                strengths.append("High task completion rate ({:.0f}%)".format(avg_completion * 100))
            else:
                weaknesses.append("Low task completion rate ({:.0f}%)".format(avg_completion * 100))
        
        # Mood analysis
        if moods:
            avg_stress = statistics.mean([m.stress_level for m in moods])
            avg_happiness = statistics.mean([m.happiness_level for m in moods])
            
            if avg_stress >= 7:
                weaknesses.append("High stress levels (avg {:.1f}/10)".format(avg_stress))
                patterns.append("Chronic stress detected")
            
            if avg_happiness >= 7:
                strengths.append("Generally positive mood (avg {:.1f}/10)".format(avg_happiness))
        
        # Calculate consistency score
        consistency_score = self._calculate_consistency_score(habits, productivity)
        
        # Update profile consistency score
        if profile:
            profile.consistency_score = consistency_score
            self.db.commit()
        
        # Generate recommendations
        recommendations = self._generate_profile_recommendations(
            strengths, weaknesses, patterns, profile
        )
        
        # Generate summary
        profile_summary = self._generate_profile_summary(
            user.username, strengths, weaknesses, patterns, consistency_score
        )
        
        return UserProfileAnalysis(
            user_id=user_id,
            profile_summary=profile_summary,
            identified_strengths=strengths,
            identified_weaknesses=weaknesses,
            behavioral_patterns=patterns,
            consistency_score=consistency_score,
            recommendations=recommendations
        )
    
    def _calculate_consistency_score(self, habits: List, productivity: List) -> float:
        """Calculate consistency score based on habit and productivity data"""
        if not habits and not productivity:
            return 0.0
        
        scores = []
        
        # Habit consistency
        if habits and len(habits) >= 7:
            # Check if habits are logged regularly
            dates = sorted([h.date for h in habits])
            gaps = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
            avg_gap = statistics.mean(gaps) if gaps else 0
            habit_consistency = max(0, 1 - (avg_gap / 7))  # Penalize gaps
            scores.append(habit_consistency)
        
        # Productivity consistency
        if productivity:
            completion_rates = [
                p.tasks_completed / p.tasks_planned if p.tasks_planned > 0 else 0 
                for p in productivity
            ]
            if completion_rates:
                prod_consistency = statistics.mean(completion_rates)
                scores.append(prod_consistency)
        
        return round(statistics.mean(scores) * 10, 2) if scores else 0.0
    
    def _generate_profile_summary(self, username: str, strengths: List, 
                                   weaknesses: List, patterns: List, 
                                   consistency_score: float) -> str:
        """Generate a natural language profile summary"""
        summary = f"Profile Analysis for {username}:\n\n"
        summary += f"Consistency Score: {consistency_score}/10\n\n"
        
        if strengths:
            summary += "Key Strengths:\n"
            for s in strengths:
                summary += f"✓ {s}\n"
            summary += "\n"
        
        if weaknesses:
            summary += "Areas for Improvement:\n"
            for w in weaknesses:
                summary += f"⚠ {w}\n"
            summary += "\n"
        
        if patterns:
            summary += "Behavioral Patterns:\n"
            for p in patterns:
                summary += f"• {p}\n"
        
        return summary
    
    def _generate_profile_recommendations(self, strengths: List, weaknesses: List, 
                                          patterns: List, profile: UserProfile) -> List[str]:
        """Generate actionable recommendations based on profile analysis"""
        recommendations = []
        
        # Sleep recommendations
        if any("sleep" in w.lower() for w in weaknesses):
            recommendations.append("Try setting a consistent bedtime routine and aim for 7-8 hours of sleep")
        
        # Exercise recommendations
        if any("exercise" in w.lower() for w in weaknesses):
            if profile and profile.exercise_preference:
                recommendations.append(f"Schedule regular {profile.exercise_preference} sessions 3-4 times per week")
            else:
                recommendations.append("Start with 20-30 minutes of physical activity 3 times per week")
        
        # Stress management
        if any("stress" in w.lower() for w in weaknesses):
            recommendations.append("Practice daily meditation or breathing exercises for stress management")
        
        # Productivity recommendations
        if any("completion" in w.lower() or "task" in w.lower() for w in weaknesses):
            recommendations.append("Break larger tasks into smaller, manageable chunks")
            recommendations.append("Use time-blocking technique to allocate focused work periods")
        
        return recommendations
    
    # ========== 2. PERSONALIZED RECOMMENDATIONS ==========
    def generate_personalized_recommendations(self, user_id: int) -> List[PersonalizedRecommendation]:
        """
        2️⃣ AI Capability: Personalized Recommendations
        Suggests habits, schedules, workouts based on user routine
        """
        profile = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        
        # Get recent data for context
        recent_habits = self.db.query(HabitTracking).filter(
            HabitTracking.user_id == user_id
        ).order_by(HabitTracking.date.desc()).limit(7).all()
        
        recent_mood = self.db.query(MoodTracking).filter(
            MoodTracking.user_id == user_id
        ).order_by(MoodTracking.timestamp.desc()).first()
        
        recommendations = []
        
        # Sleep schedule recommendation
        if recent_habits:
            avg_sleep = statistics.mean([h.sleep_hours for h in recent_habits if h.sleep_hours])
            if avg_sleep < 7:
                sleep_times = [h.sleep_time for h in recent_habits if h.sleep_time]
                if sleep_times:
                    # Analyze sleep patterns
                    recommendations.append(PersonalizedRecommendation(
                        recommendation_type="schedule",
                        title="Improve Sleep Schedule",
                        description=f"You're averaging {avg_sleep:.1f} hours of sleep. Try shifting your bedtime 30 minutes earlier.",
                        reasoning=f"Your current sleep pattern shows an average of {avg_sleep:.1f}h/night, which is below the recommended 7-8 hours.",
                        priority="high",
                        actionable_steps=[
                            "Set a bedtime alarm 30 minutes before your target sleep time",
                            "Avoid screens 1 hour before bed",
                            "Create a calming bedtime routine (reading, meditation)"
                        ]
                    ))
        
        # Exercise recommendation based on profile
        if profile and profile.exercise_preference:
            exercise_consistency = sum(1 for h in recent_habits if h.exercise_minutes and h.exercise_minutes > 0)
            if exercise_consistency < 3:
                recommendations.append(PersonalizedRecommendation(
                    recommendation_type="workout",
                    title=f"Regular {profile.exercise_preference.title()} Sessions",
                    description=f"Based on your preference for {profile.exercise_preference}, schedule regular workout sessions.",
                    reasoning=f"You've only exercised {exercise_consistency} times in the last week.",
                    priority="medium",
                    actionable_steps=[
                        f"Schedule {profile.exercise_preference} for 30 minutes, 3 times this week",
                        "Set reminders on your phone",
                        "Track progress to build consistency"
                    ]
                ))
        
        # Stress management based on mood
        if recent_mood and recent_mood.stress_level >= 7:
            recommendations.append(PersonalizedRecommendation(
                recommendation_type="relaxation",
                title="Stress Management Techniques",
                description="Your recent stress levels are high. Incorporate relaxation techniques into your routine.",
                reasoning=f"Your latest stress level is {recent_mood.stress_level}/10, indicating high stress.",
                priority="high",
                actionable_steps=[
                    "Practice 10 minutes of meditation or deep breathing daily",
                    "Take short breaks every hour during work",
                    "Consider journaling to process thoughts and emotions",
                    "Engage in a hobby or activity you enjoy"
                ]
            ))
        
        # Productivity recommendation
        if profile and profile.preferred_work_hours:
            recommendations.append(PersonalizedRecommendation(
                recommendation_type="schedule",
                title=f"Optimize {profile.preferred_work_hours.title()} Productivity",
                description=f"Schedule your most important tasks during your preferred {profile.preferred_work_hours} hours.",
                reasoning=f"You've indicated that {profile.preferred_work_hours} works best for you.",
                priority="medium",
                actionable_steps=[
                    f"Block {profile.preferred_work_hours} hours for deep work",
                    "Minimize distractions during peak productivity time",
                    "Save routine tasks for off-peak hours"
                ]
            ))
        
        return recommendations
    
    # ========== 3. ROUTINE PREDICTION ==========
    def predict_routine(self, user_id: int, prediction_date: datetime) -> RoutinePrediction:
        """
        2️⃣ AI Capability: Routine Prediction
        Predicts productive hours and habit patterns
        """
        # Get historical data for pattern analysis
        productivity_logs = self.db.query(ProductivityLog).filter(
            ProductivityLog.user_id == user_id
        ).order_by(ProductivityLog.date.desc()).limit(30).all()
        
        habits = self.db.query(HabitTracking).filter(
            HabitTracking.user_id == user_id
        ).order_by(HabitTracking.date.desc()).limit(30).all()
        
        # Predict productive hours based on historical data
        productive_hours = []
        if productivity_logs:
            hour_counter = Counter([p.most_productive_hour for p in productivity_logs if p.most_productive_hour])
            if hour_counter:
                # Get top 3 most common productive hours
                productive_hours = [hour for hour, _ in hour_counter.most_common(3)]
        
        # Predict energy levels by hour
        energy_levels = {}
        if productivity_logs:
            for log in productivity_logs:
                if log.most_productive_hour and log.energy_level:
                    hour = log.most_productive_hour.split('-')[0]  # Get start hour
                    if hour not in energy_levels:
                        energy_levels[hour] = []
                    energy_levels[hour].append(log.energy_level)
            
            # Average energy levels per hour
            energy_levels = {
                hour: round(statistics.mean(levels), 1) 
                for hour, levels in energy_levels.items()
            }
        
        # Predict habit likelihoods
        habit_predictions = {}
        if habits:
            total_days = len(habits)
            
            # Exercise prediction
            exercise_days = sum(1 for h in habits if h.exercise_minutes and h.exercise_minutes > 0)
            habit_predictions["exercise"] = round(exercise_days / total_days, 2)
            
            # Meditation prediction
            meditation_days = sum(1 for h in habits if h.meditation_minutes and h.meditation_minutes > 0)
            habit_predictions["meditation"] = round(meditation_days / total_days, 2)
            
            # Reading prediction
            reading_days = sum(1 for h in habits if h.reading_minutes and h.reading_minutes > 0)
            habit_predictions["reading"] = round(reading_days / total_days, 2)
        
        # Generate recommendations based on predictions
        recommendations = []
        if productive_hours:
            recommendations.append(f"Schedule important tasks during your peak hours: {', '.join(productive_hours)}")
        
        if habit_predictions.get("exercise", 0) < 0.5:
            recommendations.append("You have a 50%+ chance of skipping exercise tomorrow. Set a reminder!")
        
        if habit_predictions.get("meditation", 0) >= 0.7:
            recommendations.append("You're likely to meditate tomorrow. Keep up the good habit!")
        
        return RoutinePrediction(
            date=prediction_date,
            predicted_productive_hours=productive_hours,
            predicted_energy_levels=energy_levels,
            habit_predictions=habit_predictions,
            recommendations=recommendations
        )
    
    # ========== 4. HABIT ANALYTICS ==========
    def generate_habit_analytics(self, user_id: int, period: str = "month") -> HabitAnalytics:
        """
        2️⃣ AI Capability: Habit Analytics
        Analyzes habit trends and provides insights
        """
        # Determine date range
        end_date = datetime.now()
        if period == "week":
            start_date = end_date - timedelta(days=7)
        elif period == "month":
            start_date = end_date - timedelta(days=30)
        else:  # year
            start_date = end_date - timedelta(days=365)
        
        # Get habits in period
        habits = self.db.query(HabitTracking).filter(
            HabitTracking.user_id == user_id,
            HabitTracking.date >= start_date,
            HabitTracking.date <= end_date
        ).order_by(HabitTracking.date).all()
        
        if not habits:
            return HabitAnalytics(
                period=period,
                habits_summary={},
                trends={},
                streaks={},
                insights=["Not enough data to generate analytics. Start tracking your habits!"],
                visualizations_data=None
            )
        
        # Calculate habits summary
        habits_summary = {
            "total_days_tracked": len(habits),
            "avg_sleep_hours": round(statistics.mean([h.sleep_hours for h in habits if h.sleep_hours]), 1),
            "avg_exercise_minutes": round(statistics.mean([h.exercise_minutes for h in habits if h.exercise_minutes]), 1),
            "avg_meditation_minutes": round(statistics.mean([h.meditation_minutes for h in habits if h.meditation_minutes]), 1),
            "avg_reading_minutes": round(statistics.mean([h.reading_minutes for h in habits if h.reading_minutes]), 1),
            "avg_social_media_minutes": round(statistics.mean([h.social_media_minutes for h in habits if h.social_media_minutes]), 1),
        }
        
        # Analyze trends (compare first half vs second half)
        mid_point = len(habits) // 2
        first_half = habits[:mid_point]
        second_half = habits[mid_point:]
        
        trends = {}
        
        # Sleep trend
        sleep_first = statistics.mean([h.sleep_hours for h in first_half if h.sleep_hours])
        sleep_second = statistics.mean([h.sleep_hours for h in second_half if h.sleep_hours])
        trends["sleep"] = "improving" if sleep_second > sleep_first else "declining" if sleep_second < sleep_first else "stable"
        
        # Exercise trend
        exercise_first = statistics.mean([h.exercise_minutes for h in first_half if h.exercise_minutes])
        exercise_second = statistics.mean([h.exercise_minutes for h in second_half if h.exercise_minutes])
        trends["exercise"] = "improving" if exercise_second > exercise_first else "declining" if exercise_second < exercise_first else "stable"
        
        # Calculate streaks
        streaks = self._calculate_streaks(habits)
        
        # Generate insights
        insights = []
        
        if habits_summary["avg_sleep_hours"] >= 7:
            insights.append(f"✓ Great sleep habits! You're averaging {habits_summary['avg_sleep_hours']}h/night")
        else:
            insights.append(f"⚠ Sleep needs improvement. Current average: {habits_summary['avg_sleep_hours']}h/night")
        
        if trends["exercise"] == "improving":
            insights.append("✓ Exercise routine is improving over time!")
        elif trends["exercise"] == "declining":
            insights.append("⚠ Exercise consistency is declining. Try to get back on track!")
        
        if streaks.get("meditation", 0) >= 7:
            insights.append(f"🔥 Amazing meditation streak of {streaks['meditation']} days!")
        
        # Visualization data
        viz_data = {
            "sleep_trend": [h.sleep_hours for h in habits if h.sleep_hours],
            "exercise_trend": [h.exercise_minutes for h in habits if h.exercise_minutes],
            "dates": [h.date.strftime("%Y-%m-%d") for h in habits]
        }
        
        return HabitAnalytics(
            period=period,
            habits_summary=habits_summary,
            trends=trends,
            streaks=streaks,
            insights=insights,
            visualizations_data=viz_data
        )
    
    def _calculate_streaks(self, habits: List[HabitTracking]) -> Dict[str, int]:
        """Calculate current streaks for various habits"""
        streaks = {}
        
        # Sort habits by date descending
        sorted_habits = sorted(habits, key=lambda h: h.date, reverse=True)
        
        # Exercise streak
        exercise_streak = 0
        for habit in sorted_habits:
            if habit.exercise_minutes and habit.exercise_minutes > 0:
                exercise_streak += 1
            else:
                break
        streaks["exercise"] = exercise_streak
        
        # Meditation streak
        meditation_streak = 0
        for habit in sorted_habits:
            if habit.meditation_minutes and habit.meditation_minutes > 0:
                meditation_streak += 1
            else:
                break
        streaks["meditation"] = meditation_streak
        
        # Reading streak
        reading_streak = 0
        for habit in sorted_habits:
            if habit.reading_minutes and habit.reading_minutes > 0:
                reading_streak += 1
            else:
                break
        streaks["reading"] = reading_streak
        
        return streaks
    
    # ========== 5. CONVERSATIONAL AI (Gemini Integration) ==========
    def chat_with_ai(self, user_id: int, user_message: str, context: Optional[Dict] = None) -> Dict:
        """
        2️⃣ AI Capability: Conversational Guidance
        AI mentor that provides motivation, reminders, and answers
        """
        # Get user context
        user = self.db.query(User).filter(User.id == user_id).first()
        profile = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        
        # Build context for AI
        system_context = f"""You are a personal AI guidance mentor for {user.username}. 
Your role is to provide personalized advice, motivation, and support based on their habits and goals.

User Context:
"""
        
        if profile:
            system_context += f"""
- Age: {profile.age if profile.age else 'Unknown'}
- Occupation: {profile.occupation if profile.occupation else 'Unknown'}
- Personality: {profile.personality_type if profile.personality_type else 'Unknown'}
- Consistency Score: {profile.consistency_score}/10
"""
        
        # Add recent activity context if provided
        if context:
            system_context += f"\nRecent Activity:\n{json.dumps(context, indent=2)}"
        
        system_context += f"\n\nUser Message: {user_message}\n\nProvide helpful, encouraging, and actionable advice."
        
        # Call Gemini API
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": GEMINI_API_KEY
        }
        
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": system_context}
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(GEMINI_API_URL, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            ai_response = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "I'm here to help! Could you provide more details?")
            
            # Detect intent (simple keyword-based)
            intent = self._detect_intent(user_message)
            
            return {
                "response": ai_response,
                "intent": intent,
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            return {
                "response": f"I'm having trouble connecting right now. Error: {str(e)}. But I'm here to help! Could you try again?",
                "intent": "error",
                "timestamp": datetime.now()
            }
    
    def _detect_intent(self, message: str) -> str:
        """Simple intent detection based on keywords"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["motivate", "encourage", "inspire", "boost"]):
            return "motivation"
        elif any(word in message_lower for word in ["advice", "suggest", "recommend", "should"]):
            return "advice"
        elif any(word in message_lower for word in ["progress", "analytics", "stats", "how am i"]):
            return "analytics"
        elif any(word in message_lower for word in ["goal", "target", "achieve"]):
            return "goal_tracking"
        elif any(word in message_lower for word in ["stress", "anxiety", "worried", "overwhelmed"]):
            return "emotional_support"
        else:
            return "general"
