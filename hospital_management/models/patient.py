"""
Patient model for storing patient information
"""
from datetime import datetime


class Patient:
    """Patient entity class"""
    
    def __init__(self, patient_id, first_name, last_name, date_of_birth, 
                 gender, contact_number, address, email=None):
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.contact_number = contact_number
        self.address = address
        self.email = email
        self.registration_date = datetime.now()
        self.medical_history = []
    
    def get_full_name(self):
        """Return the full name of the patient"""
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        """Calculate and return the patient's age"""
        today = datetime.now()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or \
           (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
        return age
    
    def add_medical_record(self, record):
        """Add a medical record to the patient's history"""
        self.medical_history.append(record)
    
    def __str__(self):
        return f"Patient({self.patient_id}: {self.get_full_name()})"
    
    def __repr__(self):
        return self.__str__()
