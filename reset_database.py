#!/usr/bin/env python3
"""
Utility script to reset the RSVP database for a new event.
This will delete all existing RSVP entries and recreate the database with a fresh schema.
"""

import os
import sqlite3
import sys

def reset_database():
    """Reset the RSVP database by deleting it and recreating it"""
    db_path = 'rsvp.db'
    
    # Check if database exists
    if os.path.exists(db_path):
        # Confirm before deleting
        print("⚠️  WARNING: This will delete all existing RSVP data!")
        response = input("Are you sure you want to reset the database? (yes/no): ")
        
        if response.lower() not in ['yes', 'y']:
            print("❌ Database reset cancelled.")
            return False
        
        # Delete the existing database
        try:
            os.remove(db_path)
            print(f"✅ Deleted existing database: {db_path}")
        except Exception as e:
            print(f"❌ Error deleting database: {e}")
            return False
    else:
        print(f"ℹ️  Database {db_path} does not exist. Creating new one...")
    
    # Create a new database with the schema
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS rsvps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                guests INTEGER NOT NULL,
                comments TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print(f"✅ Created new database: {db_path}")
        print("✅ Database reset complete! Ready for a new event.")
        return True
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

if __name__ == '__main__':
    success = reset_database()
    sys.exit(0 if success else 1)


