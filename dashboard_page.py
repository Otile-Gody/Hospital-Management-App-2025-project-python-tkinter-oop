import tkinter as tk
from tkinter import ttk

class DashboardPage:
    """Dashboard page showing statistics and navigation"""
    
    def __init__(self, root, database, user_info, navigate_to):
        self.root = root
        self.database = database
        self.user_info = user_info
        self.navigate_to = navigate_to
        self.frame = None
    
    def show(self):
        """Display the dashboard page"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main frame
        self.frame = tk.Frame(self.root, bg="#ecf0f1")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Top navigation bar
        self.create_navigation_bar()
        
        # Welcome section
        welcome_frame = tk.Frame(self.frame, bg="#2c3e50", height=100)
        welcome_frame.pack(fill=tk.X, padx=20, pady=20)
        welcome_frame.pack_propagate(False)
        
        welcome_label = tk.Label(
            welcome_frame,
            text=f"Welcome, {self.user_info[1]}!",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        welcome_label.pack(pady=25)
        
        # Statistics section
        stats_frame = tk.Frame(self.frame, bg="#ecf0f1")
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
          # Get statistics
        total_patients = self.database.fetch_one("SELECT COUNT(*) FROM patients")[0]
        total_doctors = self.database.fetch_one("SELECT COUNT(*) FROM doctors")[0]
        total_appointments = self.database.fetch_one("SELECT COUNT(*) FROM appointments")[0]
        total_records = self.database.fetch_one("SELECT COUNT(*) FROM medical_records")[0]
        total_users = self.database.fetch_one("SELECT COUNT(*) FROM users")[0]
        
        # Create stat cards
        stats = [
            ("Total Patients", total_patients, "#3498db", "patients"),
            ("Total Doctors", total_doctors, "#e74c3c", "doctors"),
            ("Appointments", total_appointments, "#f39c12", "appointments"),
            ("Medical Records", total_records, "#9b59b6", "records"),
            ("System Users", total_users, "#1abc9c", "users")
        ]
        
        for i, (title, value, color, page) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=color, relief=tk.RAISED, bd=2)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            tk.Label(
                card,
                text=str(value),
                font=("Arial", 36, "bold"),
                bg=color,
                fg="white"
            ).pack(pady=(20, 10))
            
            tk.Label(
                card,
                text=title,
                font=("Arial", 14),
                bg=color,
                fg="white"
            ).pack(pady=(0, 20))
            
            # Make card clickable
            for widget in card.winfo_children():
                widget.bind("<Button-1>", lambda e, p=page: self.navigate_to(p))
            card.bind("<Button-1>", lambda e, p=page: self.navigate_to(p))
            card.bind("<Enter>", lambda e, c=card: c.config(cursor="hand2"))
          # Configure grid weights        stats_frame.grid_rowconfigure(0, weight=1)
        stats_frame.grid_rowconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(2, weight=1)
    
    def create_navigation_bar(self):
        """Create the top navigation bar"""
        nav_frame = tk.Frame(self.frame, bg="#34495e", height=50)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)
        
        # Navigation buttons
        nav_buttons = [
            ("Dashboard", "dashboard"),
            ("Patients", "patients"),
            ("Doctors", "doctors"),
            ("Appointments", "appointments"),
            ("Medical Records", "records"),
            ("User Management", "users"),
            ("Logout", "logout")
        ]
        
        for text, page in nav_buttons:
            btn = tk.Button(
                nav_frame,
                text=text,
                font=("Arial", 10, "bold"),
                bg="#34495e",
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                padx=15,
                command=lambda p=page: self.navigate_to(p)
            )
            btn.pack(side=tk.LEFT, padx=5, pady=10)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2c3e50"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495e"))
