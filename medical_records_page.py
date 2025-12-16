import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from datetime import datetime
import os

class MedicalRecordsPage:
    """Medical Records Management page"""
    
    def __init__(self, root, database, navigate_to):
        self.root = root
        self.database = database
        self.navigate_to = navigate_to
        self.frame = None
        self.tree = None
        self.selected_record = None
    
    def show(self):
        """Display the medical records page"""
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
            text="Medical Records Management",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=10)
        
        # Control buttons frame
        btn_frame = tk.Frame(self.frame, bg="#ecf0f1")
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="Add Record",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.add_record_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="View Details",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.view_record_details
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Download PDF",
            font=("Arial", 10, "bold"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            command=self.download_record_pdf
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Delete Record",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.delete_record
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Refresh",
            font=("Arial", 10, "bold"),
            bg="#95a5a6",
            fg="white",
            cursor="hand2",
            command=self.load_records
        ).pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = tk.Frame(self.frame, bg="#ecf0f1")
        search_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(search_frame, text="Search by Patient:", font=("Arial", 10), bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_records())
        
        # Table frame
        table_frame = tk.Frame(self.frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Create treeview
        columns = ("ID", "Patient Name", "Doctor Name", "Visit Date", "Diagnosis")
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
            self.tree.column(col, width=150, anchor=tk.CENTER)
        
        # Pack scrollbars and treeview
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Load data
        self.load_records()
    
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
            ("Billing", "billing"),
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
    
    def load_records(self):
        """Load medical records from database"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch data with joins
        query = """
            SELECT m.record_id,
                   p.first_name || ' ' || p.last_name as patient_name,
                   d.first_name || ' ' || d.last_name as doctor_name,
                   m.visit_date, m.diagnosis
            FROM medical_records m
            JOIN patients p ON m.patient_id = p.patient_id
            JOIN doctors d ON m.doctor_id = d.doctor_id
            ORDER BY m.visit_date DESC
        """
        records = self.database.fetch_all(query)
        
        # Insert data
        for record in records:
            self.tree.insert('', tk.END, values=record)
    
    def search_records(self):
        """Search records by patient name"""
        search_term = self.search_entry.get().strip().lower()
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch and filter data
        query = """
            SELECT m.record_id,
                   p.first_name || ' ' || p.last_name as patient_name,
                   d.first_name || ' ' || d.last_name as doctor_name,
                   m.visit_date, m.diagnosis
            FROM medical_records m
            JOIN patients p ON m.patient_id = p.patient_id
            JOIN doctors d ON m.doctor_id = d.doctor_id
            ORDER BY m.visit_date DESC
        """
        records = self.database.fetch_all(query)
        
        for record in records:
            if search_term in record[1].lower():
                self.tree.insert('', tk.END, values=record)
    
    def on_select(self, event):
        """Handle row selection"""
        selected = self.tree.selection()
        if selected:
            self.selected_record = self.tree.item(selected[0])['values']
    
    def get_patients_list(self):
        """Get list of patients for dropdown"""
        query = "SELECT patient_id, first_name || ' ' || last_name as name FROM patients"
        return self.database.fetch_all(query)
    
    def get_doctors_list(self):
        """Get list of doctors for dropdown"""
        query = "SELECT doctor_id, first_name || ' ' || last_name || ' (' || specialization || ')' as name FROM doctors"
        return self.database.fetch_all(query)
    
    def add_record_dialog(self):
        """Show dialog to add new medical record"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Medical Record")
        dialog.geometry("500x600")
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
        patient_combo = ttk.Combobox(dialog, textvariable=patient_var, font=("Arial", 10), state="readonly", width=40)
        patient_combo['values'] = [f"{p[0]} - {p[1]}" for p in patients]
        patient_combo.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Doctor selection
        tk.Label(dialog, text="Doctor:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        doctor_var = tk.StringVar()
        doctor_combo = ttk.Combobox(dialog, textvariable=doctor_var, font=("Arial", 10), state="readonly", width=40)
        doctor_combo['values'] = [f"{d[0]} - {d[1]}" for d in doctors]
        doctor_combo.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Visit Date
        tk.Label(dialog, text="Visit Date (YYYY-MM-DD):", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        date_entry = tk.Entry(dialog, font=("Arial", 10))
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Diagnosis
        tk.Label(dialog, text="Diagnosis:", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=10, sticky=tk.NW)
        diagnosis_text = scrolledtext.ScrolledText(dialog, font=("Arial", 10), height=5, width=40)
        diagnosis_text.grid(row=3, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Prescription
        tk.Label(dialog, text="Prescription:", font=("Arial", 10)).grid(row=4, column=0, padx=10, pady=10, sticky=tk.NW)
        prescription_text = scrolledtext.ScrolledText(dialog, font=("Arial", 10), height=5, width=40)
        prescription_text.grid(row=4, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Notes
        tk.Label(dialog, text="Notes:", font=("Arial", 10)).grid(row=5, column=0, padx=10, pady=10, sticky=tk.NW)
        notes_text = scrolledtext.ScrolledText(dialog, font=("Arial", 10), height=5, width=40)
        notes_text.grid(row=5, column=1, padx=10, pady=10, sticky=tk.EW)
        
        dialog.grid_columnconfigure(1, weight=1)
        
        def save():
            patient_id = patient_var.get().split(' - ')[0] if patient_var.get() else None
            doctor_id = doctor_var.get().split(' - ')[0] if doctor_var.get() else None
            visit_date = date_entry.get().strip()
            diagnosis = diagnosis_text.get("1.0", tk.END).strip()
            prescription = prescription_text.get("1.0", tk.END).strip()
            notes = notes_text.get("1.0", tk.END).strip()
            
            if not all([patient_id, doctor_id, visit_date, diagnosis]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            query = """INSERT INTO medical_records (patient_id, doctor_id, visit_date, diagnosis, prescription, notes)
                       VALUES (?, ?, ?, ?, ?, ?)"""
            
            if self.database.execute_query(query, (patient_id, doctor_id, visit_date, diagnosis, prescription, notes)):
                messagebox.showinfo("Success", "Medical record added successfully!")
                dialog.destroy()
                self.load_records()
            else:
                messagebox.showerror("Error", "Failed to add medical record")
        
        tk.Button(dialog, text="Save", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=save).grid(row=6, column=0, columnspan=2, pady=20, padx=10, sticky=tk.EW)
    
    def view_record_details(self):
        """View detailed information of selected record"""
        if not self.selected_record:
            messagebox.showwarning("Warning", "Please select a record to view")
            return
        
        record_id = self.selected_record[0]
        query = """
            SELECT m.*, 
                   p.first_name || ' ' || p.last_name as patient_name,
                   d.first_name || ' ' || d.last_name as doctor_name
            FROM medical_records m
            JOIN patients p ON m.patient_id = p.patient_id
            JOIN doctors d ON m.doctor_id = d.doctor_id
            WHERE m.record_id = ?
        """
        record = self.database.fetch_one(query, (record_id,))
        
        if not record:
            messagebox.showerror("Error", "Record not found")
            return
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title("Medical Record Details")
        details_window.geometry("600x700")
        details_window.resizable(False, False)
        details_window.grab_set()
        
        # Header
        header_frame = tk.Frame(details_window, bg="#2c3e50")
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="Medical Record Details", font=("Arial", 18, "bold"), bg="#2c3e50", fg="white").pack(pady=15)
        
        # Content frame
        content_frame = tk.Frame(details_window, bg="white", padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display information
        info = [
            ("Record ID:", record[0]),
            ("Patient Name:", record[7]),
            ("Doctor Name:", record[8]),
            ("Visit Date:", record[3]),
            ("Diagnosis:", record[4]),
            ("Prescription:", record[5] or "N/A"),
            ("Notes:", record[6] or "N/A")
        ]
        
        for i, (label, value) in enumerate(info):
            tk.Label(content_frame, text=label, font=("Arial", 11, "bold"), bg="white", anchor=tk.W).grid(row=i, column=0, sticky=tk.W, pady=10)
            
            if label in ["Diagnosis:", "Prescription:", "Notes:"]:
                text_widget = scrolledtext.ScrolledText(content_frame, font=("Arial", 10), height=5, width=50, wrap=tk.WORD)
                text_widget.insert("1.0", str(value))
                text_widget.config(state=tk.DISABLED)
                text_widget.grid(row=i, column=1, sticky=tk.W, pady=10)
            else:
                tk.Label(content_frame, text=str(value), font=("Arial", 10), bg="white", anchor=tk.W).grid(row=i, column=1, sticky=tk.W, pady=10)
          # Close button
        tk.Button(details_window, text="Close", bg="#95a5a6", fg="white", font=("Arial", 10, "bold"), command=details_window.destroy).pack(pady=10)
    
    def download_record_pdf(self):
        """Download/Export medical record as text file (PDF-like format)"""
        if not self.selected_record:
            messagebox.showwarning("Warning", "Please select a record to download")
            return
        
        record_id = self.selected_record[0]
        query = """
            SELECT m.*, 
                   p.first_name || ' ' || p.last_name as patient_name,
                   p.phone as patient_phone,
                   p.date_of_birth as patient_dob,
                   p.blood_group,
                   d.first_name || ' ' || d.last_name as doctor_name,
                   d.specialization,
                   d.qualification
            FROM medical_records m
            JOIN patients p ON m.patient_id = p.patient_id
            JOIN doctors d ON m.doctor_id = d.doctor_id
            WHERE m.record_id = ?
        """
        record = self.database.fetch_one(query, (record_id,))
        
        if not record:
            messagebox.showerror("Error", "Record not found")
            return
        
        # Ask user where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"Medical_Record_{record_id}_{datetime.now().strftime('%Y%m%d')}.txt"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(" " * 20 + "MEDICAL RECORD REPORT\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Record ID: {record[0]}\n")
                f.write(f"Generated Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 80 + "\n\n")
                
                f.write("PATIENT INFORMATION:\n")
                f.write(f"  Name: {record[7]}\n")
                f.write(f"  Phone: {record[8]}\n")
                f.write(f"  Date of Birth: {record[9]}\n")
                f.write(f"  Blood Group: {record[10] or 'N/A'}\n\n")
                
                f.write("DOCTOR INFORMATION:\n")
                f.write(f"  Name: Dr. {record[11]}\n")
                f.write(f"  Specialization: {record[12]}\n")
                f.write(f"  Qualification: {record[13] or 'N/A'}\n\n")
                
                f.write("-" * 80 + "\n\n")
                f.write(f"Visit Date: {record[3]}\n\n")
                
                f.write("DIAGNOSIS:\n")
                f.write(f"{record[4]}\n\n")
                
                f.write("PRESCRIPTION:\n")
                f.write(f"{record[5] or 'No prescription provided'}\n\n")
                
                f.write("ADDITIONAL NOTES:\n")
                f.write(f"{record[6] or 'No additional notes'}\n\n")
                
                f.write("=" * 80 + "\n")
                f.write("This is an official medical record from Hospital Management System\n")
                f.write("=" * 80 + "\n")
            
            messagebox.showinfo("Success", f"Medical record downloaded successfully!\n\nSaved to: {file_path}")
            
            # Ask if user wants to open the file
            if messagebox.askyesno("Open File", "Would you like to open the downloaded file?"):
                os.startfile(file_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download medical record:\n{str(e)}")
    
    def delete_record(self):
        """Delete selected medical record"""
        if not self.selected_record:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this medical record?"):
            record_id = self.selected_record[0]
            query = "DELETE FROM medical_records WHERE record_id=?"
            
            if self.database.execute_query(query, (record_id,)):
                messagebox.showinfo("Success", "Medical record deleted successfully!")
                self.selected_record = None
                self.load_records()
            else:
                messagebox.showerror("Error", "Failed to delete medical record")
    
    def download_record_pdf(self):
        """Download/Export medical record as text file (PDF-like format)"""
        if not self.selected_record:
            messagebox.showwarning("Warning", "Please select a record to download")
            return
        
        record_id = self.selected_record[0]
        query = """
            SELECT m.*, 
                   p.first_name || ' ' || p.last_name as patient_name,
                   p.phone as patient_phone,
                   p.date_of_birth as patient_dob,
                   p.blood_group,
                   d.first_name || ' ' || d.last_name as doctor_name,
                   d.specialization,
                   d.qualification
            FROM medical_records m
            JOIN patients p ON m.patient_id = p.patient_id
            JOIN doctors d ON m.doctor_id = d.doctor_id
            WHERE m.record_id = ?
        """
        record = self.database.fetch_one(query, (record_id,))
        
        if not record:
            messagebox.showerror("Error", "Record not found")
            return
        
        # Ask user where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"Medical_Record_{record_id}_{datetime.now().strftime('%Y%m%d')}.txt"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(" " * 20 + "MEDICAL RECORD REPORT\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Record ID: {record[0]}\n")
                f.write(f"Generated Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 80 + "\n\n")
                
                f.write("PATIENT INFORMATION:\n")
                f.write(f"  Name: {record[7]}\n")
                f.write(f"  Phone: {record[8]}\n")
                f.write(f"  Date of Birth: {record[9]}\n")
                f.write(f"  Blood Group: {record[10] or 'N/A'}\n\n")
                
                f.write("DOCTOR INFORMATION:\n")
                f.write(f"  Name: Dr. {record[11]}\n")
                f.write(f"  Specialization: {record[12]}\n")
                f.write(f"  Qualification: {record[13] or 'N/A'}\n\n")
                
                f.write("-" * 80 + "\n\n")
                f.write(f"Visit Date: {record[3]}\n\n")
                
                f.write("DIAGNOSIS:\n")
                f.write(f"{record[4]}\n\n")
                
                f.write("PRESCRIPTION:\n")
                f.write(f"{record[5] or 'No prescription provided'}\n\n")
                
                f.write("ADDITIONAL NOTES:\n")
                f.write(f"{record[6] or 'No additional notes'}\n\n")
                
                f.write("=" * 80 + "\n")
                f.write("This is an official medical record from Hospital Management System\n")
                f.write("=" * 80 + "\n")
            
            messagebox.showinfo("Success", f"Medical record downloaded successfully!\n\nSaved to: {file_path}")
            
            # Ask if user wants to open the file
            if messagebox.askyesno("Open File", "Would you like to open the downloaded file?"):
                os.startfile(file_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download medical record:\n{str(e)}")
