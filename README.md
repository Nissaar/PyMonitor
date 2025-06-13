# PyMonitor

**PyMonitor** is a lightweight Python-based monitoring tool designed for Linux servers. It continuously checks CPU, RAM, and Disk usage, and sends email alerts when usage crosses defined thresholds. The application runs as a background service via `systemd`, making it suitable for continuous monitoring in production or academic environments.

## Features

- Monitors system resource usage (CPU, RAM, Disk)
- Sends automated email alerts on threshold breaches
- Configuration-driven via `config.json`
- Runs persistently as a Linux systemd service
- Lightweight and easy to deploy

## Requirements

- Python 3.x
- Linux system (Amazon Linux, Ubuntu, CentOS, etc.)
- Python `psutil` module
- SMTP credentials (email account for alerts)

Install required Python module:

```bash
pip3 install psutil
```

## Configuration

Create a `config.json` file in the same directory as `pymonitor.py` with the following content:

```json
{
  "cpu_threshold": 85,
  "ram_threshold": 90,
  "disk_threshold": 90,
  "check_interval": 60,
  "email": {
    "sender": "your_email@example.com",
    "recipient": "admin@example.com",
    "smtp_server": "smtp.example.com",
    "smtp_port": 587,
    "username": "your_email@example.com",
    "password": "your_email_password"
  }
}
```

⚠️ **Warning:** Do not commit real SMTP credentials to public repositories. Consider using environment variables or secrets in production.

## Running the App

To run the application manually for testing:

```bash
python3 pymonitor.py
```

To deploy it as a persistent service:

1. Create application directory:

```bash
sudo mkdir -p /opt/pymonitor
sudo cp pymonitor.py config.json /opt/pymonitor/
```

2. Create the systemd service file:

```bash
sudo tee /etc/systemd/system/pymonitor.service > /dev/null <<EOF
[Unit]
Description=PyMonitor - Linux Monitoring Tool
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/pymonitor/pymonitor.py
WorkingDirectory=/opt/pymonitor
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF
```

3. Reload systemd and start the service:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable pymonitor
sudo systemctl start pymonitor
```

4. To check if it's running:

```bash
sudo systemctl status pymonitor
```

## Email Alerts

PyMonitor sends alert emails to the configured recipient when thresholds for CPU, RAM, or Disk usage are exceeded. Make sure the SMTP credentials are valid and supported by your mail provider (Gmail, Outlook, etc.).

## Security Notes

- Do not expose your email credentials.
- For production, use app-specific passwords or SMTP relay accounts.
- You may enhance security by using encrypted secrets or configuration management tools.

## Project Structure

```
pymonitor/
├── pymonitor.py         # Main script
├── config.json          # Configuration file
└── README.md            # Project documentation
```

## Author

**Muhammad Nissaar Mushir Gopee**  
Mauritius 🇲🇺

## License

MIT License
