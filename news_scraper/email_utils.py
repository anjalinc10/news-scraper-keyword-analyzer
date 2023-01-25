import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email_with_attachment(sender_email, sender_password, recipient_email, subject, file_path):
    # create an SMTP object
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    server.starttls()
    # Login to the server
    server.login(sender_email, sender_password)
    # create a message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    # attach the file
    print(f"Sending Email to {recipient_email}.")
    with open(file_path, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('content-disposition', 'attachment', filename=file_path.split("/")[-1])
        msg.attach(attach)
    # send the mail
    server.send_message(msg)
    # close the server
    print("The Email has been sent!")
    server.quit()
