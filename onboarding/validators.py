import re
from django.core.exceptions import ValidationError

def validate_phone_number(value):
    """Validate phone number format with country code"""
    if not value:
        return value
    
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', value)
    
    # Check if it starts with + and has 10-15 digits
    if not re.match(r'^\+?1?\d{9,15}$', cleaned):
        raise ValidationError(
            'Phone number must be entered in the format: +1234567890 or 1234567890'
        )
    
    return cleaned

def validate_email_format(value):
    """Validate email format"""
    if not value:
        return value
    
    # Basic email format validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, value):
        raise ValidationError('Invalid email format')
    
    return value

def validate_zipcode(value):
    """Validate zipcode format"""
    if not value:
        return value
    
    # Allow alphanumeric zipcodes (international)
    if not re.match(r'^[A-Za-z0-9\s-]{3,10}$', value):
        raise ValidationError('Invalid zipcode format')
    
    return value 