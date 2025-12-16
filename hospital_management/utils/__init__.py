"""
Utilities package
Contains helper functions and utilities
"""
import re


def format_date(date):
    """Format date object to string"""
    return date.strftime("%Y-%m-%d") if date else ""


def format_time(time):
    """Format time object to string"""
    return time.strftime("%H:%M") if time else ""


def validate_email(email):
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Basic phone number validation"""
    # Remove common separators
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if it's a valid phone number (10-15 digits)
    return len(phone) >= 10 and len(phone) <= 15 and phone.isdigit()
