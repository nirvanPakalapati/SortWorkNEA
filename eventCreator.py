import quickstart
import datetime
from datetime import timedelta
from datetime import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#Run the quickstart to get the service build
#This function will redefine the event dictionary and run a method to place it in the calendar
#Then debug this to let me know that event has been created

def createEvent(start, end, summary, description):
    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start,
            "timeZone": "UTC" # will change to make it variable later, for now assume in UTC
        },

        "end": {
            "dateTIme": end,
            "timeZone": "UTC" # will change to make it variable later, for now assume in UTC
        },
        "recurrence":{
            "RRULE:FREQ=DAILY;COUNT=1"
        }
    }

    quickstart.main()
    event = quickstart.service.events().insert(calendarId="primary", body=event).execute()