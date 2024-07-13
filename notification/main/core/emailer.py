import os
import pickle
import base64
import smtplib
import json
from email.message import EmailMessage

from main.core.config import get_app_settings
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from main.core.logger import logger

settings = get_app_settings()

class Notification:
    def __init__(self):
        self.credentials_file = settings.credentials_file
        self.token_file = settings.token_file
        self.scopes = ['https://mail.google.com/']
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    def _get_credentials(self):
        creds = None

        credentials_file_path = os.path.join(self.current_dir, self.credentials_file )
        
        # Check if the token file exists and load it
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials are available, perform the OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file_path, self.scopes)
                creds = flow.run_local_server(port=3000)
            # Save the credentials for future use
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def send_email(self, message):
        try:
            logger.info("Trying to get credentials")
            creds = self._get_credentials()
            access_token = creds.token
            logger.info("Obtained access token, %s", access_token)


            message = json.loads(message.body.decode())
            mp3_fid = message["mp3_fid"]
            logger.info("Obtained mp3_fid, %s", mp3_fid)
            
            msg = EmailMessage()
            msg.set_content(f"mp3 file_id: {mp3_fid} is now ready!")
            msg['Subject'] = 'MP3 Download!'
            msg['From'] = settings.gmail_admin_email_address
            msg['To'] = message["email"]

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                # Create the authentication string for XOAUTH2
                logger.info("Attempting to connect to gmail")
                auth_string = f'user={settings.gmail_admin_email_address}\1auth=Bearer {access_token}\1\1'
                auth_string = base64.b64encode(auth_string.encode()).decode()

                # Authenticate using the XOAUTH2 mechanism
                server.ehlo()
                server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
                server.send_message(msg)
                logger.info("Mail Sent using %s", mp3_fid)
        except Exception as err:
            logger.error("Exception occurred during email process: %s", err)

def create_notifier():
    """
    Initialize email notification agent.
    """
    return Notification()

notifier = create_notifier()
