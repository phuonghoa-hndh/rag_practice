import os

import msal
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = os.getenv("AUTHORITY")
SCOPE = os.getenv("SCOPE")
GRANT_TYPE = os.getenv("GRANT_TYPE")
TENANT_ID = os.getenv("TENANT_ID")
TOKEN_REQUEST_URI = os.getenv("TOKEN_REQUEST_URI")

# Initialize MSAL Confidential Client
app = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)


def get_access_token():
    token_request_uri = TOKEN_REQUEST_URI
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": GRANT_TYPE,
        "scope": SCOPE,
    }
    resp = requests.post(
        token_request_uri,
        data=data,
    )
    token_response = resp.json()
    access_token = token_response.get("access_token")
    return access_token
