import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class LoginPage:
    """Login page for the Hospital Management System"""
    
    def __init__(self, root, database, on_login_success, show_register=None):
        self.root = root
        self.database = database
        self.on_login_success = on_login_success
        self.show_register = show_register
        self.frame = None
        
    def show(self):
        """Display the login page"""
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
        
        # Login container
        login_container = tk.Frame(self.frame, bg="white", relief=tk.RAISED, bd=2)
        login_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=400)
        
        # Login header
        header_label = tk.Label(
            login_container,
            text="Login",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        header_label.pack(pady=20)
        
        # Username
        username_frame = tk.Frame(login_container, bg="white")
        username_frame.pack(pady=10, padx=30, fill=tk.X)
        
        tk.Label(
            username_frame,
            text="Username:",
            font=("Arial", 12),
            bg="white"
        ).pack(anchor=tk.W)
        
        self.username_entry = tk.Entry(
            username_frame,
            font=("Arial", 12),
            relief=tk.SOLID,
            bd=1
        )
        self.username_entry.pack(fill=tk.X, pady=5)
        
        # Password
        password_frame = tk.Frame(login_container, bg="white")
        password_frame.pack(pady=10, padx=30, fill=tk.X)
        
        tk.Label(
            password_frame,
            text="Password:",
            font=("Arial", 12),
            bg="white"
        ).pack(anchor=tk.W)
        
        self.password_entry = tk.Entry(
            password_frame,
            font=("Arial", 12),
            show="*",
            relief=tk.SOLID,
            bd=1
        )
        self.password_entry.pack(fill=tk.X, pady=5)
        
        # Login button
        login_btn = tk.Button(
            login_container,
            text="Login",            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            command=self.login
        )
        login_btn.pack(pady=20, padx=30, fill=tk.X)
        
        # Info label
        info_label = tk.Label(
            login_container,
            text="Default: username=admin, password=admin123",
            font=("Arial", 9),
            bg="white",
            fg="#7f8c8d"
        )
        info_label.pack(pady=5)
        
        # Register link (only show if show_register is provided)
        if self.show_register:
            register_frame = tk.Frame(login_container, bg="white")
            register_frame.pack(pady=5)
            
            tk.Label(
                register_frame,
                text="Don't have an account?",
                font=("Arial", 10),
                bg="white",
                fg="#7f8c8d"
            ).pack(side=tk.LEFT)
            
            register_link = tk.Label(
                register_frame,
                text=" Register here",
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#3498db",
                cursor="hand2"
            )
            register_link.pack(side=tk.LEFT)
            register_link.bind("<Button-1>", lambda e: self.show_register())
        
        # Bind Enter key to login        self.username_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Focus on username entry
        self.username_entry.focus()
    
    def login(self):
        """Handle login logic"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Check credentials and user status
        query = "SELECT user_id, username, role, status FROM users WHERE username=? AND password=?"
        user = self.database.fetch_one(query, (username, password))
        
        if user:
            # Check if user account is active
            if user[3] == "Inactive":
                messagebox.showerror("Error", "Your account has been deactivated. Please contact administrator.")
                return
            
            messagebox.showinfo("Success", f"Welcome {user[1]}!")
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
