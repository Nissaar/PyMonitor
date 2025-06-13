import psutil
import smtplib
import time
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Load configuration from config.json
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

with open(CONFIG_FILE) as f:
    config = json.load(f)

cpu_threshold = config['cpu_threshold']
ram_threshold = config['ram_threshold']
disk_threshold = config['disk_threshold']
check_interval = config['check_interval']
email_settings = config['email']

# Email alert function
def send_email_alert(subject, body):
    msg = MIMEMultipart()
    msg['From'] = email_settings['sender']
    msg['To'] = email_settings['recipient']
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(email_settings['smtp_server'], email_settings['smtp_port'])
        server.starttls()
        server.login(email_settings['username'], email_settings['password'])
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

# Monitoring loop
def monitor():
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        alerts = []

        if cpu > cpu_threshold:
            alerts.append(f"High CPU usage detected: {cpu}%")

        if ram > ram_threshold:
            alerts.append(f"High RAM usage detected: {ram}%")

        if disk > disk_threshold:
            alerts.append(f"High Disk usage detected: {disk}%")

        if alerts:
            subject = "[PyMonitor] Resource Alert"
            body = "\n".join(alerts)
            send_email_alert(subject, body)

        time.sleep(check_interval)

if __name__ == "__main__":
    monitor()

