import imaplib
import email
from email.header import decode_header
from twilio.rest import Client
import time

# Email and IMAP settings
EMAIL = 'refer5193@gmail.com'
PASSWORD = 'ztontuokelrvcreg'  # Use App Password if 2FA is enabled
IMAP_SERVER = 'imap.gmail.com'
FROM_EMAIL = 'saiteja1234v@gmail.com'  # The specific sender to watch

# Twilio credentials
TWILIO_SID = 'ACb89fa8c68bd0c03ed9a4299a2f7c19ef'
TWILIO_AUTH = '9a4b9609000327b3e444d9d3b57e9de0'
FROM_WHATSAPP = 'whatsapp:+14155238886'  # Twilio Sandbox number
TO_WHATSAPP = 'whatsapp:+919705602313'   # Your verified number

# Initialize Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH)

def send_whatsapp_alert(subject):
    message = client.messages.create(
        body=f"You received an email from {FROM_EMAIL} with subject: {subject}",
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP
    )
    print("WhatsApp message sent:", message.sid)

def check_mail():
    print("Connecting to mail server...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    print(f"Searching for unseen emails from {FROM_EMAIL}...")
    status, messages = mail.search(None, f'(UNSEEN FROM "{FROM_EMAIL}")')

    if status == "OK":
        email_nums = messages[0].split()
        if not email_nums:
            print("No new emails found.")
        for num in email_nums:
            _, data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            subject, _ = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            print(f"New email found with subject: {subject}")
            send_whatsapp_alert(subject)
    else:
        print("Failed to search emails.")

    mail.logout()
    print("Logged out.")

print("Starting email watcher. Press Ctrl+C to exit.")
while True:
    try:
        check_mail()
        print("Waiting 60 seconds before next check...\n")
        time.sleep(60)
    except Exception as e:
        print("Error:", e)
        time.sleep(60)
 