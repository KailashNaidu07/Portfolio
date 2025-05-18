from flask import Flask, request, jsonify
from flask_cors import CORS  # Remove if not needed
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Remove this line if frontend/backend are same domain

# Email Configuration
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
RECIPIENT_EMAIL = os.getenv('YOUR_EMAIL')

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all([data.get('name'), data.get('email'), data.get('message')]):
            return jsonify({"error": "Missing required fields"}), 400

        # Create email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"New Contact: {data.get('subject', 'No Subject')}"
        
        body = f"""
        Name: {data['name']}
        Email: {data['email']}
        Message: {data['message']}
        """
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        
        return jsonify({"success": True, "message": "Email sent successfully!"})

    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

if __name__ == '__main__':
    app.run(debug=True)