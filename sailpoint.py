import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# GitHub API configuration
repo_owner = "OWNER"
repo_name = "REPO"
github_pat = "YOUR_GITHUB_PAT"
github_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"

# Email configuration
email_from = "decogzz@gmail.com"
email_to = "decogzz@gmail.com"
email_subject = "Weekly Pull Request Summary"

# Calculate the date range for the past week
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

# Prepare the GitHub API headers with your PAT
headers = {
    "Authorization": f"token {github_pat}",
    "Accept": "application/vnd.github.v3+json",
}

# Define a function to get pull requests within a date range
def get_pull_requests():
    params = {
        "state": "all",
        "sort": "created",
        "direction": "desc",
    }
    response = requests.get(github_api_url, params=params, headers=headers)
    response.raise_for_status()
    pull_requests = response.json()
    return [pr for pr in pull_requests if start_date <= datetime.fromisoformat(pr["created_at"][:-1])]

# Get the pull requests
pull_requests = get_pull_requests()

# Create the email content
email_content = "<h2>Weekly Pull Request Summary</h2>\n\n"
for pr in pull_requests:
    email_content += f"<strong>#{pr['number']}</strong> ({pr['state']}): {pr['title']}<br>\n"
    email_content += f"Created by {pr['user']['login']} on {pr['created_at']}<br>\n"
    email_content += f"URL: {pr['html_url']}<br><br>\n"

# Create the email message
email_message = MIMEMultipart()
email_message["From"] = email_from
email_message["To"] = email_to
email_message["Subject"] = email_subject
email_message.attach(MIMEText(email_content, "html"))

# Send the email
try:
    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login(email_from, "YOUR_EMAIL_PASSWORD")
    smtp_server.sendmail(email_from, email_to, email_message.as_string())
    smtp_server.quit()
    print("Email sent successfully.")
except Exception as e:
    print(f"Email sending failed: {str(e)}")
