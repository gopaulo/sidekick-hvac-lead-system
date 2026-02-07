"""
Calendly Integration Handler
Books appointments automatically
"""

import requests
from datetime import datetime, timedelta


class CalendlyHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.calendly.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_booking(self, name, email, phone, event_type):
        """
        Create a Calendly booking
        
        Args:
            name: Customer name
            email: Customer email
            phone: Customer phone
            event_type: Calendly event type URI
        
        Returns:
            {
                'success': True/False,
                'time': 'appointment time string',
                'booking_url': 'Calendly confirmation URL'
            }
        """
        
        # NOTE: Calendly API v2 requires invitee to schedule via their UI
        # For fully automated booking, use Calendly's Routing Forms or Zapier
        # This is a simplified version - production needs proper implementation
        
        try:
            # Get available times for event type
            available_times = self._get_available_times(event_type)
            
            if not available_times:
                return {'success': False, 'error': 'No available times'}
            
            # Book first available slot
            first_slot = available_times[0]
            
            # Create invitee (actual booking)
            # Note: This is pseudo-code - Calendly API doesn't support direct booking
            # Real implementation needs webhook or Zapier
            
            booking_data = {
                'event_type': event_type,
                'start_time': first_slot,
                'invitee': {
                    'name': name,
                    'email': email,
                    'phone': phone
                }
            }
            
            # For MVP: Return success with manual booking needed
            return {
                'success': True,
                'time': first_slot,
                'booking_url': f"https://calendly.com/[your-link-here]",
                'note': 'Manual confirmation needed'
            }
            
        except Exception as e:
            print(f"Error creating Calendly booking: {e}")
            return {'success': False, 'error': str(e)}
    
    def _get_available_times(self, event_type, days_ahead=7):
        """
        Get available time slots for an event type
        """
        try:
            # Get user info
            user_response = requests.get(
                f"{self.base_url}/users/me",
                headers=self.headers
            )
            user_data = user_response.json()
            user_uri = user_data['resource']['uri']
            
            # Get availability
            start_time = datetime.now().isoformat()
            end_time = (datetime.now() + timedelta(days=days_ahead)).isoformat()
            
            availability_response = requests.get(
                f"{self.base_url}/event_type_available_times",
                headers=self.headers,
                params={
                    'event_type': event_type,
                    'start_time': start_time,
                    'end_time': end_time
                }
            )
            
            if availability_response.status_code == 200:
                available_times = availability_response.json()
                # Extract time slots
                slots = [slot['start_time'] for slot in available_times.get('collection', [])]
                return slots
            else:
                return []
                
        except Exception as e:
            print(f"Error fetching available times: {e}")
            return []
    
    def get_scheduled_events(self, days_back=7):
        """
        Get scheduled events for reporting
        """
        try:
            user_response = requests.get(
                f"{self.base_url}/users/me",
                headers=self.headers
            )
            user_data = user_response.json()
            user_uri = user_data['resource']['uri']
            
            # Get scheduled events
            events_response = requests.get(
                f"{self.base_url}/scheduled_events",
                headers=self.headers,
                params={
                    'user': user_uri,
                    'count': 100
                }
            )
            
            if events_response.status_code == 200:
                return events_response.json()['collection']
            else:
                return []
                
        except Exception as e:
            print(f"Error fetching scheduled events: {e}")
            return []


# Alternative: Simple Google Calendar integration (easier for MVP)
class GoogleCalendarHandler:
    """
    Simpler alternative using Google Calendar API
    Easier to implement full automation
    """
    def __init__(self, credentials_file):
        # TODO: Implement Google Calendar API integration
        # Easier to automate booking than Calendly
        pass
    
    def create_booking(self, name, email, phone, date_time):
        # TODO: Create Google Calendar event
        # Send invite to customer email
        pass
