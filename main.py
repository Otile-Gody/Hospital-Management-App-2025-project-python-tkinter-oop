"""
Hospital Management System
A comprehensive desktop application for managing hospital operations
Built with Python Tkinter and SQLite Database

Features:
- User Authentication
- Patient Management
- Doctor Management
- Appointment Scheduling
- Medical Records Management
"""

import tkinter as tk
from tkinter import messagebox
import sys

# Import custom modules
from database import Database
from login_page import LoginPage
from registration_page import RegistrationPage
from dashboard_page import DashboardPage
from patients_page import PatientsPage
from doctors_page import DoctorsPage
from appointments_page import AppointmentsPage
from medical_records_page import MedicalRecordsPage
from billing_page import BillingPage
from user_management_page import UserManagementPage


class HospitalManagementSystem:
    """Main Application Class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hospital Management System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Center the window
        self.center_window()
        
        # Initialize database
        self.database = Database()
        
        # User information
        self.current_user = None
          # Current page
        self.current_page = None
        
        # Show login page
        self.show_login()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Center the application window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def show_login(self):
        """Display the login page"""
        self.current_page = LoginPage(self.root, self.database, self.on_login_success, self.show_register)
        self.current_page.show()
    
    def show_register(self):
        """Display the registration page"""
        self.current_page = RegistrationPage(self.root, self.database, self.on_registration_success, self.show_login)
        self.current_page.show()
    
    def on_login_success(self, user_info):
        """Callback for successful login"""
        self.current_user = user_info
        self.show_dashboard()
    
    def on_registration_success(self, user_info):
        """Callback for successful registration"""
        self.current_user = user_info
        self.show_dashboard()
    
    def show_dashboard(self):
        """Display the dashboard page"""
        if not self.current_user:
            self.show_login()
            return
        
        self.current_page = DashboardPage(
            self.root,
            self.database,
            self.current_user,
            self.navigate_to
        )
        self.current_page.show()
    
    def show_patients(self):
        """Display the patients management page"""
        self.current_page = PatientsPage(
            self.root,
            self.database,
            self.navigate_to
        )
        self.current_page.show()
    
    def show_doctors(self):
        """Display the doctors management page"""
        self.current_page = DoctorsPage(
            self.root,
            self.database,
            self.navigate_to
        )
        self.current_page.show()
    
    def show_appointments(self):
        """Display the appointments management page"""
        self.current_page = AppointmentsPage(
            self.root,
            self.database,
            self.navigate_to
        )
        self.current_page.show()
    
    def show_medical_records(self):
        """Display the medical records management page"""
        self.current_page = MedicalRecordsPage(
            self.root,
            self.database,
            self.navigate_to
        )
        self.current_page.show()
    
    def show_billing(self):
        """Display the billing management page"""
        self.current_page = BillingPage(
            self.root,
            self.database,
            self.navigate_to
                )
        self.current_page.show()
    
    def show_user_management(self):
        """Display the user management page"""
        self.current_page = UserManagementPage(
            self.root,
            self.database,
            self.navigate_to
        )
        self.current_page.show()
    
    def navigate_to(self, page_name):
        """Navigate to a specific page"""
        if page_name == "dashboard":
            self.show_dashboard()
        elif page_name == "patients":
            self.show_patients()
        elif page_name == "doctors":
            self.show_doctors()
        elif page_name == "appointments":
            self.show_appointments()
        elif page_name == "records":
            self.show_medical_records()
        elif page_name == "billing":
            self.show_billing()
        elif page_name == "users":
            self.show_user_management()
        elif page_name == "logout":
            self.logout()
    
    def logout(self):
        """Logout the current user"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.show_login()
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.database.close()
            self.root.destroy()
            sys.exit(0)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        app = HospitalManagementSystem()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
