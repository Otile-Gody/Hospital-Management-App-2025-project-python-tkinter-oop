# Hospital Management System

A comprehensive desktop application for managing hospital operations built with Python Tkinter and SQLite database with full authentication system.

## Features

### 1. **User Authentication System**
- **Login Page**: Secure login with username and password
- **Registration Page**: New user registration with validation
  - Email validation
  - Password strength validation (minimum 6 characters, must contain letters and numbers)
  - Username uniqueness check
  - Role-based registration (Admin, Doctor, Nurse, Receptionist)
- **User Management**: Admin can manage all users
  - View user details
  - Change user passwords
  - Activate/Deactivate user accounts
  - Delete users (except admin)
- **Account Status**: Active/Inactive user status tracking
- Default admin credentials provided

### 2. **Dashboard**
- Overview of system statistics
- Quick access to all modules
- Visual statistics cards

### 3. **Patient Management**
- Add, update, and delete patient records
- Search patients by name or phone
- Store comprehensive patient information:
  - Personal details (name, gender, DOB)
  - Contact information (phone, email, address)
  - Medical information (blood group)

### 4. **Doctor Management**
- Manage doctor profiles
- Specialization tracking
- Store doctor information:
  - Personal details
  - Specialization
  - Qualifications and experience

### 5. **Appointment Scheduling**
- Schedule appointments between patients and doctors
- Track appointment status (Scheduled, Completed, Cancelled)
- View all appointments with patient and doctor details

### 6. **Medical Records**
- Create comprehensive medical records
- Link records to patients and doctors
- Store:
  - Diagnosis
  - Prescriptions
  - Medical notes
- View detailed record information

### 7. **User Management (Admin Only)**
- View all registered users
- View user details and activity
- Change user passwords
- Activate/Deactivate user accounts
- Delete users (except admin)
- Role-based access control

## Technologies Used

- **Python 3.x**: Core programming language
- **Tkinter**: GUI framework for desktop application
- **SQLite3**: Embedded database for data storage
- **OOP Principles**: Object-oriented design pattern

## Database Schema

The application uses SQLite with the following tables:

1. **users**: User authentication
2. **patients**: Patient information
3. **doctors**: Doctor profiles
4. **appointments**: Appointment scheduling
5. **medical_records**: Patient medical history

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Tkinter (usually comes with Python)

### Running the Application

1. Navigate to the project directory:
```bash
cd "c:\Users\JUDICIARY\Desktop\OTILE GODFREY"
```

2. Run the application:
```bash
python main.py
```

### Default Login Credentials
- **Username**: admin
- **Password**: admin123

## File Structure

```
hospital_management_system/
│
├── main.py                      # Main application entry point
├── database.py                  # Database operations and setup
├── login_page.py               # Login page (Page 1)
├── dashboard_page.py           # Dashboard (Page 2)
├── patients_page.py            # Patient management (Page 3)
├── doctors_page.py             # Doctor management (Page 4)
├── appointments_page.py        # Appointments (Page 5)
├── medical_records_page.py     # Medical records (Page 6)
├── user_management_page.py     # User management (Page 7)
├── registration_page.py        # Registration page
├── hospital_management.db      # SQLite database (auto-generated)
└── README.md                   # This file
```

## Usage Guide

### Adding a Patient
1. Navigate to "Patients" from the navigation bar
2. Click "Add Patient" button
3. Fill in all required fields
4. Click "Save"

### Scheduling an Appointment
1. Navigate to "Appointments"
2. Click "Add Appointment"
3. Select patient and doctor from dropdowns
4. Choose date, time, and status
5. Add reason for visit
6. Click "Save"

### Creating Medical Records
1. Navigate to "Medical Records"
2. Click "Add Record"
3. Select patient and doctor
4. Enter diagnosis, prescription, and notes
5. Click "Save"

## Features Highlights

- **Intuitive Navigation**: Easy-to-use navigation bar on all pages
- **Search Functionality**: Quick search on all management pages
- **Data Validation**: Form validation to ensure data integrity
- **Responsive Design**: Clean and modern UI design
- **Database Integration**: All data persisted in SQLite database
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality

## Database Browser Integration

The application uses SQLite, which can be viewed and managed using:
- **DB Browser for SQLite** (recommended)
- Any SQLite database viewer

To view the database:
1. Open DB Browser for SQLite
2. Open the `hospital_management.db` file
3. Browse tables and data

## Future Enhancements

- Patient billing and invoicing
- Inventory management for medical supplies
- Report generation (PDF/Excel)
- User role-based access control
- Email/SMS notifications
- Backup and restore functionality

## Developer Information

- **Project Type**: Desktop Application
- **Architecture**: MVC Pattern with OOP
- **Database**: SQLite3 (Embedded)
- **UI Framework**: Tkinter

## License

This is an educational project for learning purposes.

## Support

For issues or questions, please check the code documentation or contact the developer.

---
**Developed with ❤️ using Python & Tkinter**
