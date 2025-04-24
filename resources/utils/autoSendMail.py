import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender, receiver, subject, body, password):

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()
        server.login(sender, password)

        text = message.as_string()
        server.sendmail(sender, receiver, text)
        print(f"Email send to {receiver} success")

        server.quit()
        return True

    except smtplib.SMTPException as e:
        print(f"Error while send email: {e}")
        return False

