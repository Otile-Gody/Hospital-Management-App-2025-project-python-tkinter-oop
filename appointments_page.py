import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class AppointmentsPage:
    """Appointment Management page"""
    
    def __init__(self, root, database, navigate_to):
        self.root = root
        self.database = database
        self.navigate_to = navigate_to
        self.frame = None
        self.tree = None
        self.selected_appointment = None
    
    def show(self):
        """Display the appointments page"""
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
            text="Appointment Management",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=10)
        
        # Control buttons frame
        btn_frame = tk.Frame(self.frame, bg="#ecf0f1")
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="Add Appointment",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.add_appointment_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Update Appointment",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.update_appointment_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Delete Appointment",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.delete_appointment
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Refresh",
            font=("Arial", 10, "bold"),
            bg="#95a5a6",
            fg="white",
            cursor="hand2",
            command=self.load_appointments
        ).pack(side=tk.LEFT, padx=5)
        
        # Table frame
        table_frame = tk.Frame(self.frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Create treeview
        columns = ("ID", "Patient Name", "Doctor Name", "Date", "Time", "Status", "Reason")
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
        
        # Load data        self.load_appointments()
    
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
    
    def load_appointments(self):
        """Load appointments from database"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch data with joins
        query = """
            SELECT a.appointment_id, 
                   p.first_name || ' ' || p.last_name as patient_name,
                   d.first_name || ' ' || d.last_name as doctor_name,
                   a.appointment_date, a.appointment_time, a.status, a.reason
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """
        appointments = self.database.fetch_all(query)
        
        # Insert data
        for appointment in appointments:
            self.tree.insert('', tk.END, values=appointment)
    
    def on_select(self, event):
        """Handle row selection"""
        selected = self.tree.selection()
        if selected:
            self.selected_appointment = self.tree.item(selected[0])['values']
    
    def get_patients_list(self):
        """Get list of patients for dropdown"""
        query = "SELECT patient_id, first_name || ' ' || last_name as name FROM patients"
        return self.database.fetch_all(query)
    
    def get_doctors_list(self):
        """Get list of doctors for dropdown"""
        query = "SELECT doctor_id, first_name || ' ' || last_name || ' (' || specialization || ')' as name FROM doctors"
        return self.database.fetch_all(query)
    
    def add_appointment_dialog(self):
        """Show dialog to add new appointment"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Appointment")
        dialog.geometry("400x450")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Get patients and doctors
        patients = self.get_patients_list()
        doctors = self.get_doctors_list()
        
        if not patients:
            messagebox.showerror("Error", "No patients found. Please add patients first.")
            dialog.destroy()
            return
        
        if not doctors:
            messagebox.showerror("Error", "No doctors found. Please add doctors first.")
            dialog.destroy()
            return
        
        # Patient selection
        tk.Label(dialog, text="Patient:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        patient_var = tk.StringVar()
        patient_combo = ttk.Combobox(dialog, textvariable=patient_var, font=("Arial", 10), state="readonly")
        patient_combo['values'] = [f"{p[0]} - {p[1]}" for p in patients]
        patient_combo.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Doctor selection
        tk.Label(dialog, text="Doctor:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        doctor_var = tk.StringVar()
        doctor_combo = ttk.Combobox(dialog, textvariable=doctor_var, font=("Arial", 10), state="readonly")
        doctor_combo['values'] = [f"{d[0]} - {d[1]}" for d in doctors]
        doctor_combo.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Date
        tk.Label(dialog, text="Date (YYYY-MM-DD):", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        date_entry = tk.Entry(dialog, font=("Arial", 10))
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Time
        tk.Label(dialog, text="Time (HH:MM):", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        time_entry = tk.Entry(dialog, font=("Arial", 10))
        time_entry.insert(0, "09:00")
        time_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Status
        tk.Label(dialog, text="Status:", font=("Arial", 10)).grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(dialog, textvariable=status_var, values=["Scheduled", "Completed", "Cancelled"], font=("Arial", 10), state="readonly")
        status_combo.set("Scheduled")
        status_combo.grid(row=4, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Reason
        tk.Label(dialog, text="Reason:", font=("Arial", 10)).grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
        reason_entry = tk.Entry(dialog, font=("Arial", 10))
        reason_entry.grid(row=5, column=1, padx=10, pady=10, sticky=tk.EW)
        
        dialog.grid_columnconfigure(1, weight=1)
        
        def save():
            patient_id = patient_var.get().split(' - ')[0] if patient_var.get() else None
            doctor_id = doctor_var.get().split(' - ')[0] if doctor_var.get() else None
            date = date_entry.get().strip()
            time = time_entry.get().strip()
            status = status_var.get()
            reason = reason_entry.get().strip()
            
            if not all([patient_id, doctor_id, date, time]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            query = """INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, reason)
                       VALUES (?, ?, ?, ?, ?, ?)"""
            
            if self.database.execute_query(query, (patient_id, doctor_id, date, time, status, reason)):
                messagebox.showinfo("Success", "Appointment added successfully!")
                dialog.destroy()
                self.load_appointments()
            else:
                messagebox.showerror("Error", "Failed to add appointment")
        
        tk.Button(dialog, text="Save", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=save).grid(row=6, column=0, columnspan=2, pady=20, padx=10, sticky=tk.EW)
    
    def update_appointment_dialog(self):
        """Show dialog to update appointment"""
        if not self.selected_appointment:
            messagebox.showwarning("Warning", "Please select an appointment to update")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Appointment")
        dialog.geometry("400x400")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Get current appointment data
        appointment_id = self.selected_appointment[0]
        query = "SELECT * FROM appointments WHERE appointment_id=?"
        appointment = self.database.fetch_one(query, (appointment_id,))
        
        # Date
        tk.Label(dialog, text="Date (YYYY-MM-DD):", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        date_entry = tk.Entry(dialog, font=("Arial", 10))
        date_entry.insert(0, appointment[3])
        date_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Time
        tk.Label(dialog, text="Time (HH:MM):", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        time_entry = tk.Entry(dialog, font=("Arial", 10))
        time_entry.insert(0, appointment[4])
        time_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Status
        tk.Label(dialog, text="Status:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(dialog, textvariable=status_var, values=["Scheduled", "Completed", "Cancelled"], font=("Arial", 10), state="readonly")
        status_combo.set(appointment[5])
        status_combo.grid(row=2, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Reason
        tk.Label(dialog, text="Reason:", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        reason_entry = tk.Entry(dialog, font=("Arial", 10))
        reason_entry.insert(0, appointment[6] or "")
        reason_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.EW)
        
        dialog.grid_columnconfigure(1, weight=1)
        
        def update():
            date = date_entry.get().strip()
            time = time_entry.get().strip()
            status = status_var.get()
            reason = reason_entry.get().strip()
            
            query = """UPDATE appointments SET appointment_date=?, appointment_time=?, status=?, reason=?
                       WHERE appointment_id=?"""
            
            if self.database.execute_query(query, (date, time, status, reason, appointment_id)):
                messagebox.showinfo("Success", "Appointment updated successfully!")
                dialog.destroy()
                self.load_appointments()
            else:
                messagebox.showerror("Error", "Failed to update appointment")
        
        tk.Button(dialog, text="Update", bg="#3498db", fg="white", font=("Arial", 10, "bold"), command=update).grid(row=4, column=0, columnspan=2, pady=20, padx=10, sticky=tk.EW)
    
    def delete_appointment(self):
        """Delete selected appointment"""
        if not self.selected_appointment:
            messagebox.showwarning("Warning", "Please select an appointment to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this appointment?"):
            appointment_id = self.selected_appointment[0]
            query = "DELETE FROM appointments WHERE appointment_id=?"
            
            if self.database.execute_query(query, (appointment_id,)):
                messagebox.showinfo("Success", "Appointment deleted successfully!")
                self.selected_appointment = None
                self.load_appointments()
            else:
                messagebox.showerror("Error", "Failed to delete appointment")
