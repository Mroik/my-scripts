from os.path import exists
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError


SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events.readonly",
]
WEEKDAY = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)


def setup():
    creds = None
    if exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as fd:
            fd.write(creds.to_json())
    return creds


def main():
    creds = setup()
    try:
        service = build("calendar", "v3", credentials=creds)
        events = service.events().list(
            calendarId="REPLACE ME",
            timeMin=datetime.now().utcnow().isoformat() + "Z",
            timeMax=(datetime.now() + timedelta(days=7)).isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime",
        ).execute().get("items", [])

        prev = None

        if not events:
            print("No events")
        for event in events:
            date = datetime.fromisoformat(event["start"]["dateTime"])
            if prev is None or prev != date.day:
                print()
                print(date.date(), end=" ")
                print(WEEKDAY[date.weekday()])
            print(date.time())
            print(event["summary"])
            prev = date.day

    except HttpError as e:
        print(f"{e}")


if __name__ == "__main__":
    main()
