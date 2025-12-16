import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os

class BillingPage:
    """Billing and Invoice Management page"""
    
    def __init__(self, root, database, navigate_to):
        self.root = root
        self.database = database
        self.navigate_to = navigate_to
        self.frame = None
        self.tree = None
        self.selected_bill = None
    
    def show(self):
        """Display the billing page"""
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
            text="Billing & Invoice Management",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=10)
        
        # Control buttons frame
        btn_frame = tk.Frame(self.frame, bg="#ecf0f1")
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="Create Invoice",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.create_invoice_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="View Invoice",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.view_invoice_details
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Download Invoice",
            font=("Arial", 10, "bold"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            command=self.download_invoice
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Mark as Paid",
            font=("Arial", 10, "bold"),
            bg="#f39c12",
            fg="white",
            cursor="hand2",
            command=self.mark_as_paid
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Delete Invoice",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.delete_invoice
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Refresh",
            font=("Arial", 10, "bold"),
            bg="#95a5a6",
            fg="white",
            cursor="hand2",
            command=self.load_invoices
        ).pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = tk.Frame(self.frame, bg="#ecf0f1")
        search_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(search_frame, text="Search by Patient:", font=("Arial", 10), bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_invoices())
        
        tk.Label(search_frame, text="Filter by Status:", font=("Arial", 10), bg="#ecf0f1").pack(side=tk.LEFT, padx=20)
        self.status_filter = ttk.Combobox(search_frame, font=("Arial", 10), state="readonly", width=15)
        self.status_filter['values'] = ["All", "Pending", "Paid", "Overdue"]
        self.status_filter.set("All")
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.search_invoices())
        self.status_filter.pack(side=tk.LEFT, padx=5)
        
        # Table frame
        table_frame = tk.Frame(self.frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Create treeview
        columns = ("ID", "Patient Name", "Invoice Date", "Amount", "Status", "Payment Date")
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
        column_widths = {"ID": 70, "Patient Name": 200, "Invoice Date": 120, "Amount": 120, "Status": 100, "Payment Date": 120}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col], anchor=tk.CENTER)
        
        # Pack scrollbars and treeview
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Load data
        self.load_invoices()
    
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
    
    def load_invoices(self):
        """Load invoices from database"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch data with joins
        query = """
            SELECT b.invoice_id,
                   p.first_name || ' ' || p.last_name as patient_name,
                   b.invoice_date, b.total_amount, b.status, b.payment_date
            FROM billing b
            JOIN patients p ON b.patient_id = p.patient_id
            ORDER BY b.invoice_date DESC
        """
        invoices = self.database.fetch_all(query)
          # Insert data with status-based colors
        for invoice in invoices:
            invoice_list = list(invoice)
            invoice_list[3] = f"UGX {invoice_list[3]:,.0f}"
            invoice_list[5] = invoice_list[5] or "N/A"
            
            item = self.tree.insert('', tk.END, values=invoice_list)
            
            # Color coding based on status
            if invoice[4] == "Paid":
                self.tree.item(item, tags=('paid',))
            elif invoice[4] == "Overdue":
                self.tree.item(item, tags=('overdue',))
            else:
                self.tree.item(item, tags=('pending',))
        
        # Configure tags
        self.tree.tag_configure('paid', background='#d4edda')
        self.tree.tag_configure('overdue', background='#f8d7da')
        self.tree.tag_configure('pending', background='#fff3cd')
    
    def search_invoices(self):
        """Search invoices by patient name and filter by status"""
        search_term = self.search_entry.get().strip().lower()
        status_filter = self.status_filter.get()
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch and filter data
        query = """
            SELECT b.invoice_id,
                   p.first_name || ' ' || p.last_name as patient_name,
                   b.invoice_date, b.total_amount, b.status, b.payment_date
            FROM billing b
            JOIN patients p ON b.patient_id = p.patient_id
            ORDER BY b.invoice_date DESC        """
        invoices = self.database.fetch_all(query)
        
        for invoice in invoices:
            # Apply filters
            if search_term and search_term not in invoice[1].lower():
                continue
            if status_filter != "All" and invoice[4] != status_filter:
                continue
            
            invoice_list = list(invoice)
            invoice_list[3] = f"UGX {invoice_list[3]:,.0f}"
            invoice_list[5] = invoice_list[5] or "N/A"
            
            item = self.tree.insert('', tk.END, values=invoice_list)
            
            # Color coding based on status
            if invoice[4] == "Paid":
                self.tree.item(item, tags=('paid',))
            elif invoice[4] == "Overdue":
                self.tree.item(item, tags=('overdue',))
            else:
                self.tree.item(item, tags=('pending',))
        
        # Configure tags
        self.tree.tag_configure('paid', background='#d4edda')
        self.tree.tag_configure('overdue', background='#f8d7da')
        self.tree.tag_configure('pending', background='#fff3cd')
    
    def on_select(self, event):
        """Handle row selection"""
        selected = self.tree.selection()
        if selected:
            self.selected_bill = self.tree.item(selected[0])['values']
    
    def get_patients_list(self):
        """Get list of patients for dropdown"""
        query = "SELECT patient_id, first_name || ' ' || last_name as name FROM patients"
        return self.database.fetch_all(query)
    
    def create_invoice_dialog(self):
        """Show dialog to create new invoice"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Invoice")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Get patients
        patients = self.get_patients_list()
        
        if not patients:
            messagebox.showerror("Error", "No patients found. Please add patients first.")
            dialog.destroy()
            return
        
        # Patient selection
        tk.Label(dialog, text="Patient:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        patient_var = tk.StringVar()
        patient_combo = ttk.Combobox(dialog, textvariable=patient_var, font=("Arial", 10), state="readonly", width=40)
        patient_combo['values'] = [f"{p[0]} - {p[1]}" for p in patients]
        patient_combo.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Invoice Date
        tk.Label(dialog, text="Invoice Date (YYYY-MM-DD):", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        date_entry = tk.Entry(dialog, font=("Arial", 10))
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Description
        tk.Label(dialog, text="Description:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        desc_entry = tk.Entry(dialog, font=("Arial", 10))
        desc_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Services/Items Frame
        tk.Label(dialog, text="Services:", font=("Arial", 10, "bold")).grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)
          # Consultation Fee
        tk.Label(dialog, text="Consultation Fee:", font=("Arial", 10)).grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        consultation_entry = tk.Entry(dialog, font=("Arial", 10))
        consultation_entry.insert(0, "0")
        consultation_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.EW)
        
        # Lab Tests
        tk.Label(dialog, text="Lab Tests:", font=("Arial", 10)).grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        lab_entry = tk.Entry(dialog, font=("Arial", 10))
        lab_entry.insert(0, "0")
        lab_entry.grid(row=5, column=1, padx=10, pady=5, sticky=tk.EW)
        
        # Medicines
        tk.Label(dialog, text="Medicines:", font=("Arial", 10)).grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
        medicine_entry = tk.Entry(dialog, font=("Arial", 10))
        medicine_entry.insert(0, "0")
        medicine_entry.grid(row=6, column=1, padx=10, pady=5, sticky=tk.EW)
        
        # Room Charges
        tk.Label(dialog, text="Room Charges:", font=("Arial", 10)).grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
        room_entry = tk.Entry(dialog, font=("Arial", 10))
        room_entry.insert(0, "0")
        room_entry.grid(row=7, column=1, padx=10, pady=5, sticky=tk.EW)
          # Other Charges
        tk.Label(dialog, text="Other Charges:", font=("Arial", 10)).grid(row=8, column=0, padx=10, pady=5, sticky=tk.W)
        other_entry = tk.Entry(dialog, font=("Arial", 10))
        other_entry.insert(0, "0")
        other_entry.grid(row=8, column=1, padx=10, pady=5, sticky=tk.EW)
        
        # Total Amount (readonly)
        tk.Label(dialog, text="Total Amount:", font=("Arial", 10, "bold")).grid(row=9, column=0, padx=10, pady=10, sticky=tk.W)
        total_var = tk.StringVar(value="UGX 0")
        total_label = tk.Label(dialog, textvariable=total_var, font=("Arial", 12, "bold"), fg="#27ae60")
        total_label.grid(row=9, column=1, padx=10, pady=10, sticky=tk.W)
        
        dialog.grid_columnconfigure(1, weight=1)
        
        def calculate_total(*args):
            try:
                consultation = float(consultation_entry.get() or 0)
                lab = float(lab_entry.get() or 0)
                medicine = float(medicine_entry.get() or 0)
                room = float(room_entry.get() or 0)
                other = float(other_entry.get() or 0)
                total = consultation + lab + medicine + room + other
                total_var.set(f"UGX {total:,.0f}")
            except ValueError:
                total_var.set("UGX 0")
          # Bind calculation to entries
        for entry in [consultation_entry, lab_entry, medicine_entry, room_entry, other_entry]:
            entry.bind('<KeyRelease>', calculate_total)
        
        def save():
            patient_id = patient_var.get().split(' - ')[0] if patient_var.get() else None
            invoice_date = date_entry.get().strip()
            description = desc_entry.get().strip()
            
            try:
                consultation = float(consultation_entry.get() or 0)
                lab = float(lab_entry.get() or 0)
                medicine = float(medicine_entry.get() or 0)
                room = float(room_entry.get() or 0)
                other = float(other_entry.get() or 0)
                total_amount = consultation + lab + medicine + room + other
            except ValueError:
                messagebox.showerror("Error", "Please enter valid amounts")
                return
            
            if not all([patient_id, invoice_date]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            if total_amount <= 0:
                messagebox.showerror("Error", "Total amount must be greater than 0")
                return
            
            # Create services JSON-like string
            services = f"Consultation: UGX {consultation:,.0f}, Lab Tests: UGX {lab:,.0f}, Medicines: UGX {medicine:,.0f}, Room: UGX {room:,.0f}, Other: UGX {other:,.0f}"
            
            query = """INSERT INTO billing (patient_id, invoice_date, description, services, total_amount, status)
                       VALUES (?, ?, ?, ?, ?, ?)"""
            
            if self.database.execute_query(query, (patient_id, invoice_date, description, services, total_amount, "Pending")):
                messagebox.showinfo("Success", f"Invoice created successfully!\nTotal Amount: UGX {total_amount:,.0f}")
                dialog.destroy()
                self.load_invoices()
            else:
                messagebox.showerror("Error", "Failed to create invoice")
        
        tk.Button(dialog, text="Create Invoice", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=save).grid(row=10, column=0, columnspan=2, pady=20, padx=10, sticky=tk.EW)
    
    def view_invoice_details(self):
        """View detailed information of selected invoice"""
        if not self.selected_bill:
            messagebox.showwarning("Warning", "Please select an invoice to view")
            return
        
        invoice_id = self.selected_bill[0]
        query = """
            SELECT b.*, 
                   p.first_name || ' ' || p.last_name as patient_name,
                   p.phone as patient_phone,
                   p.email as patient_email,
                   p.address as patient_address
            FROM billing b
            JOIN patients p ON b.patient_id = p.patient_id
            WHERE b.invoice_id = ?
        """
        invoice = self.database.fetch_one(query, (invoice_id,))
        
        if not invoice:
            messagebox.showerror("Error", "Invoice not found")
            return
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title("Invoice Details")
        details_window.geometry("600x600")
        details_window.resizable(False, False)
        details_window.grab_set()
        
        # Header
        header_frame = tk.Frame(details_window, bg="#2c3e50")
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="INVOICE DETAILS", font=("Arial", 18, "bold"), bg="#2c3e50", fg="white").pack(pady=15)
        
        # Content frame
        content_frame = tk.Frame(details_window, bg="white", padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display information
        info = [
            ("Invoice ID:", invoice[0]),
            ("Patient Name:", invoice[7]),
            ("Phone:", invoice[8] or "N/A"),
            ("Email:", invoice[9] or "N/A"),
            ("Address:", invoice[10] or "N/A"),
            ("", ""),
            ("Invoice Date:", invoice[2]),
            ("Description:", invoice[3] or "General Treatment"),            ("Services:", invoice[4]),
            ("", ""),
            ("Total Amount:", f"UGX {invoice[5]:,.0f}"),
            ("Status:", invoice[6]),
            ("Payment Date:", invoice[7] if len(invoice) > 7 and invoice[7] else "Not Paid")
        ]
        
        for i, (label, value) in enumerate(info):
            if label:
                tk.Label(content_frame, text=label, font=("Arial", 11, "bold"), bg="white", anchor=tk.W).grid(row=i, column=0, sticky=tk.W, pady=8, padx=10)
                tk.Label(content_frame, text=str(value), font=("Arial", 10), bg="white", anchor=tk.W, wraplength=350).grid(row=i, column=1, sticky=tk.W, pady=8)
        
        # Close button
        tk.Button(details_window, text="Close", bg="#95a5a6", fg="white", font=("Arial", 10, "bold"), command=details_window.destroy).pack(pady=10)
    
    def download_invoice(self):
        """Download/Export invoice as text file"""
        if not self.selected_bill:
            messagebox.showwarning("Warning", "Please select an invoice to download")
            return
        
        invoice_id = self.selected_bill[0]
        query = """
            SELECT b.*, 
                   p.first_name || ' ' || p.last_name as patient_name,
                   p.phone as patient_phone,
                   p.email as patient_email,
                   p.address as patient_address
            FROM billing b
            JOIN patients p ON b.patient_id = p.patient_id
            WHERE b.invoice_id = ?
        """
        invoice = self.database.fetch_one(query, (invoice_id,))
        
        if not invoice:
            messagebox.showerror("Error", "Invoice not found")
            return
          # Ask user where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"Invoice_{invoice_id}_{datetime.now().strftime('%Y%m%d')}.txt"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(" " * 25 + "INVOICE\n")
                f.write(" " * 15 + "HOSPITAL MANAGEMENT SYSTEM\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Invoice Number: #{invoice[0]}\n")
                f.write(f"Invoice Date: {invoice[2]}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 80 + "\n\n")
                
                f.write("BILL TO:\n")
                f.write(f"  Name: {invoice[7]}\n")
                f.write(f"  Phone: {invoice[8] or 'N/A'}\n")
                f.write(f"  Email: {invoice[9] or 'N/A'}\n")
                f.write(f"  Address: {invoice[10] or 'N/A'}\n\n")
                
                f.write("-" * 80 + "\n")
                f.write(f"Description: {invoice[3] or 'General Treatment'}\n\n")
                
                f.write("SERVICES:\n")
                f.write(f"{invoice[4]}\n\n")
                
                f.write("-" * 80 + "\n")
                f.write(f"TOTAL AMOUNT: UGX {invoice[5]:,.0f}\n")
                f.write(f"Status: {invoice[6]}\n")
                
                if invoice[6] == "Paid":
                    payment_date = invoice[7] if len(invoice) > 7 else "N/A"
                    f.write(f"Payment Date: {payment_date}\n")
                
                f.write("=" * 80 + "\n")
                f.write("\nThank you for choosing our hospital!\n")
                f.write("=" * 80 + "\n")
            
            messagebox.showinfo("Success", f"Invoice downloaded successfully!\n\nSaved to: {file_path}")
            
            # Ask if user wants to open the file
            if messagebox.askyesno("Open File", "Would you like to open the downloaded invoice?"):
                os.startfile(file_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download invoice:\n{str(e)}")
    
    def mark_as_paid(self):
        """Mark selected invoice as paid"""
        if not self.selected_bill:
            messagebox.showwarning("Warning", "Please select an invoice to mark as paid")
            return
        
        invoice_id = self.selected_bill[0]
        current_status = self.selected_bill[4]
        
        if current_status == "Paid":
            messagebox.showinfo("Info", "This invoice is already marked as paid")
            return
        
        if messagebox.askyesno("Confirm", "Mark this invoice as paid?"):
            payment_date = datetime.now().strftime("%Y-%m-%d")
            query = "UPDATE billing SET status=?, payment_date=? WHERE invoice_id=?"
            
            if self.database.execute_query(query, ("Paid", payment_date, invoice_id)):
                messagebox.showinfo("Success", "Invoice marked as paid!")
                self.selected_bill = None
                self.load_invoices()
            else:
                messagebox.showerror("Error", "Failed to update invoice status")
    
    def delete_invoice(self):
        """Delete selected invoice"""
        if not self.selected_bill:
            messagebox.showwarning("Warning", "Please select an invoice to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this invoice?\nThis action cannot be undone."):
            invoice_id = self.selected_bill[0]
            query = "DELETE FROM billing WHERE invoice_id=?"
            
            if self.database.execute_query(query, (invoice_id,)):
                messagebox.showinfo("Success", "Invoice deleted successfully!")
                self.selected_bill = None
                self.load_invoices()
            else:
                messagebox.showerror("Error", "Failed to delete invoice")
