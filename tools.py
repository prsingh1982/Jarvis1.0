import logging
from typing import Optional
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun 

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

@function_tool
async def get_weather(
    context: RunContext,
    city: str) -> str:
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(
            f"http://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
        
    except Exception as e:
        logging.error(f"Error getting weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}."

@function_tool
async def web_search(
    context: RunContext,
    query: str) -> str:
    """
    Perform a web search using DuckDuckGo.
    """
    try:
        search = DuckDuckGoSearchRun()
        results = search.run(tool_input=query)
        if results:
            logging.info(f"Search results for '{query}': {results}")
            return results
        else:
            logging.info(f"No results found for '{query}'.")
            return f"No results found for '{query}'."
        
    except Exception as e:
        logging.error(f"Error performing web search for '{query}': {e}")
        return f"An error occurred while searching for '{query}'."
    

@function_tool
async def send_email(
    context: RunContext,
    recipient: str,
    subject: str,
    body: str,
    cc_email: Optional[str] = None
) -> str:
    """
    Send an email using Gmail SMTP.

    Args:
        recipient: The recipient's email address.
        subject: The subject of the email.
        body: The body content of the email.
        cc_email: An optional CC email address.
    """

    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        gmail_user = os.getenv("GMAIL_USER")
        gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_app_password:
            logging.error("Gmail Credentials not found in environment variables.")
            return "Email sending failed: Email credentials are missing."
    
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = recipient
        msg['Subject'] = subject
        recepients = [recipient]
        if cc_email:
            msg['Cc'] = cc_email
            recepients.append(cc_email)
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(gmail_user, gmail_app_password)

        text = msg.as_string()
        server.sendmail(gmail_user, recepients, text)
        server.quit()

        logging.info(f"Email sent to {recipient} with subject '{subject}'.")
        return f"Email successfully sent to {recipient}."
    except smtplib.SMTPAuthenticationError:
        logging.error("SMTP Authentication Error: Check your Gmail credentials.")
        return "Email sending failed: Authentication error."
    except smtplib.SMTPException as e:
        logging.error(f"SMTP Error sending email to {recipient}: {e}")
        return f"Email sending failed due to SMTP error. - {str(e)}"
    except Exception as e:
        logging.error(f"Error sending email to {recipient}: {e}")
        return f"An error occurred while sending email to {recipient}."