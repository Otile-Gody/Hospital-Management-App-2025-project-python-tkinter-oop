import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class PatientsPage:
    """Patient Management page"""
    
    def __init__(self, root, database, navigate_to):
        self.root = root
        self.database = database
        self.navigate_to = navigate_to
        self.frame = None
        self.tree = None
        self.selected_patient = None
    
    def show(self):
        """Display the patients page"""
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
            text="Patient Management",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=10)
        
        # Control buttons frame
        btn_frame = tk.Frame(self.frame, bg="#ecf0f1")
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="Add Patient",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.add_patient_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Update Patient",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.update_patient_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Delete Patient",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.delete_patient
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Refresh",
            font=("Arial", 10, "bold"),
            bg="#95a5a6",
            fg="white",
            cursor="hand2",
            command=self.load_patients
        ).pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = tk.Frame(self.frame, bg="#ecf0f1")
        search_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(search_frame, text="Search:", font=("Arial", 10), bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_patients())
        
        # Table frame
        table_frame = tk.Frame(self.frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Create treeview
        columns = ("ID", "First Name", "Last Name", "Gender", "DOB", "Phone", "Email", "Blood Group")
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
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        # Pack scrollbars and treeview
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
          # Load data
        self.load_patients()
    
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
    
    def load_patients(self):
        """Load patients from database"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch data
        query = "SELECT patient_id, first_name, last_name, gender, date_of_birth, phone, email, blood_group FROM patients"
        patients = self.database.fetch_all(query)
        
        # Insert data
        for patient in patients:
            self.tree.insert('', tk.END, values=patient)
    
    def search_patients(self):
        """Search patients by name or phone"""
        search_term = self.search_entry.get().strip().lower()
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch and filter data
        query = "SELECT patient_id, first_name, last_name, gender, date_of_birth, phone, email, blood_group FROM patients"
        patients = self.database.fetch_all(query)
        
        for patient in patients:
            if (search_term in patient[1].lower() or 
                search_term in patient[2].lower() or 
                search_term in patient[5].lower()):
                self.tree.insert('', tk.END, values=patient)
    
    def on_select(self, event):
        """Handle row selection"""
        selected = self.tree.selection()
        if selected:
            self.selected_patient = self.tree.item(selected[0])['values']
    
    def add_patient_dialog(self):
        """Show dialog to add new patient"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Patient")
        dialog.geometry("400x500")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Form fields
        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Gender:", "gender"),
            ("Date of Birth (YYYY-MM-DD):", "dob"),
            ("Phone:", "phone"),
            ("Email:", "email"),
            ("Address:", "address"),
            ("Blood Group:", "blood_group")
        ]
        
        entries = {}
        
        for i, (label, key) in enumerate(fields):
            tk.Label(dialog, text=label, font=("Arial", 10)).grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)
            
            if key == "gender":
                entries[key] = ttk.Combobox(dialog, values=["Male", "Female", "Other"], font=("Arial", 10), state="readonly")
                entries[key].grid(row=i, column=1, padx=10, pady=10, sticky=tk.EW)
            elif key == "blood_group":
                entries[key] = ttk.Combobox(dialog, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], font=("Arial", 10), state="readonly")
                entries[key].grid(row=i, column=1, padx=10, pady=10, sticky=tk.EW)
            else:
                entries[key] = tk.Entry(dialog, font=("Arial", 10))
                entries[key].grid(row=i, column=1, padx=10, pady=10, sticky=tk.EW)
        
        dialog.grid_columnconfigure(1, weight=1)
        
        def save():
            data = {key: widget.get().strip() for key, widget in entries.items()}
            
            if not all([data['first_name'], data['last_name'], data['gender'], data['dob'], data['phone']]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            query = """INSERT INTO patients (first_name, last_name, gender, date_of_birth, phone, email, address, blood_group)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            
            if self.database.execute_query(query, (
                data['first_name'], data['last_name'], data['gender'], data['dob'],
                data['phone'], data['email'], data['address'], data['blood_group']
            )):
                messagebox.showinfo("Success", "Patient added successfully!")
                dialog.destroy()
                self.load_patients()
            else:
                messagebox.showerror("Error", "Failed to add patient")
        
        tk.Button(dialog, text="Save", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=save).grid(row=len(fields), column=0, columnspan=2, pady=20, padx=10, sticky=tk.EW)
    
    def update_patient_dialog(self):
        """Show dialog to update patient"""
        if not self.selected_patient:
            messagebox.showwarning("Warning", "Please select a patient to update")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Patient")
        dialog.geometry("400x500")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Get current patient data
        patient_id = self.selected_patient[0]
        query = "SELECT * FROM patients WHERE patient_id=?"
        patient = self.database.fetch_one(query, (patient_id,))
        
        fields = [
            ("First Name:", "first_name", patient[1]),
            ("Last Name:", "last_name", patient[2]),
            ("Gender:", "gender", patient[3]),
            ("Date of Birth (YYYY-MM-DD):", "dob", patient[4]),
            ("Phone:", "phone", patient[5]),
            ("Email:", "email", patient[6]),
            ("Address:", "address", patient[7]),
            ("Blood Group:", "blood_group", patient[8])
        ]
        
        entries = {}
        
        for i, (label, key, value) in enumerate(fields):
            tk.Label(dialog, text=label, font=("Arial", 10)).grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)
            
            if key == "gender":
                entries[key] = ttk.Combobox(dialog, values=["Male", "Female", "Other"], font=("Arial", 10), state="readonly")
                entries[key].set(value)
            elif key == "blood_group":
                entries[key] = ttk.Combobox(dialog, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], font=("Arial", 10), state="readonly")
                entries[key].set(value)
            else:
                entries[key] = tk.Entry(dialog, font=("Arial", 10))
                entries[key].insert(0, value or "")
            
            entries[key].grid(row=i, column=1, padx=10, pady=10, sticky=tk.EW)
        
        dialog.grid_columnconfigure(1, weight=1)
        
        def update():
            data = {key: widget.get().strip() for key, widget in entries.items()}
            
            query = """UPDATE patients SET first_name=?, last_name=?, gender=?, date_of_birth=?,
                       phone=?, email=?, address=?, blood_group=? WHERE patient_id=?"""
            
            if self.database.execute_query(query, (
                data['first_name'], data['last_name'], data['gender'], data['dob'],
                data['phone'], data['email'], data['address'], data['blood_group'], patient_id
            )):
                messagebox.showinfo("Success", "Patient updated successfully!")
                dialog.destroy()
                self.load_patients()
            else:
                messagebox.showerror("Error", "Failed to update patient")
        
        tk.Button(dialog, text="Update", bg="#3498db", fg="white", font=("Arial", 10, "bold"), command=update).grid(row=len(fields), column=0, columnspan=2, pady=20, padx=10, sticky=tk.EW)
    
    def delete_patient(self):
        """Delete selected patient"""
        if not self.selected_patient:
            messagebox.showwarning("Warning", "Please select a patient to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this patient?"):
            patient_id = self.selected_patient[0]
            query = "DELETE FROM patients WHERE patient_id=?"
            
            if self.database.execute_query(query, (patient_id,)):
                messagebox.showinfo("Success", "Patient deleted successfully!")
                self.selected_patient = None
                self.load_patients()
            else:
                messagebox.showerror("Error", "Failed to delete patient")
