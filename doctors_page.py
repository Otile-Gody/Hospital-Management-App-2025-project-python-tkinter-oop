import tkinter as tk
from tkinter import ttk, messagebox

class DoctorsPage:
    """Doctor Management page"""
    
    def __init__(self, root, database, navigate_to):
        self.root = root
        self.database = database
        self.navigate_to = navigate_to
        self.frame = None
        self.tree = None
        self.selected_doctor = None
    
    def show(self):
        """Display the doctors page"""
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
            text="Doctor Management",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=10)
        
        # Control buttons frame
        btn_frame = tk.Frame(self.frame, bg="#ecf0f1")
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="Add Doctor",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.add_doctor_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Update Doctor",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.update_doctor_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Delete Doctor",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.delete_doctor
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Refresh",
            font=("Arial", 10, "bold"),
            bg="#95a5a6",
            fg="white",
            cursor="hand2",
            command=self.load_doctors
        ).pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = tk.Frame(self.frame, bg="#ecf0f1")
        search_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(search_frame, text="Search:", font=("Arial", 10), bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_doctors())
        
        # Table frame
        table_frame = tk.Frame(self.frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Create treeview
        columns = ("ID", "First Name", "Last Name", "Specialization", "Phone", "Email", "Qualification", "Experience")
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
        
        # Bind selection event        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Load data
        self.load_doctors()
    
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
    
    def load_doctors(self):
        """Load doctors from database"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch data
        query = "SELECT doctor_id, first_name, last_name, specialization, phone, email, qualification, experience FROM doctors"
        doctors = self.database.fetch_all(query)
        
        # Insert data
        for doctor in doctors:
            self.tree.insert('', tk.END, values=doctor)
    
    def search_doctors(self):
        """Search doctors by name or specialization"""
        search_term = self.search_entry.get().strip().lower()
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch and filter data
        query = "SELECT doctor_id, first_name, last_name, specialization, phone, email, qualification, experience FROM doctors"
        doctors = self.database.fetch_all(query)
        
        for doctor in doctors:
            if (search_term in doctor[1].lower() or 
                search_term in doctor[2].lower() or 
                search_term in doctor[3].lower()):
                self.tree.insert('', tk.END, values=doctor)
    
    def on_select(self, event):
        """Handle row selection"""
        selected = self.tree.selection()
        if selected:
            self.selected_doctor = self.tree.item(selected[0])['values']
    
    def add_doctor_dialog(self):
        """Show dialog to add new doctor"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Doctor")
        dialog.geometry("400x450")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Form fields
        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Specialization:", "specialization"),
            ("Phone:", "phone"),
            ("Email:", "email"),
            ("Qualification:", "qualification"),
            ("Experience (years):", "experience")
        ]
        
        entries = {}
        
        for i, (label, key) in enumerate(fields):
            tk.Label(dialog, text=label, font=("Arial", 10)).grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)
            
            if key == "specialization":
                entries[key] = ttk.Combobox(dialog, values=[
                    "Cardiology", "Dermatology", "Neurology", "Orthopedics", 
                    "Pediatrics", "Psychiatry", "General Medicine", "Surgery"
                ], font=("Arial", 10))
                entries[key].grid(row=i, column=1, padx=10, pady=10, sticky=tk.EW)
            else:
                entries[key] = tk.Entry(dialog, font=("Arial", 10))
                entries[key].grid(row=i, column=1, padx=10, pady=10, sticky=tk.EW)
        
        dialog.grid_columnconfigure(1, weight=1)
        
        def save():
            data = {key: widget.get().strip() for key, widget in entries.items()}
            
            if not all([data['first_name'], data['last_name'], data['specialization'], data['phone']]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            query = """INSERT INTO doctors (first_name, last_name, specialization, phone, email, qualification, experience)
                       VALUES (?, ?, ?, ?, ?, ?, ?)"""
            
            if self.database.execute_query(query, (
                data['first_name'], data['last_name'], data['specialization'],
                data['phone'], data['email'], data['qualification'], data['experience'] or 0
            )):
                messagebox.showinfo("Success", "Doctor added successfully!")
                dialog.destroy()
                self.load_doctors()
            else:
                messagebox.showerror("Error", "Failed to add doctor")
        
        tk.Button(dialog, text="Save", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=save).grid(row=len(fields), column=0, columnspan=2, pady=20, padx=10, sticky=tk.EW)
    
    def update_doctor_dialog(self):
        """Show dialog to update doctor"""
        if not self.selected_doctor:
            messagebox.showwarning("Warning", "Please select a doctor to update")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Doctor")
        dialog.geometry("400x450")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Get current doctor data
        doctor_id = self.selected_doctor[0]
        query = "SELECT * FROM doctors WHERE doctor_id=?"
        doctor = self.database.fetch_one(query, (doctor_id,))
        
        fields = [
            ("First Name:", "first_name", doctor[1]),
            ("Last Name:", "last_name", doctor[2]),
            ("Specialization:", "specialization", doctor[3]),
            ("Phone:", "phone", doctor[4]),
            ("Email:", "email", doctor[5]),
            ("Qualification:", "qualification", doctor[6]),
            ("Experience (years):", "experience", doctor[7])
        ]
        
        entries = {}
        
        for i, (label, key, value) in enumerate(fields):
            tk.Label(dialog, text=label, font=("Arial", 10)).grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)
            
            if key == "specialization":
                entries[key] = ttk.Combobox(dialog, values=[
                    "Cardiology", "Dermatology", "Neurology", "Orthopedics",
                    "Pediatrics", "Psychiatry", "General Medicine", "Surgery"
                ], font=("Arial", 10))
                entries[key].set(value)
            else:
                entries[key] = tk.Entry(dialog, font=("Arial", 10))
                entries[key].insert(0, value or "")
            
            entries[key].grid(row=i, column=1, padx=10, pady=10, sticky=tk.EW)
        
        dialog.grid_columnconfigure(1, weight=1)
        
        def update():
            data = {key: widget.get().strip() for key, widget in entries.items()}
            
            query = """UPDATE doctors SET first_name=?, last_name=?, specialization=?,
                       phone=?, email=?, qualification=?, experience=? WHERE doctor_id=?"""
            
            if self.database.execute_query(query, (
                data['first_name'], data['last_name'], data['specialization'],
                data['phone'], data['email'], data['qualification'], data['experience'] or 0, doctor_id
            )):
                messagebox.showinfo("Success", "Doctor updated successfully!")
                dialog.destroy()
                self.load_doctors()
            else:
                messagebox.showerror("Error", "Failed to update doctor")
        
        tk.Button(dialog, text="Update", bg="#3498db", fg="white", font=("Arial", 10, "bold"), command=update).grid(row=len(fields), column=0, columnspan=2, pady=20, padx=10, sticky=tk.EW)
    
    def delete_doctor(self):
        """Delete selected doctor"""
        if not self.selected_doctor:
            messagebox.showwarning("Warning", "Please select a doctor to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this doctor?"):
            doctor_id = self.selected_doctor[0]
            query = "DELETE FROM doctors WHERE doctor_id=?"
            
            if self.database.execute_query(query, (doctor_id,)):
                messagebox.showinfo("Success", "Doctor deleted successfully!")
                self.selected_doctor = None
                self.load_doctors()
            else:
                messagebox.showerror("Error", "Failed to delete doctor")
