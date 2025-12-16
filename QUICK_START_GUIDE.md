# Hospital Management System - Quick Start Guide

## 🚀 How to Run the Application

### Method 1: Using Batch File (Recommended for Windows)
1. Double-click on `run.bat` file
2. The application will start automatically

### Method 2: Using Command Line
1. Open PowerShell or Command Prompt
2. Navigate to the project folder:
   ```
   cd "c:\Users\JUDICIARY\Desktop\OTILE GODFREY"
   ```
3. Run the application:
   ```
   python main.py
   ```

### Method 3: Using Python Directly
1. Right-click on `main.py`
2. Select "Open with" → "Python"

## 🔐 Login Credentials

**Default Admin Account:**
- Username: `admin`
- Password: `admin123`

## 📋 Application Overview

The Hospital Management System includes **6 main pages**:

### 1. Login Page
- Secure authentication system
- Enter username and password to access the system

### 2. Dashboard
- Overview of system statistics
- Shows total patients, doctors, appointments, and medical records
- Click on any card to navigate to that section

### 3. Patient Management Page
- **Add Patient**: Click "Add Patient" button and fill in the form
- **Update Patient**: Select a patient, then click "Update Patient"
- **Delete Patient**: Select a patient, then click "Delete Patient"
- **Search**: Type in the search box to find patients by name or phone

### 4. Doctor Management Page
- **Add Doctor**: Click "Add Doctor" and enter doctor information
- **Update Doctor**: Select a doctor, then click "Update Doctor"
- **Delete Doctor**: Select a doctor, then click "Delete Doctor"
- **Search**: Search doctors by name or specialization

### 5. Appointment Scheduling Page
- **Schedule Appointment**: Click "Add Appointment"
- Select patient from dropdown
- Select doctor from dropdown
- Choose date and time
- Set status (Scheduled/Completed/Cancelled)
- Add reason for visit

### 6. Medical Records Page
- **Create Record**: Click "Add Record"
- Select patient and doctor
- Enter diagnosis, prescription, and notes
- **View Details**: Select a record and click "View Details"
- **Search**: Search records by patient name

## 📊 Sample Workflow

### Complete Patient Journey Example:

1. **Login** to the system (admin/admin123)

2. **Add a Patient**:
   - Go to Patients page
   - Click "Add Patient"
   - Fill in: John Doe, Male, DOB: 1990-01-15, Phone: 555-1234, Blood Group: A+

3. **Add a Doctor**:
   - Go to Doctors page
   - Click "Add Doctor"
   - Fill in: Dr. Smith, Specialization: Cardiology, Phone: 555-5678

4. **Schedule Appointment**:
   - Go to Appointments page
   - Click "Add Appointment"
   - Select "John Doe" as patient
   - Select "Dr. Smith" as doctor
   - Set date and time
   - Reason: "Regular checkup"

5. **Create Medical Record**:
   - Go to Medical Records page
   - Click "Add Record"
   - Select patient and doctor
   - Enter diagnosis: "Healthy, normal blood pressure"
   - Add prescription if needed
   - Add any notes

## 🗂️ Database Information

- **Database Type**: SQLite
- **Database File**: `hospital_management.db` (created automatically)
- **Location**: Same folder as application files

### Viewing Database with DB Browser for SQLite:
1. Download DB Browser for SQLite (free): https://sqlitebrowser.org/
2. Open DB Browser
3. Click "Open Database"
4. Select `hospital_management.db` from the project folder
5. Browse all tables and data

## 📱 Navigation

All pages have a navigation bar at the top with buttons:
- **Dashboard**: Return to main dashboard
- **Patients**: Manage patients
- **Doctors**: Manage doctors
- **Appointments**: Schedule and view appointments
- **Medical Records**: View and create medical records
- **Logout**: Exit and return to login screen

## 💡 Tips

1. **Always add patients and doctors before creating appointments or medical records**
2. **Use the search feature** to quickly find specific records
3. **Refresh button** updates the table with latest data
4. **Select a row** in the table before updating or deleting
5. **All data is saved** in the SQLite database automatically

## ⚠️ Important Notes

- The application requires Python 3.7 or higher
- Tkinter should be installed (usually comes with Python)
- No internet connection required - fully offline application
- All data is stored locally in `hospital_management.db`

## 🔧 Troubleshooting

### Application won't start:
- Make sure Python is installed
- Check if Python is added to PATH
- Try running from command line to see error messages

### "Module not found" error:
- Make sure all Python files are in the same folder
- Don't rename or move any files

### Database errors:
- Delete `hospital_management.db` file to start fresh
- The database will be recreated automatically

## 📧 Features Summary

✅ User Authentication
✅ Patient Management (CRUD operations)
✅ Doctor Management (CRUD operations)
✅ Appointment Scheduling
✅ Medical Records Management
✅ Search Functionality
✅ SQLite Database Integration
✅ Modern UI with Tkinter
✅ Complete OOP Implementation

---

**Enjoy using the Hospital Management System!** 🏥
