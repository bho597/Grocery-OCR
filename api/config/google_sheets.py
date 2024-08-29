import os 

from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from api.config.settings import GoogleSheetsSettings


settings = GoogleSheetsSettings()
SCOPES = settings.scopes


def load_credentials(token_path, scopes):
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)
    else:
        creds = None
    return creds

def refresh_credentials(creds):
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except RefreshError:
            os.remove("token.json")
            creds = None
    return creds

def get_new_credentials(cred_file, scopes):
    flow = InstalledAppFlow.from_client_secrets_file(cred_file, scopes)
    creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    return creds

def get_credentials():
    creds = load_credentials("token.json", SCOPES)
    creds = refresh_credentials(creds) if creds else get_new_credentials("credentials.json", SCOPES)
    return creds