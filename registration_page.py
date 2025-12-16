import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re

class RegistrationPage:
    """Registration page for new users"""
    
    def __init__(self, root, database, on_registration_success, show_login):
        self.root = root
        self.database = database
        self.on_registration_success = on_registration_success
        self.show_login = show_login
        self.frame = None
        
    def show(self):
        """Display the registration page"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main frame
        self.frame = tk.Frame(self.root, bg="#f0f0f0")
        self.frame.pack(fill=tk.BOTH, expand=True)
          # Title
        title_frame = tk.Frame(self.frame, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="Hospital Management System",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Create outer container for the registration form
        outer_container = tk.Frame(self.frame, bg="white", relief=tk.RAISED, bd=2)
        outer_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=550)
        
        # Registration header (fixed at top)
        header_label = tk.Label(
            outer_container,
            text="Create New Account",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        header_label.pack(pady=20)
        
        # Create canvas and scrollbar for scrollable content
        canvas = tk.Canvas(outer_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer_container, orient="vertical", command=canvas.yview)
        
        # Create frame inside canvas for form fields
        register_container = tk.Frame(canvas, bg="white")
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create window in canvas
        canvas_frame = canvas.create_window((0, 0), window=register_container, anchor="nw")
        
        # Configure canvas scroll region when frame changes size
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        register_container.bind("<Configure>", on_frame_configure)
        
        # Bind mousewheel to scroll
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Make canvas window resize with canvas
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_frame, width=event.width)
        
        canvas.bind("<Configure>", on_canvas_configure)
        
        # Full Name
        fullname_frame = tk.Frame(register_container, bg="white")
        fullname_frame.pack(pady=8, padx=30, fill=tk.X)
        
        tk.Label(
            fullname_frame,
            text="Full Name:",
            font=("Arial", 11),
            bg="white"
        ).pack(anchor=tk.W)
        
        self.fullname_entry = tk.Entry(
            fullname_frame,
            font=("Arial", 11),
            relief=tk.SOLID,
            bd=1
        )
        self.fullname_entry.pack(fill=tk.X, pady=5)
        
        # Username
        username_frame = tk.Frame(register_container, bg="white")
        username_frame.pack(pady=8, padx=30, fill=tk.X)
        
        tk.Label(
            username_frame,
            text="Username:",
            font=("Arial", 11),
            bg="white"
        ).pack(anchor=tk.W)
        
        self.username_entry = tk.Entry(
            username_frame,
            font=("Arial", 11),
            relief=tk.SOLID,
            bd=1
        )
        self.username_entry.pack(fill=tk.X, pady=5)
        
        # Email
        email_frame = tk.Frame(register_container, bg="white")
        email_frame.pack(pady=8, padx=30, fill=tk.X)
        
        tk.Label(
            email_frame,
            text="Email:",
            font=("Arial", 11),
            bg="white"
        ).pack(anchor=tk.W)
        
        self.email_entry = tk.Entry(
            email_frame,
            font=("Arial", 11),
            relief=tk.SOLID,
            bd=1
        )
        self.email_entry.pack(fill=tk.X, pady=5)
        
        # Role
        role_frame = tk.Frame(register_container, bg="white")
        role_frame.pack(pady=8, padx=30, fill=tk.X)
        
        tk.Label(
            role_frame,
            text="Role:",
            font=("Arial", 11),
            bg="white"
        ).pack(anchor=tk.W)
        
        self.role_var = tk.StringVar()
        role_combo = ttk.Combobox(
            role_frame,
            textvariable=self.role_var,
            values=["Admin", "Doctor", "Nurse", "Receptionist"],
            font=("Arial", 11),
            state="readonly"
        )
        role_combo.pack(fill=tk.X, pady=5)
        role_combo.set("Receptionist")
        
        # Password
        password_frame = tk.Frame(register_container, bg="white")
        password_frame.pack(pady=8, padx=30, fill=tk.X)
        
        tk.Label(
            password_frame,
            text="Password:",
            font=("Arial", 11),
            bg="white"
        ).pack(anchor=tk.W)
        
        self.password_entry = tk.Entry(
            password_frame,
            font=("Arial", 11),
            show="*",
            relief=tk.SOLID,
            bd=1
        )
        self.password_entry.pack(fill=tk.X, pady=5)
        
        # Confirm Password
        confirm_frame = tk.Frame(register_container, bg="white")
        confirm_frame.pack(pady=8, padx=30, fill=tk.X)
        
        tk.Label(
            confirm_frame,
            text="Confirm Password:",
            font=("Arial", 11),
            bg="white"
        ).pack(anchor=tk.W)
        
        self.confirm_entry = tk.Entry(
            confirm_frame,
            font=("Arial", 11),
            show="*",
            relief=tk.SOLID,
            bd=1
        )
        self.confirm_entry.pack(fill=tk.X, pady=5)
        
        # Register button
        register_btn = tk.Button(
            register_container,
            text="Register",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            command=self.register
        )
        register_btn.pack(pady=15, padx=30, fill=tk.X)
        
        # Login link
        login_frame = tk.Frame(register_container, bg="white")
        login_frame.pack(pady=5)
        
        tk.Label(
            login_frame,
            text="Already have an account?",
            font=("Arial", 10),
            bg="white",
            fg="#7f8c8d"
        ).pack(side=tk.LEFT)
        
        login_link = tk.Label(
            login_frame,
            text=" Login here",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#3498db",
            cursor="hand2"
        )
        login_link.pack(side=tk.LEFT)
        login_link.bind("<Button-1>", lambda e: self.show_login())
        
        # Bind Enter key to register
        self.confirm_entry.bind('<Return>', lambda e: self.register())
        
        # Focus on fullname entry
        self.fullname_entry.focus()
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_username(self, username):
        """Validate username format"""
        # Username should be alphanumeric and 3-20 characters
        if len(username) < 3 or len(username) > 20:
            return False
        return username.isalnum()
    
    def validate_password(self, password):
        """Validate password strength"""
        # Password should be at least 6 characters
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        # Check for at least one letter and one number
        has_letter = any(c.isalpha() for c in password)
        has_number = any(c.isdigit() for c in password)
        
        if not (has_letter and has_number):
            return False, "Password must contain both letters and numbers"
        
        return True, "Valid"
    
    def register(self):
        """Handle registration logic"""
        fullname = self.fullname_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        role = self.role_var.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()
        
        # Validate all fields are filled
        if not all([fullname, username, email, role, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Validate full name
        if len(fullname) < 3:
            messagebox.showerror("Error", "Full name must be at least 3 characters")
            return
        
        # Validate username
        if not self.validate_username(username):
            messagebox.showerror("Error", "Username must be 3-20 alphanumeric characters")
            return
        
        # Check if username already exists
        query = "SELECT user_id FROM users WHERE username=?"
        existing_user = self.database.fetch_one(query, (username,))
        if existing_user:
            messagebox.showerror("Error", "Username already exists. Please choose another.")
            return
        
        # Validate email
        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        # Check if email already exists
        query = "SELECT user_id FROM users WHERE email=?"
        existing_email = self.database.fetch_one(query, (email,))
        if existing_email:
            messagebox.showerror("Error", "Email already registered. Please use another.")
            return
        
        # Validate password
        is_valid, message = self.validate_password(password)
        if not is_valid:
            messagebox.showerror("Error", message)
            return
        
        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Insert new user
        query = """INSERT INTO users (username, password, role, full_name, email, status)
                   VALUES (?, ?, ?, ?, ?, ?)"""
        
        if self.database.execute_query(query, (username, password, role, fullname, email, "Active")):
            messagebox.showinfo("Success", f"Account created successfully!\nUsername: {username}\nRole: {role}")
            
            # Get the newly created user info
            user_query = "SELECT user_id, username, role FROM users WHERE username=?"
            user = self.database.fetch_one(user_query, (username,))
            
            if user:
                self.on_registration_success(user)
        else:
            messagebox.showerror("Error", "Failed to create account. Please try again.")
