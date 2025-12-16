"""
Main entry point for the Hospital Management System application
"""
import tkinter as tk
from tkinter import ttk, messagebox


class HospitalManagementApp:
    """Main application class for the Hospital Management System"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1024x768")
        
        # Create main container
        self.create_widgets()
        
    def create_widgets(self):
        """Create the main application widgets"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="Hospital Management System",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main content area
        content_frame = tk.Frame(self.root, bg="#ecf0f1")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_label = tk.Label(
            content_frame,
            text="Welcome to the Hospital Management System",
            font=("Arial", 18),
            bg="#ecf0f1"
        )
        welcome_label.pack(pady=40)
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg="#ecf0f1")
        button_frame.pack(pady=20)
        
        # Sample buttons for different modules
        modules = [
            ("Patient Management", self.open_patient_module),
            ("Doctor Management", self.open_doctor_module),
            ("Appointment Scheduling", self.open_appointment_module),
            ("Medical Records", self.open_records_module)
        ]
        
        for text, command in modules:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 12),
                bg="#3498db",
                fg="white",
                padx=20,
                pady=10,
                relief=tk.RAISED,
                cursor="hand2"
            )
            btn.pack(pady=10, fill=tk.X)
    
    def open_patient_module(self):
        """Open patient management module"""
        messagebox.showinfo("Module", "Patient Management Module - Coming Soon")
    
    def open_doctor_module(self):
        """Open doctor management module"""
        messagebox.showinfo("Module", "Doctor Management Module - Coming Soon")
    
    def open_appointment_module(self):
        """Open appointment scheduling module"""
        messagebox.showinfo("Module", "Appointment Scheduling Module - Coming Soon")
    
    def open_records_module(self):
        """Open medical records module"""
        messagebox.showinfo("Module", "Medical Records Module - Coming Soon")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = HospitalManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
