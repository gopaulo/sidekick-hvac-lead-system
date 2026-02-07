from flask import Flask, request
import os
from twilio.rest import Client
from anthropic import Anthropic

app = Flask(__name__)

twilio_client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
anthropic_client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

@app.route('/sms', methods=['POST'])
def sms_reply():
    from_number = request.form.get('From')
    body = request.form.get('Body')
    
    response = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": f"You are an HVAC assistant. Customer said: {body}. Reply under 160 chars with Calendly link: {os.environ.get('CALENDLY_URL')}"}]
    )
    
    reply_text = response.content[0].text
    
    twilio_client.messages.create(
        to=from_number,
        from_=os.environ.get('TWILIO_PHONE_NUMBER'),
        body=reply_text
    )
    
    return '', 200

@app.route('/')
def health():
    return 'HVAC Lead System Online', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
