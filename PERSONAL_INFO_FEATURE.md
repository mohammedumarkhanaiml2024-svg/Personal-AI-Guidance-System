# Personal Information Collection Feature

## Overview
When users register for a new account, they can optionally provide personal information that will be stored **separately** in their **private brain file**. This information is completely isolated per user and helps the AI provide more personalized guidance.

## What Information is Collected?

### Basic Information
- **Full Name**: User's complete name
- **Age**: User's age (13-120)
- **Gender**: Male, Female, Other, or Prefer not to say
- **Occupation**: Current job or profession
- **Location**: City/Country
- **Timezone**: User's timezone (e.g., UTC+5:30)

### Background
- **Education Level**: High school, Bachelor's, Master's, PhD, etc.
- **Relationship Status**: Single, Married, In relationship, etc.
- **Has Children**: Yes/No

### Goals & Interests
- **Primary Goals**: List of main life goals (e.g., "Improve fitness", "Learn new skills")
- **Interests**: Hobbies and passions (e.g., "Reading", "Coding", "Yoga")
- **Challenges**: Current struggles (e.g., "Time management", "Procrastination")

### Preferences
- **Communication Style**: Formal, Casual, Motivational, or Direct
- **Motivation Type**: Achievement, Growth, Social, or Purpose
- **Work Style**: Structured, Flexible, Creative, or Analytical

### Additional Context
- **Why Using App**: User's reason for using the application
- **Custom Notes**: Any additional information user wants to share

## Data Storage

### Where is it Stored?
All personal information is stored in the user's **private brain file**:
```
private_user_data/
└── user_{ID}/
    └── brain.json
```

### Example Brain Structure
```json
{
  "user_id": 123,
  "personal_info": {
    "full_name": "John Doe",
    "age": 28,
    "gender": "male",
    "occupation": "Software Engineer",
    "location": "San Francisco, USA",
    "timezone": "PST (UTC-8)",
    "primary_goals": ["Build successful startup", "Improve fitness", "Learn AI/ML"],
    "interests": ["Coding", "Reading", "Hiking", "Photography"],
    "challenges": ["Time management", "Work-life balance"],
    "preferred_communication_style": "direct",
    "motivation_type": "achievement",
    "work_style": "analytical",
    "education_level": "masters",
    "why_using_app": "Want to track my productivity and get AI-powered insights",
    "collected_at": "2025-10-05T12:30:00",
    "last_updated": "2025-10-05T12:30:00"
  },
  "learning_history": [],
  "behavior_patterns": {},
  ...
}
```

## Privacy & Security

✅ **Complete Data Isolation**: Each user's personal info is stored in their own brain file  
✅ **No Mixing**: User A cannot access User B's personal information  
✅ **Secure Storage**: Brain files have 600 permissions (owner read/write only)  
✅ **Optional**: Users can skip personal info during registration  
✅ **Updatable**: Users can update their info anytime via `/profile/personal-info`  
✅ **GDPR Compliant**: Users can delete all their data via privacy endpoints

## API Endpoints

### 1. Register with Personal Info
```bash
POST /register
```

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword",
  "personal_info": {
    "full_name": "John Doe",
    "age": 28,
    "occupation": "Software Engineer",
    "primary_goals": ["Build startup", "Improve fitness"],
    "interests": ["Coding", "Reading"],
    "preferred_communication_style": "direct"
  }
}
```

**Response:**
```json
{
  "id": 123,
  "username": "johndoe",
  "created_at": "2025-10-05T12:30:00"
}
```

### 2. Get Personal Info
```bash
GET /profile/personal-info
Headers: Authorization: Bearer {token}
```

**Response:**
```json
{
  "full_name": "John Doe",
  "age": 28,
  "occupation": "Software Engineer",
  "location": "San Francisco, USA",
  "primary_goals": ["Build startup", "Improve fitness"],
  "interests": ["Coding", "Reading"],
  "collected_at": "2025-10-05T12:30:00",
  "last_updated": "2025-10-05T12:30:00"
}
```

### 3. Update Personal Info
```bash
PUT /profile/personal-info
Headers: Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "age": 29,
  "location": "New York, USA",
  "primary_goals": ["Build successful AI startup", "Run marathon"]
}
```

### 4. Create/Overwrite Personal Info
```bash
POST /profile/personal-info
Headers: Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "full_name": "John Doe",
  "age": 29,
  "occupation": "Senior Engineer",
  "primary_goals": ["New goals here"]
}
```

## User Experience Flow

### Registration Flow (3 Steps)

#### Step 1: Account Credentials
- Username (required)
- Password (required)
- Confirm Password (required)

#### Step 2: Personal Information
- Name, Age, Gender
- Occupation, Location, Timezone
- Education Level

#### Step 3: Goals & Preferences
- Primary Goals (comma-separated)
- Interests & Hobbies (comma-separated)
- Current Challenges (comma-separated)
- Communication Style preference
- Motivation Type
- Work Style
- Why using the app

### Features
✨ **Multi-step Form**: Easy-to-use 3-step registration process  
✨ **Skip Option**: Users can skip personal info and add it later  
✨ **Validation**: Client-side validation for required fields  
✨ **Beautiful UI**: Gradient design with step indicators  
✨ **Auto-redirect**: Automatically redirects to login after successful registration

## How to Access

### For New Users
1. Go to the homepage: `https://your-codespace-8080.app.github.dev/`
2. Click on "✨ Create New Account"
3. Fill in the 3-step form
4. (Optional) Skip personal info if you want
5. Click "Create Account 🚀"
6. You'll be redirected to login

