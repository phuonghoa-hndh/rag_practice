import requests
import json
from authenticate import get_access_token
from datetime import datetime, timedelta
from constant import URL


def create_teams_meetings(user_input):
    start_time = datetime.now() + timedelta(minutes=30)
    end_time = start_time + timedelta(minutes=30)
    access_token = get_access_token()

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    url = URL
    meeting_data = {
        "subject": "Techvify Meeting",
        "body": {
            "contentType": "HTML",
            "content": "Does next month work for you?"
        },
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "UTC"
        },
        "location": {
            "displayName": "Dissneyland"
        },
        "attendees": [
            {
                "emailAddress": {
                    "address": "phuonghoa.hndh@gmail.com",
                    "name": "Hoa"
                },
                "type": "required"
            }
        ],
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "teamsForBusiness"
    }

    response = requests.post(
        url, headers=headers, data=json.dumps(meeting_data))
    if response.status_code == 201:
        meeting_data = response.json()
        # meeting_id = meeting_data["id"]
        # print("Meeting created successfully. Meeting ID:", meeting_id)
        # print("Join URL:", meeting_data["onlineMeeting"]["joinUrl"])
        return meeting_data["onlineMeeting"]["joinUrl"]
    else:
        return response.status_code
