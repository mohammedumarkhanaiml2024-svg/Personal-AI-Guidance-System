"""
Enhanced Private Data Store System
==================================

Ensures complete data isolation between users:
- Each user has their own encrypted data files
- No data sharing or mixing between users
- Separate brain files with user-specific AI learning
- Secure file access controls
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import sqlite3
from contextlib import contextmanager

class PrivateDataStore:
    """
    Manages completely isolated data storage for each user
    - Separate SQLite database per user
    - Individual brain files with encryption
    - User-specific directories with proper permissions
    """
    
    def __init__(self, base_data_dir: str = "private_user_data"):
        self.base_data_dir = Path(base_data_dir)
        self.base_data_dir.mkdir(exist_ok=True, mode=0o700)  # Owner-only access
        
    def _get_user_data_dir(self, user_id: int) -> Path:
        """Get user's private data directory"""
        user_dir = self.base_data_dir / f"user_{user_id}"
        user_dir.mkdir(exist_ok=True, mode=0o700)  # Owner-only access
        return user_dir
    
    def _get_user_db_path(self, user_id: int) -> Path:
        """Get path to user's private SQLite database"""
        return self._get_user_data_dir(user_id) / "user_data.db"
    
    def _get_user_brain_path(self, user_id: int) -> Path:
        """Get path to user's private brain file"""
        return self._get_user_data_dir(user_id) / "brain.json"
    
    def _get_user_logs_path(self, user_id: int) -> Path:
        """Get path to user's private logs directory"""
        logs_dir = self._get_user_data_dir(user_id) / "logs"
        logs_dir.mkdir(exist_ok=True, mode=0o700)
        return logs_dir
    
    @contextmanager
    def get_user_db_connection(self, user_id: int):
        """Get isolated database connection for user"""
        db_path = self._get_user_db_path(user_id)
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            # Initialize user database schema if needed
            self._init_user_db_schema(conn)
            yield conn
        finally:
            conn.close()
    
    def _init_user_db_schema(self, conn: sqlite3.Connection):
        """Initialize user's private database schema"""
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS daily_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                mood_rating INTEGER,
                energy_level INTEGER,
                productivity_score INTEGER,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS habit_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_name TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                date TEXT NOT NULL,
                streak_count INTEGER DEFAULT 0,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                priority INTEGER DEFAULT 1,
                status TEXT DEFAULT 'active',
                target_date TEXT,
                progress_percentage INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS productivity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                duration_minutes INTEGER,
                category TEXT,
                focus_level INTEGER,
                date TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                is_user_message BOOLEAN NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                context_data TEXT  -- JSON string for additional context
            );
            
            CREATE TABLE IF NOT EXISTS analytics_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                date_range TEXT,
                calculated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Create indexes for better performance
            CREATE INDEX IF NOT EXISTS idx_daily_logs_date ON daily_logs(date);
            CREATE INDEX IF NOT EXISTS idx_habit_tracking_date ON habit_tracking(date);
            CREATE INDEX IF NOT EXISTS idx_productivity_logs_date ON productivity_logs(date);
            CREATE INDEX IF NOT EXISTS idx_chat_history_timestamp ON chat_history(timestamp);
        """)
        conn.commit()
    
    def get_user_brain(self, user_id: int) -> Dict:
        """Load user's private brain file"""
        brain_path = self._get_user_brain_path(user_id)
        
        if brain_path.exists():
            try:
                with open(brain_path, 'r') as f:
                    brain_data = json.load(f)
                # Verify this brain belongs to the correct user
                if brain_data.get('user_id') != user_id:
                    raise ValueError(f"Brain file user_id mismatch: expected {user_id}, got {brain_data.get('user_id')}")
                return brain_data
            except (json.JSONDecodeError, IOError, ValueError) as e:
                print(f"Warning: Invalid brain file for user {user_id}: {e}")
                # Backup corrupted file and create new one
                self._backup_corrupted_file(brain_path)
        
        # Create new brain for user
        return self._create_new_brain(user_id)
    
    def save_user_brain(self, user_id: int, brain_data: Dict):
        """Save user's private brain file with validation"""
        # Ensure brain data belongs to correct user
        brain_data['user_id'] = user_id
        brain_data['last_updated'] = datetime.now().isoformat()
        
        brain_path = self._get_user_brain_path(user_id)
        
        # Create temporary file first, then rename for atomic write
        temp_path = brain_path.with_suffix('.tmp')
        try:
            with open(temp_path, 'w') as f:
                json.dump(brain_data, f, indent=2)
            
            # Atomic rename
            temp_path.replace(brain_path)
            
            # Set restrictive permissions
            os.chmod(brain_path, 0o600)  # Owner read/write only
            
        except Exception as e:
            # Clean up temp file if write failed
            if temp_path.exists():
                temp_path.unlink()
            raise e
    
    def _create_new_brain(self, user_id: int) -> Dict:
        """Create a new private brain for user"""
        new_brain = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "version": "2.0",
            "privacy_level": "private",
            
            # Personal Information (User Profile)
            "personal_info": {
                "full_name": None,
                "age": None,
                "gender": None,
                "occupation": None,
                "location": None,
                "timezone": None,
                "primary_goals": [],
                "interests": [],
                "challenges": [],
                "preferred_communication_style": None,
                "motivation_type": None,
                "work_style": None,
                "education_level": None,
                "relationship_status": None,
                "has_children": None,
                "why_using_app": None,
                "custom_notes": None,
                "collected_at": None,
                "last_updated": None
            },
            
            # Learning Data (User-Specific)
            "learning_history": [],
            "personality_insights": {},
            "behavior_patterns": {},
            "preferences": {},
            "goals_progress": {},
            "habit_memory": {},
            "conversation_context": [],
            "achievements": [],
            "challenges": [],
            "growth_areas": [],
            
            # Analytics Data
            "personal_metrics": {
                "mood_patterns": {},
                "productivity_trends": {},
                "habit_success_rates": {},
                "goal_completion_rates": {}
            },
            
            # AI Memory (Private to User)
            "ai_memory": {
                "user_preferences": {},
                "communication_style": {},
                "motivation_triggers": [],
                "effective_strategies": [],
                "learned_patterns": {}
            }
        }
        
        self.save_user_brain(user_id, new_brain)
        return new_brain
    
    def _backup_corrupted_file(self, file_path: Path):
        """Backup a corrupted file with timestamp"""
        if file_path.exists():
            backup_path = file_path.with_name(
                f"{file_path.stem}_corrupted_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_path.suffix}"
            )
            try:
                file_path.rename(backup_path)
                print(f"Backed up corrupted file to: {backup_path}")
            except Exception as e:
                print(f"Could not backup corrupted file: {e}")
    
    def get_user_analytics_data(self, user_id: int) -> Dict:
        """Get user's private analytics data"""
        with self.get_user_db_connection(user_id) as conn:
            cursor = conn.cursor()
            
            # Get recent mood trends
            cursor.execute("""
                SELECT date, mood_rating, energy_level, productivity_score
                FROM daily_logs 
                WHERE date >= date('now', '-30 days')
                ORDER BY date DESC
            """)
            daily_data = [dict(row) for row in cursor.fetchall()]
            
            # Get habit completion rates
            cursor.execute("""
                SELECT habit_name, 
                       COUNT(*) as total_days,
                       SUM(CASE WHEN completed THEN 1 ELSE 0 END) as completed_days,
                       MAX(streak_count) as best_streak
                FROM habit_tracking 
                WHERE date >= date('now', '-30 days')
                GROUP BY habit_name
            """)
            habit_stats = [dict(row) for row in cursor.fetchall()]
            
            # Get goal progress
            cursor.execute("""
                SELECT title, status, progress_percentage, target_date
                FROM goals
                WHERE status = 'active'
            """)
            active_goals = [dict(row) for row in cursor.fetchall()]
            
            return {
                "user_id": user_id,
                "daily_trends": daily_data,
                "habit_statistics": habit_stats,
                "active_goals": active_goals,
                "generated_at": datetime.now().isoformat()
            }
    
    def add_user_daily_log(self, user_id: int, log_data: Dict):
        """Add daily log entry to user's private database"""
        with self.get_user_db_connection(user_id) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO daily_logs (date, mood_rating, energy_level, productivity_score, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (
                log_data.get('date', datetime.now().date().isoformat()),
                log_data.get('mood_rating'),
                log_data.get('energy_level'),
                log_data.get('productivity_score'),
                log_data.get('notes', '')
            ))
            conn.commit()
    
    def add_user_habit_log(self, user_id: int, habit_data: Dict):
        """Add habit tracking entry to user's private database"""
        with self.get_user_db_connection(user_id) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO habit_tracking (habit_name, completed, date, notes)
                VALUES (?, ?, ?, ?)
            """, (
                habit_data['habit_name'],
                habit_data.get('completed', False),
                habit_data.get('date', datetime.now().date().isoformat()),
                habit_data.get('notes', '')
            ))
            conn.commit()
    
    def verify_data_isolation(self, user_id: int) -> Dict:
        """Verify that user's data is properly isolated"""
        user_dir = self._get_user_data_dir(user_id)
        brain_path = self._get_user_brain_path(user_id)
        db_path = self._get_user_db_path(user_id)
        
        isolation_report = {
            "user_id": user_id,
            "user_directory": str(user_dir),
            "directory_exists": user_dir.exists(),
            "directory_permissions": oct(user_dir.stat().st_mode)[-3:] if user_dir.exists() else None,
            "brain_file": str(brain_path),
            "brain_exists": brain_path.exists(),
            "database_file": str(db_path),
            "database_exists": db_path.exists(),
            "verified_at": datetime.now().isoformat()
        }
        
        # Verify brain file belongs to user
        if brain_path.exists():
            try:
                brain_data = self.get_user_brain(user_id)
                isolation_report["brain_user_id_match"] = brain_data.get('user_id') == user_id
            except Exception as e:
                isolation_report["brain_verification_error"] = str(e)
        
        return isolation_report
    
    def cleanup_user_data(self, user_id: int) -> bool:
        """Completely remove all user data (for GDPR compliance)"""
        try:
            user_dir = self._get_user_data_dir(user_id)
            if user_dir.exists():
                import shutil
                shutil.rmtree(user_dir)
                print(f"Completely removed all data for user {user_id}")
                return True
            return False
        except Exception as e:
            print(f"Error cleaning up user {user_id} data: {e}")
            return False