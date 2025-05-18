from flask import Flask, request, jsonify, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='assets', template_folder='templates')

# Configure email settings
EMAIL_CONFIG = {
    'user': os.getenv('EMAIL_USER', 'kailashnaidu07@gmail.com'),
    'password': os.getenv('EMAIL_PASS', 'nfmpcbpgixtenuos'),
    'recipient': os.getenv('YOUR_EMAIL', 'kailashnaidu07@gmail.com'),
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 465
}

@app.route('/')
def home():
    """Serve the main portfolio page"""
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    """Process contact form submissions"""
    try:
        # Get and validate form data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400

        required_fields = ['name', 'email', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400

        # Create email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['user']
        msg['To'] = EMAIL_CONFIG['recipient']
        msg['Subject'] = f"New Contact: {data.get('subject', 'No Subject')}"
        
        email_body = f"""
        Name: {data['name']}
        Email: {data['email']}
        Message:
        {data['message']}
        """
        msg.attach(MIMEText(email_body, 'plain'))

        # Send email
        with smtplib.SMTP_SSL(
            EMAIL_CONFIG['smtp_server'],
            EMAIL_CONFIG['smtp_port'],
            timeout=10
        ) as server:
            server.login(EMAIL_CONFIG['user'], EMAIL_CONFIG['password'])
            server.send_message(msg)

        return jsonify({
            'success': True,
            'message': 'Your message has been sent successfully!'
        })

    except smtplib.SMTPAuthenticationError:
        return jsonify({
            'error': 'Email authentication failed. Please check your credentials.',
            'success': False
        }), 401
        
    except Exception as e:
        # Log the error for debugging
        app.logger.error(f'Error sending email: {str(e)}')
        return jsonify({
            'error': 'An internal server error occurred',
            'success': False
        }), 500

if __name__ == '__main__':
    app.run(debug=True)