"""
HVAC AI Agent - Qualification Logic
Handles conversation flow for HVAC lead qualification
"""

import openai
import config
from prompts import SYSTEM_PROMPT, INITIAL_MESSAGE_TEMPLATE


class HVACAgent:
    def __init__(self):
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=config.OPENROUTER_API_KEY
        )
        self.conversation_history = {}
    
    def get_initial_message(self, name=None):
        """
        Generate initial outreach message
        """
        if name:
            return INITIAL_MESSAGE_TEMPLATE.format(name=name)
        else:
            return INITIAL_MESSAGE_TEMPLATE.format(name="there")
    
    def process_response(self, lead, message):
        """
        Process customer response and determine next action
        
        Returns:
            {
                'action': 'continue' | 'book_appointment' | 'escalate',
                'message': 'response text',
                'qualification_data': {...}
            }
        """
        lead_id = lead['id']
        
        # Initialize conversation history for this lead
        if lead_id not in self.conversation_history:
            self.conversation_history[lead_id] = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
        
        # Add customer message to history
        self.conversation_history[lead_id].append({
            "role": "user",
            "content": f"Customer response: {message}"
        })
        
        # Get AI response
        try:
            response = self.client.chat.completions.create(
                model=config.AI_MODEL,
                messages=self.conversation_history[lead_id],
                temperature=0.7,
                max_tokens=300
            )
            
            ai_message = response.choices[0].message.content
            
            # Add AI response to history
            self.conversation_history[lead_id].append({
                "role": "assistant",
                "content": ai_message
            })
            
            # Parse AI response for actions
            result = self._parse_ai_response(ai_message, lead)
            
            return result
            
        except Exception as e:
            print(f"Error calling AI: {e}")
            return {
                'action': 'escalate',
                'message': "I'm having trouble processing that. Let me connect you with someone who can help right away. Expect a call within 30 minutes."
            }
    
    def _parse_ai_response(self, ai_message, lead):
        """
        Parse AI response to determine action
        
        Looks for markers:
        - [BOOK] = ready to book appointment
        - [ESCALATE] = needs human intervention
        - [CONTINUE] = continue qualification
        """
        
        if '[BOOK]' in ai_message:
            return {
                'action': 'book_appointment',
                'message': ai_message.replace('[BOOK]', '').strip(),
                'qualification_data': self._extract_qualification_data(lead)
            }
        
        elif '[ESCALATE]' in ai_message:
            return {
                'action': 'escalate',
                'message': ai_message.replace('[ESCALATE]', '').strip()
            }
        
        else:
            return {
                'action': 'continue',
                'message': ai_message.replace('[CONTINUE]', '').strip()
            }
    
    def _extract_qualification_data(self, lead):
        """
        Extract qualification data from conversation history
        """
        # TODO: Parse conversation to extract:
        # - Service type (heating, cooling, both, other)
        # - Urgency (emergency, soon, flexible)
        # - Property type (residential, commercial)
        # - Budget awareness
        
        return {
            'qualified': True,
            'service_type': lead.get('service_type', 'unknown'),
            'urgency': 'unknown'
        }