### For Existing Users
1. Login to your account
2. Go to your profile settings
3. Use the personal info endpoints to add/update your information

## AI Personalization Benefits

By providing personal information, the AI can:

🎯 **Better Goal Tracking**: Understand your primary goals and track progress  
💬 **Personalized Communication**: Adapt communication style to your preference  
📊 **Contextual Insights**: Provide insights based on your occupation and lifestyle  
🧠 **Smarter Recommendations**: Suggest activities aligned with your interests  
⚡ **Targeted Motivation**: Use your motivation type to inspire you effectively  
🎨 **Customized Experience**: Tailor the entire app to your work style and preferences

## Technical Implementation

### Backend (FastAPI)
- **Schemas**: `PersonalInfoCreate`, `PersonalInfoUpdate`, `PersonalInfoOut` in `schemas.py`
- **Registration**: Enhanced `/register` endpoint accepts `UserRegistrationWithInfo`
- **Storage**: `private_data_store.py` includes personal_info in brain structure
- **Endpoints**: GET/PUT/POST `/profile/personal-info` for managing personal data

### Frontend (HTML + Alpine.js)
- **Register Page**: `register.html` with 3-step form
- **Index Page**: Updated `index.html` with "Create Account" button
- **Styling**: Uses shared.css for consistent UI

### Security
- Personal info stored in user's private brain file (not in shared database)
- Brain files have restrictive permissions (600 - owner only)
- User ID validation on all operations
- No data mixing between users

## Future Enhancements

🔮 **AI-Powered Onboarding**: Use personal info to create custom onboarding experience  
🔮 **Smart Defaults**: Pre-fill forms based on user profile  
🔮 **Personality Insights**: Analyze personal info to provide personality insights  
🔮 **Goal Templates**: Suggest goal templates based on occupation and interests  
🔮 **Habit Recommendations**: Recommend habits aligned with user's goals and challenges  
🔮 **Progress Visualization**: Show personalized progress charts  
🔮 **AI Coach Customization**: Train AI coach with user's communication preference

## Example Use Cases

### Use Case 1: Student Registration
```json
{
  "username": "student_alice",
  "password": "securepass123",
  "personal_info": {
    "full_name": "Alice Johnson",
    "age": 20,
    "occupation": "College Student",
    "education_level": "bachelors",
    "primary_goals": ["Maintain 4.0 GPA", "Learn programming", "Build portfolio"],
    "interests": ["Web development", "Design", "Photography"],
    "challenges": ["Procrastination", "Time management"],
    "preferred_communication_style": "motivational",
    "motivation_type": "achievement",
    "work_style": "flexible"
  }
}
```

### Use Case 2: Professional Registration
```json
{
  "username": "engineer_bob",
  "password": "securepass456",
  "personal_info": {
    "full_name": "Bob Smith",
    "age": 32,
    "occupation": "Senior Software Engineer",
    "education_level": "masters",
    "primary_goals": ["Lead engineering team", "Work-life balance", "Learn AI/ML"],
    "interests": ["Coding", "Reading tech blogs", "Running"],
    "challenges": ["Burnout prevention", "Delegation"],
    "preferred_communication_style": "direct",
    "motivation_type": "growth",
    "work_style": "analytical"
  }
}
```

### Use Case 3: Minimal Registration (Skip Personal Info)
```json
{
  "username": "quick_user",
  "password": "password123",
  "personal_info": null
}
```

---

## Summary

✅ **Implemented**: Personal information collection during registration  
✅ **Secure**: Stored in user's private brain file with complete isolation  
✅ **Optional**: Users can skip and add later  
✅ **Updateable**: Users can modify their info anytime  
✅ **Beautiful UI**: 3-step registration form with gradients  
✅ **API Ready**: Full CRUD endpoints for personal information  

🎉 **Users now have a personalized AI guidance experience from day one!**
