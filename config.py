"""
Configuration File - FILL IN YOUR API CREDENTIALS
"""

# Twilio Configuration
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"  # Get from twilio.com/console
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"    # Get from twilio.com/console
TWILIO_PHONE_NUMBER = "+12485551234"            # Your Twilio number (format: +1XXXXXXXXXX)

# Calendly Configuration
CALENDLY_API_KEY = "YOUR_CALENDLY_API_KEY"      # Get from calendly.com/integrations/api_webhooks
CALENDLY_EVENT_TYPE = "https://api.calendly.com/event_types/XXXXXX"  # Your event type URI

# OpenRouter (AI) Configuration
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"  # Get from openrouter.ai
AI_MODEL = "anthropic/claude-3.5-sonnet"        # Or "openai/gpt-4" or cheaper options

# Company Information (for SMS responses)
COMPANY_NAME = "ABC Heating & Cooling"
COMPANY_PHONE = "(248) 555-1234"
SERVICE_AREA = "Rochester Hills, Troy, Auburn Hills, Bloomfield, Sterling Heights"

# System Settings
DEBUG = True  # Set to False in production
LOG_LEVEL = "INFO"

# Database (for production - currently using in-memory storage)
# DATABASE_URL = "postgresql://user:pass@localhost/sidekick_leads"
