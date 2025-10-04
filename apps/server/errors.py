"""
Error handling module for Time Traveler Agent.
Contains custom exceptions, error mappings, and validation utilities.
"""

import re
from typing import Dict, Tuple


# Custom exception classes for better error handling
class TimeTravelerError(Exception):
    """Base exception for Time Traveler specific errors"""
    def __init__(self, message: str, error_code: str = None, user_message: str = None):
        self.message = message
        self.error_code = error_code
        self.user_message = user_message or message
        super().__init__(self.message)


class PhoneNumberError(TimeTravelerError):
    """Invalid phone number format or validation error"""
    pass


class TwilioServiceError(TimeTravelerError):
    """Twilio service related errors"""
    pass


class ElevenLabsServiceError(TimeTravelerError):
    """ElevenLabs service related errors"""
    pass


class ConfigurationError(TimeTravelerError):
    """Configuration or environment variable errors"""
    pass


# Twilio error mappings
TWILIO_ERROR_MAPPINGS = {
    20003: {
        "error_code": "AUTHENTICATION_FAILED",
        "user_message": "Service authentication failed. Please try again later.",
        "suggestion": "Contact support if this persists."
    },
    21211: {
        "error_code": "INVALID_PHONE_NUMBER",
        "user_message": "Invalid phone number format.",
        "suggestion": "Please check that your number includes the country code (e.g., +1234567890)."
    },
    21214: {
        "error_code": "PHONE_NUMBER_NOT_REACHABLE",
        "user_message": "Phone number is not reachable.",
        "suggestion": "Please verify the number is correct and try again."
    },
    21610: {
        "error_code": "INVALID_FROM_NUMBER",
        "user_message": "Service configuration error.",
        "suggestion": "Please try again later or contact support."
    },
    21612: {
        "error_code": "PHONE_NUMBER_NOT_OWNED",
        "user_message": "Service configuration error.",
        "suggestion": "Please try again later or contact support."
    },
    21614: {
        "error_code": "PHONE_NUMBER_NOT_VERIFIED",
        "user_message": "Phone number not verified for this service.",
        "suggestion": "Please try a different number or contact support."
    },
    21617: {
        "error_code": "INVALID_CALLER_ID",
        "user_message": "Invalid caller ID configuration.",
        "suggestion": "Please try again later or contact support."
    },
    21618: {
        "error_code": "PHONE_NUMBER_BLOCKED",
        "user_message": "Phone number is blocked.",
        "suggestion": "Please try a different number."
    },
    21619: {
        "error_code": "INVALID_PHONE_NUMBER_FORMAT",
        "user_message": "Invalid phone number format.",
        "suggestion": "Please check that your number includes the country code (e.g., +1234567890)."
    }
}


def map_twilio_error(twilio_error) -> Dict[str, str]:
    """Map Twilio error codes to user-friendly messages"""
    error_code = getattr(twilio_error, 'code', None)
    if error_code and error_code in TWILIO_ERROR_MAPPINGS:
        return TWILIO_ERROR_MAPPINGS[error_code]
    
    # Default fallback
    return {
        "error_code": "TWILIO_ERROR",
        "user_message": "Call service temporarily unavailable.",
        "suggestion": "Please try again in a few moments."
    }


def validate_phone_number(phone: str) -> Tuple[bool, str]:
    """Validate phone number format"""
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Check if it starts with +
    if not cleaned.startswith('+'):
        return False, "Phone number must start with country code (e.g., +1234567890)"
    
    # Check if it has at least 10 digits after country code
    digits_only = cleaned[1:]  # Remove the +
    if len(digits_only) < 10:
        return False, "Phone number must have at least 10 digits"
    
    if len(digits_only) > 15:
        return False, "Phone number is too long (maximum 15 digits)"
    
    # Check for valid country code (1-3 digits)
    country_code_match = re.match(r'^\+(\d{1,3})', cleaned)
    if not country_code_match:
        return False, "Invalid country code format"
    
    return True, "Valid phone number"


def validate_year(year: int) -> Tuple[bool, str]:
    """Validate year input"""
    if year < -1500:
        return False, "Year must be after 1500 BC"
    if year > 3000:
        return False, "Year must be before 3000 AD"
    return True, "Valid year"


def validate_language(lang: str) -> Tuple[bool, str]:
    """Validate language input"""
    if lang not in ['en', 'es']:
        return False, 'Language must be either "en" or "es"'
    return True, "Valid language"
