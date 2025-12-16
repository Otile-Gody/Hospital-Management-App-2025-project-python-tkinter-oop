"""
Appointment model for managing patient appointments
"""
from datetime import datetime


class Appointment:
    """Appointment entity class"""
    
    def __init__(self, appointment_id, patient, doctor, date, time, reason):
        self.appointment_id = appointment_id
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time
        self.reason = reason
        self.status = "Scheduled"  # Scheduled, Completed, Cancelled
        self.notes = ""
        self.created_at = datetime.now()
    
    def complete_appointment(self, notes=""):
        """Mark appointment as completed"""
        self.status = "Completed"
        self.notes = notes
    
    def cancel_appointment(self, reason=""):
        """Cancel the appointment"""
        self.status = "Cancelled"
        self.notes = reason
    
    def reschedule(self, new_date, new_time):
        """Reschedule the appointment"""
        self.date = new_date
        self.time = new_time
    
    def __str__(self):
        return f"Appointment({self.appointment_id}: {self.patient.get_full_name()} with {self.doctor.get_full_name()} on {self.date})"
    
    def __repr__(self):
        return self.__str__()
