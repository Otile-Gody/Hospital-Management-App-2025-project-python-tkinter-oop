# Hospital Management App 2025

A desktop application for managing hospital operations, built with Python, Tkinter, and Object-Oriented Programming principles.

**Individual Project - UTAMU Year 2, Semester 1**

## Project Structure

```
hospital_management/
├── __init__.py           # Package initialization
├── main.py              # Main application entry point
├── models/              # Data models (Patient, Doctor, Appointment)
│   ├── __init__.py
│   ├── patient.py
│   ├── doctor.py
│   └── appointment.py
├── views/               # Tkinter UI components
│   └── __init__.py
├── controllers/         # Business logic
│   └── __init__.py
├── utils/               # Utility functions
│   └── __init__.py
└── database/            # Database operations
    ├── __init__.py
    └── db_manager.py
```

## Features

- **Patient Management**: Register and manage patient information
- **Doctor Management**: Manage doctor profiles and specializations
- **Appointment Scheduling**: Schedule and track patient appointments
- **Medical Records**: Store and retrieve medical history

## Requirements

- Python 3.7 or higher
- Tkinter (included with Python)
- SQLite3 (included with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Otile-Gody/Hospital-Management-App-2025-project-python-tkinter-oop.git
cd Hospital-Management-App-2025-project-python-tkinter-oop
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies (if any):
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python -m hospital_management.main
```

Or directly:
```bash
cd hospital_management
python main.py
```

## Project Architecture

This project follows Object-Oriented Programming principles with a clear separation of concerns:

- **Models**: Define data structures and entity relationships
- **Views**: Handle user interface presentation
- **Controllers**: Manage business logic and coordinate between models and views
- **Database**: Handle data persistence using SQLite
- **Utils**: Provide helper functions for common tasks

## Development

The application is structured as a Python package in the `hospital_management/` folder, making it easy to:
- Import modules
- Maintain code organization
- Scale the application
- Add new features

## License

This is an academic project for educational purposes.

## Author

Otile Godfrey - UTAMU Student
