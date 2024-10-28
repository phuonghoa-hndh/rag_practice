import msal
import requests
from constant import CLIENT_ID, CLIENT_SECRET, AUTHORITY, SCOPE, GRANT_TYPE, TENANT_ID, TOKEN_REQUEST_URI


# Initialize MSAL Confidential Client
app = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)


def get_access_token():
    token_request_uri = TOKEN_REQUEST_URI
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
        'scope': SCOPE
    }
    resp = requests.post(
        token_request_uri,
        data=data,
    )
    token_response = resp.json()
    access_token = token_response.get('access_token')
    return access_token
