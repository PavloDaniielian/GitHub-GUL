import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define the email sender and receiver
sender_email = "corecore0417@outlook.com"
password = "Rkdtjdus1!"

# Create the email content
subject = "I can hire you providing $100 hourly!"
body = "Hello, I know you are finding new job.\nI favourite you.\nIf you are agree, reply to this\nGood Luck!\nBest Regards"

receiver_email = "aphpollo.dev@gmail.com"
# Set up the email message with subject and body
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Attach the email body text
message.attach(MIMEText(body, "plain"))

# Set up the SMTP server connection
try:
    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        #server.sendmail(sender_email, receiver_email, message.as_string())
        server.send_message(message)  # Send the email
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")