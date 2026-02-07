"""
Twilio SMS Handler
Sends and receives text messages
"""

from twilio.rest import Client


class TwilioHandler:
    def __init__(self, account_sid, auth_token):
        self.client = Client(account_sid, auth_token)
    
    def send_sms(self, to_number, message, from_number):
        """
        Send SMS to customer
        
        Args:
            to_number: Customer phone (E.164 format recommended: +12485551234)
            message: Text message content
            from_number: Your Twilio number
        
        Returns:
            message_sid if successful, None if failed
        """
        try:
            # Normalize phone number
            if not to_number.startswith('+'):
                # Assume US number, add +1
                to_number = f"+1{to_number.replace('-', '').replace(' ', '')}"
            
            message = self.client.messages.create(
                body=message,
                from_=from_number,
                to=to_number
            )
            
            print(f"SMS sent to {to_number}: {message.sid}")
            return message.sid
            
        except Exception as e:
            print(f"Error sending SMS to {to_number}: {e}")
            return None
    
    def get_message_history(self, phone_number, limit=20):
        """
        Get recent message history for a phone number
        """
        try:
            messages = self.client.messages.list(
                to=phone_number,
                limit=limit
            )
            
            return [
                {
                    'from': msg.from_,
                    'to': msg.to,
                    'body': msg.body,
                    'timestamp': msg.date_sent,
                    'status': msg.status
                }
                for msg in messages
            ]
            
        except Exception as e:
            print(f"Error fetching message history: {e}")
            return []
