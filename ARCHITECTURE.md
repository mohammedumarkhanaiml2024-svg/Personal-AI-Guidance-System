# System Architecture & Data Flow

## Overall System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Personal AI Guidance System                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────┐         ┌──────────────────────────────┐
│                     │         │                              │
│   User Interface    │◄────────┤   FastAPI Backend           │
│   (API Client)      │         │   (main_enhanced.py)        │
│                     │         │                              │
└─────────────────────┘         └──────────────┬───────────────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
                    ▼                          ▼                          ▼
        ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
        │  Authentication  │      │   AI Service     │      │    Database      │
        │    (auth.py)     │      │ (ai_service.py)  │      │  (SQLAlchemy)    │
        │                  │      │                  │      │                  │
        │ - JWT Tokens     │      │ - Profiling      │      │ - User Data      │
        │ - Argon2 Hash    │      │ - Recommendations│      │ - Habits         │
        │ - Password Auth  │      │ - Predictions    │      │ - Goals          │
        │                  │      │ - Analytics      │      │ - Productivity   │
        └──────────────────┘      │ - Chatbot        │      │ - Mood Logs      │
                                  │                  │      │                  │
                                  └────────┬─────────┘      └──────────────────┘
                                           │
                                           ▼
                              ┌──────────────────────┐
                              │   Gemini AI API      │
                              │  (Google Cloud)      │
                              │                      │
                              │ - Chat responses     │
                              │ - NLU processing     │
                              └──────────────────────┘
```

## Data Flow: From Input to AI Insights

```
1️⃣ INPUT FEATURES (Data Collection)
═══════════════════════════════════

User Actions                    Database Models
─────────────                  ───────────────
Log habits          ──────►    HabitTracking
Log productivity    ──────►    ProductivityLog
Log mood           ──────►    MoodTracking
Set goals          ──────►    Goal
Update profile     ──────►    UserProfile

                    ▼
               [SQLite Database]
                    │
                    │ Raw data stored
                    ▼


2️⃣ AI PROCESSING (Analysis Layer)
═══════════════════════════════════

AIGuidanceService methods:
─────────────────────────

┌──────────────────────────────────────────────────────┐
│  generate_user_profile_analysis()                    │
│  ├─ Query 30 days of habits, productivity, mood      │
│  ├─ Calculate averages, patterns, trends             │
│  ├─ Identify strengths & weaknesses                  │
│  └─ Generate consistency score                       │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────┐
│  generate_personalized_recommendations()             │
│  ├─ Analyze recent patterns                          │
│  ├─ Compare against goals & preferences              │
│  ├─ Prioritize recommendations                       │
│  └─ Generate actionable steps                        │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────┐
│  predict_routine()                                   │
│  ├─ Analyze historical productivity times            │
│  ├─ Calculate habit frequencies                      │
│  ├─ Predict energy levels by hour                    │
│  └─ Forecast habit likelihoods                       │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────┐
│  generate_habit_analytics()                          │
│  ├─ Calculate summary statistics                     │
│  ├─ Compare periods (trends)                         │
│  ├─ Calculate streaks                                │
│  └─ Generate insights                                │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────┐
│  chat_with_ai()                                      │
│  ├─ Build context from user data                     │
│  ├─ Call Gemini API with context                     │
│  ├─ Detect intent from message                       │
│  └─ Return personalized response                     │
└──────────────────────────────────────────────────────┘


3️⃣ AI CAPABILITIES (Output)
═══════════════════════════════

User gets:
──────────
✓ Profile Analysis with insights
✓ Personalized recommendations
✓ Routine predictions
✓ Habit analytics & trends
✓ Conversational AI guidance
```

## Database Schema Relationships

```
┌──────────────┐
│    Users     │
│──────────────│
│ id (PK)      │───┐
│ username     │   │
│ password     │   │
└──────────────┘   │
                   │
        ┌──────────┼──────────┬──────────┬──────────┬──────────┐
        │          │          │          │          │          │
        ▼          ▼          ▼          ▼          ▼          ▼
