import os
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Environment variables
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
CALENDLY_URL = os.environ.get('CALENDLY_URL', 'https://calendly.com/max-splendor/30min')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'sidekick-sms-webhook'})

@app.route('/sms', methods=['POST'])
def sms_webhook():
    resp = MessagingResponse()
    resp.message(f"Thanks for reaching out! Schedule a call with us here: {CALENDLY_URL}")
    return str(resp), 200, {'Content-Type': 'text/xml'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
