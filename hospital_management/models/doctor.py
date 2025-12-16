"""
Doctor model for storing doctor information
"""


class Doctor:
    """Doctor entity class"""
    
    def __init__(self, doctor_id, first_name, last_name, specialization, 
                 license_number, contact_number, email):
        self.doctor_id = doctor_id
        self.first_name = first_name
        self.last_name = last_name
        self.specialization = specialization
        self.license_number = license_number
        self.contact_number = contact_number
        self.email = email
        self.appointments = []
    
    def get_full_name(self):
        """Return the full name of the doctor"""
        return f"Dr. {self.first_name} {self.last_name}"
    
    def add_appointment(self, appointment):
        """Add an appointment to the doctor's schedule"""
        self.appointments.append(appointment)
    
    def get_appointments_for_date(self, date):
        """Get all appointments for a specific date"""
        return [apt for apt in self.appointments if apt.date == date]
    
    def __str__(self):
        return f"Doctor({self.doctor_id}: {self.get_full_name()}, {self.specialization})"
    
    def __repr__(self):
        return self.__str__()
