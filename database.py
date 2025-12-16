import sqlite3
import os

class Database:
    """Database class to handle all SQLite operations"""
    
    def __init__(self, db_name="hospital_management.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print("Database connected successfully!")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
    
    def create_tables(self):
        """Create all necessary tables"""
        try:
            # Users table for login
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    full_name TEXT,
                    email TEXT UNIQUE,
                    status TEXT DEFAULT 'Active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Patients table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    date_of_birth DATE NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT,
                    address TEXT,
                    blood_group TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Doctors table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS doctors (
                    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    specialization TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT,
                    qualification TEXT,
                    experience INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Appointments table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    appointment_date DATE NOT NULL,
                    appointment_time TEXT NOT NULL,
                    status TEXT DEFAULT 'Scheduled',
                    reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )            ''')
              # Medical Records table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS medical_records (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    visit_date DATE NOT NULL,
                    diagnosis TEXT NOT NULL,
                    prescription TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
            ''')
            
            # Billing table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS billing (
                    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    invoice_date DATE NOT NULL,
                    description TEXT,
                    services TEXT,
                    total_amount REAL NOT NULL,
                    status TEXT DEFAULT 'Pending',
                    payment_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                )
            ''')
            
            self.conn.commit()
            
            # Insert default admin user if not exists
            self.cursor.execute("SELECT * FROM users WHERE username='admin'")
            if not self.cursor.fetchone():
                self.cursor.execute(
                    "INSERT INTO users (username, password, role, full_name, email, status) VALUES (?, ?, ?, ?, ?, ?)",
                    ('admin', 'admin123', 'Admin', 'System Administrator', 'admin@hospital.com', 'Active')
                )
                self.conn.commit()
                print("Default admin user created (username: admin, password: admin123)")
            
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
    
    def execute_query(self, query, params=()):
        """Execute a query and return results"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            self.conn.rollback()
            return False
    
    def fetch_all(self, query, params=()):
        """Fetch all results from a query"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Fetch error: {e}")
            return []
    
    def fetch_one(self, query, params=()):
        """Fetch one result from a query"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Fetch error: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
