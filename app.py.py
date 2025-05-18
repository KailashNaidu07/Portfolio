# app.py
from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='assets')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    
    # Email configuration
    sender_email = os.getenv('EMAIL_USER')
    sender_password = os.getenv('EMAIL_PASS')
    receiver_email = os.getenv('YOUR_EMAIL')
    
    # Create message
    message = MIMEMultipart()
    message['From'] = f"Portfolio Contact <{sender_email}>"
    message['To'] = receiver_email
    message['Subject'] = f"New message: {data.get('subject', 'No subject')}"
    
    # Email body
    body = f"""
    Name: {data.get('name', 'Not provided')}
    Email: {data.get('email', 'Not provided')}
    Message: {data.get('message', 'No message')}
    """
    
    message.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return jsonify({'success': True, 'message': 'Message sent successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)