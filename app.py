"""
Sidekick AI Lead System - Main Webhook Server
Receives leads from any source, qualifies via AI, books appointments
"""

from flask import Flask, request, jsonify
import json
from datetime import datetime
from hvac_agent import HVACAgent
from twilio_handler import TwilioHandler
from calendly_handler import CalendlyHandler
import config

app = Flask(__name__)

# Initialize handlers
hvac_agent = HVACAgent()
twilio = TwilioHandler(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
calendly = CalendlyHandler(config.CALENDLY_API_KEY)

# In-memory lead storage (replace with database in production)
leads = {}


@app.route('/webhook/lead', methods=['POST'])
def receive_lead():
    """
    Receives new lead from any source
    Expected fields: name, phone, email, service_type (optional)
    """
    data = request.json
    
    # Extract lead info
    lead = {
        'id': f"lead_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'name': data.get('name'),
        'phone': data.get('phone'),
        'email': data.get('email'),
        'service_type': data.get('service_type', 'not specified'),
        'source': data.get('source', 'unknown'),
        'timestamp': datetime.now().isoformat(),
        'status': 'new'
    }
    
    # Validate required fields
    if not lead['phone']:
        return jsonify({'error': 'Phone number required'}), 400
    
    # Store lead
    leads[lead['id']] = lead
    
    # Send initial SMS
    initial_message = hvac_agent.get_initial_message(lead['name'])
    twilio.send_sms(
        to_number=lead['phone'],
        message=initial_message,
        from_number=config.TWILIO_PHONE_NUMBER
    )
    
    # Update lead status
    leads[lead['id']]['status'] = 'contacted'
    leads[lead['id']]['last_message'] = initial_message
    
    return jsonify({
        'success': True,
        'lead_id': lead['id'],
        'message': 'Lead received and contacted'
    }), 200


@app.route('/webhook/sms', methods=['POST'])
def receive_sms():
    """
    Receives incoming SMS from Twilio
    Processes response and continues qualification
    """
    from_number = request.form.get('From')
    message_body = request.form.get('Body')
    
    # Find lead by phone number
    lead = None
    lead_id = None
    for lid, l in leads.items():
        if l['phone'] == from_number or l['phone'] == from_number.replace('+1', ''):
            lead = l
            lead_id = lid
            break
    
    if not lead:
        # Unknown number - send generic response
        twilio.send_sms(
            to_number=from_number,
            message="Thanks for reaching out! Please call our office at [COMPANY_PHONE] for assistance.",
            from_number=config.TWILIO_PHONE_NUMBER
        )
        return jsonify({'success': True}), 200
    
    # Process response with AI
    response = hvac_agent.process_response(lead, message_body)
    
    # Check if ready to book
    if response['action'] == 'book_appointment':
        # Book via Calendly
        booking = calendly.create_booking(
            name=lead['name'],
            email=lead['email'],
            phone=lead['phone'],
            event_type=config.CALENDLY_EVENT_TYPE
        )
        
        if booking['success']:
            confirmation_message = f"Perfect! I've booked your estimate for {booking['time']}. You'll receive a confirmation email shortly. See you then!"
            leads[lead_id]['status'] = 'booked'
            leads[lead_id]['appointment_time'] = booking['time']
        else:
            confirmation_message = "I'm having trouble accessing the calendar. Let me connect you with someone who can help. Expect a call within 30 minutes."
            leads[lead_id]['status'] = 'escalated'
    
    elif response['action'] == 'escalate':
        confirmation_message = response['message']
        leads[lead_id]['status'] = 'escalated'
        # TODO: Send alert to company (Slack, email, SMS to owner)
    
    else:
        confirmation_message = response['message']
    
    # Send response
    twilio.send_sms(
        to_number=from_number,
        message=confirmation_message,
        from_number=config.TWILIO_PHONE_NUMBER
    )
    
    # Update lead
    leads[lead_id]['last_message'] = confirmation_message
    leads[lead_id]['last_response'] = message_body
    
    return jsonify({'success': True}), 200


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Simple dashboard showing all leads and their status
    """
    html = """
    <html>
    <head><title>Sidekick AI Lead Dashboard</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h1>Sidekick AI Lead System</h1>
        <h2>Recent Leads</h2>
        <table border="1" cellpadding="10">
            <tr>
                <th>Time</th>
                <th>Name</th>
                <th>Phone</th>
                <th>Service</th>
                <th>Status</th>
                <th>Last Message</th>
            </tr>
    """
    
    for lead in sorted(leads.values(), key=lambda x: x['timestamp'], reverse=True):
        html += f"""
            <tr>
                <td>{lead['timestamp'][:16]}</td>
                <td>{lead['name']}</td>
                <td>{lead['phone']}</td>
                <td>{lead.get('service_type', 'N/A')}</td>
                <td><strong>{lead['status']}</strong></td>
                <td>{lead.get('last_message', 'N/A')[:50]}...</td>
            </tr>
        """
    
    html += """
        </table>
        <br><br>
        <p>Total Leads: {}</p>
        <p>Booked: {}</p>
        <p>In Progress: {}</p>
    </body>
    </html>
    """.format(
        len(leads),
        len([l for l in leads.values() if l['status'] == 'booked']),
        len([l for l in leads.values() if l['status'] == 'contacted'])
    )
    
    return html


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
