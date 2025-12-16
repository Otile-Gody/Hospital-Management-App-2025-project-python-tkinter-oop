"""
Database connection and management module
"""
import sqlite3
import os


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path="hospital.db"):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    
    def execute_update(self, query, params=None):
        """Execute an update/insert/delete query"""
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
        return cursor.lastrowid
    
    def create_tables(self):
        """Create necessary database tables"""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                gender TEXT NOT NULL,
                contact_number TEXT NOT NULL,
                address TEXT NOT NULL,
                email TEXT,
                registration_date TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                license_number TEXT UNIQUE NOT NULL,
                contact_number TEXT NOT NULL,
                email TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
            )
            """
        ]
        
        for query in queries:
            self.execute_update(query)
