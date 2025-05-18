from flask import Flask, request, jsonify, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='assets', template_folder='templates')

# Email configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 465,
    'timeout': 10,
    'sender': os.getenv('EMAIL_USER'),
    'password': os.getenv('EMAIL_PASS'),
    'recipient': os.getenv('YOUR_EMAIL')
}

def send_email_via_gmail(form_data):
    """Send email using Gmail SMTP with enhanced error handling"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender']
        msg['To'] = EMAIL_CONFIG['recipient']
        msg['Subject'] = f"New Contact: {form_data.get('subject', 'No Subject')}"
        
        body = f"""
        Name: {form_data['name']}
        Email: {form_data['email']}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Message:
        {form_data['message']}
        """
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP_SSL(
            EMAIL_CONFIG['smtp_server'],
            EMAIL_CONFIG['smtp_port'],
            timeout=EMAIL_CONFIG['timeout']
        ) as server:
            server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
            server.send_message(msg)
        return True, None
    except Exception as e:
        logger.error(f"Email send failed: {str(e)}")
        return False, str(e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        data = request.get_json()
        required_fields = ['name', 'email', 'message']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400

        # Attempt to send email
        success, error = send_email_via_gmail(data)
        
        if not success:
            return jsonify({
                'error': f'Failed to send message: {error}',
                'success': False
            }), 500
            
        return jsonify({
            'success': True,
            'message': 'Your message has been sent successfully!'
        })
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'error': 'An unexpected error occurred',
            'success': False
        }), 500

if __name__ == '__main__':
    app.run(debug=True)