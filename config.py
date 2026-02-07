"""
Configuration File - Reads from Environment Variables
"""
import os

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')

# Calendly Configuration  
CALENDLY_URL = os.environ.get('CALENDLY_URL', 'https://calendly.com/max-splendor/30min')
CALENDLY_API_KEY = None  # Not using API, just sending URL in SMS
CALENDLY_EVENT_TYPE = None  # Not using API

# OpenRouter (AI) Configuration
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
AI_MODEL = "anthropic/claude-3.5-sonnet"

# Company Information (for SMS responses)
COMPANY_NAME = "Sidekick HVAC"
COMPANY_PHONE = os.environ.get('TWILIO_PHONE_NUMBER', '(248) 480-8761')
SERVICE_AREA = "Rochester Hills, Troy, Auburn Hills, Bloomfield, Sterling Heights"

# System Settings
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
