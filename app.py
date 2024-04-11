from flask import Flask, render_template, request, redirect, url_for, flash
import re
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

GMAIL_USERNAME = 'votrinhnhan1403@gmail.com'  # Your Gmail username
GMAIL_PASSWORD = 'xuzy egdc brrw jbef'  # Your Gmail password (make sure to keep it secure)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        sender_email = GMAIL_USERNAME
        recipient = request.form['recipient']
        message = request.form['message']
        image = request.files['image']

        # Validate email
        if not validate_email_custom(recipient):
            flash('Invalid email address', 'error')
            return redirect(url_for('index'))

        # Send email
        send_email(sender_email, recipient, message, image)

        flash('Image sent successfully', 'success')
        return redirect(url_for('index'))

def validate_email_custom(email):
    # Basic regex pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def send_email(sender_email, recipient, message, image):
    try:
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = 'Image from Image Uploader'

        # Add message body
        msg.attach(MIMEText(message, 'plain'))

        # Add image attachment
        image_data = image.read()
        image_name = image.filename
        image_mime = MIMEImage(image_data, name=image_name)
        msg.attach(image_mime)

        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USERNAME, GMAIL_PASSWORD)

            # Send the email
            smtp.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    app.run(debug=True)