┌──────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ ┌────────┐
│ Profile  │ │  Goals  │ │ Habits  │ │Productivity│ │  Mood  │ │  Chat  │
│──────────│ │─────────│ │─────────│ │──────────│ │────────│ │────────│
│user_id FK│ │user_id FK│ │user_id FK│ │user_id FK│ │user_id │ │user_id │
│age       │ │title    │ │date     │ │date      │ │stress  │ │message │
│occupation│ │category │ │sleep_hrs│ │tasks_done│ │happy   │ │role    │
│strengths │ │target   │ │exercise │ │deadlines │ │energy  │ │intent  │
│weaknesses│ │progress │ │reading  │ │focus_time│ │anxiety │ │        │
└──────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ └────────┘
    (1:1)      (1:Many)    (1:Many)     (1:Many)   (1:Many)   (1:Many)
```

## API Request Flow Example

```
User wants AI recommendations
────────────────────────────

1. Client Request
   ↓
   GET /ai/recommendations
   Headers: Authorization: Bearer <JWT_TOKEN>

2. FastAPI Middleware
   ↓
   - Verify JWT token (auth.py)
   - Extract user_id from token
   - Get database session

3. Endpoint Handler
   ↓
   - Call AIGuidanceService.generate_personalized_recommendations()

4. AI Service Processing
   ↓
   - Query UserProfile for preferences
   - Query last 7 days of HabitTracking
   - Query latest MoodTracking
   - Analyze patterns
   - Generate recommendations based on:
     * Sleep patterns
     * Exercise consistency
     * Stress levels
     * User preferences (exercise_preference, work hours)

5. Response Construction
   ↓
   - Build list of PersonalizedRecommendation objects
   - Include: title, description, reasoning, priority, steps

6. Return to Client
   ↓
   JSON response with personalized recommendations
```

## Feature Integration Map

```
How Input Features → Enable AI Capabilities
══════════════════════════════════════════

INPUT: UserProfile (age, occupation, personality)
   ↓
   ENABLES: Personalized context for recommendations
   EXAMPLE: "As an introvert, schedule solo work during peak hours"

INPUT: HabitTracking (sleep, exercise, meditation)
   ↓
   ENABLES: Habit analytics, trend detection, streak calculation
   EXAMPLE: "14-day meditation streak! Exercise declining 20%"

INPUT: ProductivityLog (tasks, focus time, deadlines)
   ↓
   ENABLES: Routine prediction, productive hour detection
   EXAMPLE: "You're most productive 9-10 AM. Schedule tasks then."

INPUT: MoodTracking (stress, happiness, energy)
   ↓
   ENABLES: Emotional pattern detection, wellness recommendations
   EXAMPLE: "High stress detected. Your data shows exercise helps."

INPUT: Goals (targets, progress, categories)
   ↓
   ENABLES: Goal-oriented recommendations, progress tracking
   EXAMPLE: "You're 60% toward your fitness goal. Great progress!"

ALL INPUTS COMBINED
   ↓
   ENABLES: Comprehensive user profiling
   EXAMPLE: "Your sleep affects productivity by 30%. Stress correlates
            with missed deadlines. Exercise boosts happiness by 25%."
```

## AI Capability Dependencies

```
                    ┌─────────────────┐
                    │  USER PROFILING │
                    │  (Foundation)   │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│ RECOMMENDATIONS  │ │ PREDICTIONS  │ │   ANALYTICS      │
│                  │ │              │ │                  │
│ Uses: Profile +  │ │ Uses: Profile│ │ Uses: Profile +  │
│ Recent patterns  │ │ Historical   │ │ Time series data │
└──────────────────┘ └──────────────┘ └──────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  CHATBOT        │
                    │  (Integrates    │
                    │   all above)    │
                    └─────────────────┘
```

## Technology Stack Detail

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend Layer                         │
│  Any HTTP client (curl, Postman, React, mobile app)     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   API Layer                              │
│  FastAPI (Python)                                        │
│  - REST endpoints                                        │
│  - Automatic OpenAPI docs                                │
│  - Pydantic validation                                   │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│   Security  │  │  AI Engine   │  │   Database   │
│─────────────│  │──────────────│  │──────────────│
│ JWT (jose)  │  │ Statistics   │  │ SQLAlchemy   │
│ Argon2      │  │ Pattern      │  │ SQLite       │
│ AES-256     │  │  Recognition │  │              │
│             │  │ Gemini API   │  │              │
└─────────────┘  └──────────────┘  └──────────────┘
```

This architecture enables a complete AI guidance system that learns from your data and provides intelligent insights! 🚀
