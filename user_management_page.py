import tkinter as tk
from tkinter import ttk, messagebox
import re

class UserManagementPage:
    """User Management page for administrators"""
    
    def __init__(self, root, database, navigate_to):
        self.root = root
        self.database = database
        self.navigate_to = navigate_to
        self.frame = None
        self.tree = None
        self.selected_user = None
    
    def show(self):
        """Display the user management page"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main frame
        self.frame = tk.Frame(self.root, bg="#ecf0f1")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Navigation bar
        self.create_navigation_bar()
        
        # Title
        title_frame = tk.Frame(self.frame, bg="#2c3e50")
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            title_frame,
            text="User Management",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=10)
        
        # Control buttons frame
        btn_frame = tk.Frame(self.frame, bg="#ecf0f1")
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="View Details",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.view_user_details
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Change Password",
            font=("Arial", 10, "bold"),
            bg="#f39c12",
            fg="white",
            cursor="hand2",
            command=self.change_password_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Deactivate User",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.toggle_user_status
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Delete User",
            font=("Arial", 10, "bold"),
            bg="#c0392b",
            fg="white",
            cursor="hand2",
            command=self.delete_user
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Refresh",
            font=("Arial", 10, "bold"),
            bg="#95a5a6",
            fg="white",
            cursor="hand2",
            command=self.load_users
        ).pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = tk.Frame(self.frame, bg="#ecf0f1")
        search_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(search_frame, text="Search:", font=("Arial", 10), bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_users())
        
        # Table frame
        table_frame = tk.Frame(self.frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Create treeview
        columns = ("ID", "Username", "Full Name", "Email", "Role", "Status", "Created Date")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )
        
        # Configure scrollbars
        y_scrollbar.config(command=self.tree.yview)
        x_scrollbar.config(command=self.tree.xview)
        
        # Define column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.CENTER)
        
        # Pack scrollbars and treeview
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Load data
        self.load_users()
    
    def create_navigation_bar(self):
        """Create navigation bar"""
        nav_frame = tk.Frame(self.frame, bg="#34495e", height=50)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)
        
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
                nav_frame, text=text, font=("Arial", 10, "bold"),
                bg="#34495e", fg="white", relief=tk.FLAT,
                cursor="hand2", padx=15,
                command=lambda p=page: self.navigate_to(p)
            )
            btn.pack(side=tk.LEFT, padx=5, pady=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2c3e50"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495e"))
    
    def load_users(self):
        """Load users from database"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch data
        query = """SELECT user_id, username, full_name, email, role, status, 
                   DATE(created_at) FROM users ORDER BY created_at DESC"""
        users = self.database.fetch_all(query)
        
        # Insert data with color coding
        for user in users:
            tags = ('inactive',) if user[5] == 'Inactive' else ()
            self.tree.insert('', tk.END, values=user, tags=tags)
        
        # Configure tag colors
        self.tree.tag_configure('inactive', background='#ffcccc')
    
    def search_users(self):
        """Search users by username or full name"""
        search_term = self.search_entry.get().strip().lower()
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch and filter data
        query = """SELECT user_id, username, full_name, email, role, status, 
                   DATE(created_at) FROM users ORDER BY created_at DESC"""
        users = self.database.fetch_all(query)
        
        for user in users:
            if (search_term in user[1].lower() or 
                (user[2] and search_term in user[2].lower())):
                tags = ('inactive',) if user[5] == 'Inactive' else ()
                self.tree.insert('', tk.END, values=user, tags=tags)
        
        self.tree.tag_configure('inactive', background='#ffcccc')
    
    def on_select(self, event):
        """Handle row selection"""
        selected = self.tree.selection()
        if selected:
            self.selected_user = self.tree.item(selected[0])['values']
    
    def view_user_details(self):
        """View detailed information of selected user"""
        if not self.selected_user:
            messagebox.showwarning("Warning", "Please select a user to view")
            return
        
        user_id = self.selected_user[0]
        query = "SELECT * FROM users WHERE user_id=?"
        user = self.database.fetch_one(query, (user_id,))
        
        if not user:
            messagebox.showerror("Error", "User not found")
            return
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title("User Details")
        details_window.geometry("500x450")
        details_window.resizable(False, False)
        details_window.grab_set()
        
        # Header
        header_frame = tk.Frame(details_window, bg="#2c3e50")
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="User Details", font=("Arial", 18, "bold"), bg="#2c3e50", fg="white").pack(pady=15)
        
        # Content frame
        content_frame = tk.Frame(details_window, bg="white", padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display information
        info = [
            ("User ID:", user[0]),
            ("Username:", user[1]),
            ("Full Name:", user[4] or "N/A"),
            ("Email:", user[5] or "N/A"),
            ("Role:", user[3]),
            ("Status:", user[6]),
            ("Created Date:", user[7])
        ]
        
        for i, (label, value) in enumerate(info):
            tk.Label(content_frame, text=label, font=("Arial", 11, "bold"), bg="white", anchor=tk.W).grid(row=i, column=0, sticky=tk.W, pady=10, padx=10)
            
            value_label = tk.Label(content_frame, text=str(value), font=("Arial", 11), bg="white", anchor=tk.W)
            value_label.grid(row=i, column=1, sticky=tk.W, pady=10, padx=10)
            
            # Color code status
            if label == "Status:":
                if value == "Active":
                    value_label.config(fg="green")
                else:
                    value_label.config(fg="red")
        
        # Close button
        tk.Button(details_window, text="Close", bg="#95a5a6", fg="white", font=("Arial", 10, "bold"), command=details_window.destroy).pack(pady=10)
    
    def change_password_dialog(self):
        """Show dialog to change user password"""
        if not self.selected_user:
            messagebox.showwarning("Warning", "Please select a user to change password")
            return
        
        # Don't allow changing admin password this way for security
        if self.selected_user[1] == 'admin':
            messagebox.showwarning("Warning", "Admin password cannot be changed from this interface")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Password")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Change password for: {self.selected_user[1]}", font=("Arial", 12, "bold")).pack(pady=20)
        
        # New Password
        tk.Label(dialog, text="New Password:", font=("Arial", 10)).pack(pady=5)
        new_password_entry = tk.Entry(dialog, font=("Arial", 10), show="*", width=30)
        new_password_entry.pack(pady=5)
        
        # Confirm Password
        tk.Label(dialog, text="Confirm Password:", font=("Arial", 10)).pack(pady=5)
        confirm_password_entry = tk.Entry(dialog, font=("Arial", 10), show="*", width=30)
        confirm_password_entry.pack(pady=5)
        
        def change():
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            if not new_password or not confirm_password:
                messagebox.showerror("Error", "Please enter both passwords")
                return
            
            if len(new_password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters")
                return
            
            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            query = "UPDATE users SET password=? WHERE user_id=?"
            if self.database.execute_query(query, (new_password, self.selected_user[0])):
                messagebox.showinfo("Success", "Password changed successfully!")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to change password")
        
        tk.Button(dialog, text="Change Password", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=change).pack(pady=20)
    
    def toggle_user_status(self):
        """Toggle user active/inactive status"""
        if not self.selected_user:
            messagebox.showwarning("Warning", "Please select a user")
            return
        
        # Don't allow deactivating admin
        if self.selected_user[1] == 'admin':
            messagebox.showwarning("Warning", "Admin account cannot be deactivated")
            return
        
        current_status = self.selected_user[5]
        new_status = "Inactive" if current_status == "Active" else "Active"
        
        if messagebox.askyesno("Confirm", f"Change user status to {new_status}?"):
            query = "UPDATE users SET status=? WHERE user_id=?"
            
            if self.database.execute_query(query, (new_status, self.selected_user[0])):
                messagebox.showinfo("Success", f"User status changed to {new_status}")
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to change user status")
    
    def delete_user(self):
        """Delete selected user"""
        if not self.selected_user:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        # Don't allow deleting admin
        if self.selected_user[1] == 'admin':
            messagebox.showwarning("Warning", "Admin account cannot be deleted")
            return
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to permanently delete user '{self.selected_user[1]}'?\n\nThis action cannot be undone!"):
            query = "DELETE FROM users WHERE user_id=?"
            
            if self.database.execute_query(query, (self.selected_user[0],)):
                messagebox.showinfo("Success", "User deleted successfully!")
                self.selected_user = None
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to delete user")
