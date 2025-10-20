import sqlite3
import os
import json
import hashlib
from pathlib import Path

class Database:
    def __init__(self):
        self.app_data_dir = Path.home() / ".whatsapp-manager"
        self.app_data_dir.mkdir(exist_ok=True)
        self.db_path = self.app_data_dir / "accounts.db"
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                session_dir TEXT NOT NULL,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                settings TEXT
            )
        """)
        
        try:
            cursor.execute("SELECT zoom_level FROM accounts LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE accounts ADD COLUMN zoom_level REAL DEFAULT 1.0")
        
        try:
            cursor.execute("SELECT password_hash FROM accounts LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE accounts ADD COLUMN password_hash TEXT")
        
        conn.commit()
        conn.close()
    
    def add_account(self, name):
        session_dir = self.app_data_dir / f"session_{name.replace(' ', '_').lower()}"
        session_dir.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO accounts (name, session_dir) VALUES (?, ?)",
            (name, str(session_dir))
        )
        account_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return account_id, str(session_dir)
    
    def get_all_accounts(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, session_dir, zoom_level, password_hash FROM accounts ORDER BY last_active DESC")
        accounts = cursor.fetchall()
        conn.close()
        return accounts
    
    def update_zoom_level(self, account_id, zoom_level):
        """Update zoom level for account"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE accounts SET zoom_level = ? WHERE id = ?",
            (zoom_level, account_id)
        )
        conn.commit()
        conn.close()
    
    def update_account_name(self, account_id, new_name):
        """Update account name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE accounts SET name = ? WHERE id = ?",
            (new_name, account_id)
        )
        conn.commit()
        conn.close()
    
    def set_password(self, account_id, password):
        """Set/update password for account (stores hash)"""
        if password:
            # Hash password with SHA256
            password_hash = hashlib.sha256(password.encode()).hexdigest()
        else:
            password_hash = None
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE accounts SET password_hash = ? WHERE id = ?",
            (password_hash, account_id)
        )
        conn.commit()
        conn.close()
    
    def verify_password(self, account_id, password):
        """Verify password for account"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM accounts WHERE id = ?", (account_id,))
        result = cursor.fetchone()
        conn.close()
        
        if not result or not result[0]:
            # No password set
            return True
        
        # Compare hash
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == result[0]
    
    def has_password(self, account_id):
        """Check if account has password set"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM accounts WHERE id = ?", (account_id,))
        result = cursor.fetchone()
        conn.close()
        return result and result[0] is not None
    
    def delete_account(self, account_id):
        """Delete account and its session directory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get session directory path
            cursor.execute("SELECT session_dir FROM accounts WHERE id = ?", (account_id,))
            result = cursor.fetchone()
            
            if result:
                import shutil, time
                session_dir = Path(result[0])
                
                if session_dir.exists():
                    max_retries = 3
                    for attempt in range(max_retries):
                        try:
                            shutil.rmtree(session_dir)
                            break
                        except PermissionError:
                            if attempt < max_retries - 1:
                                time.sleep(0.5)
            
            cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
            conn.commit()
            
        except Exception as e:
            raise
        finally:
            conn.close()
    
    def update_last_active(self, account_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE accounts SET last_active = CURRENT_TIMESTAMP WHERE id = ?",
            (account_id,)
        )
        conn.commit()
        conn.close()
