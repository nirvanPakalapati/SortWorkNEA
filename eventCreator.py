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
#This function will redefine event dictionary and run a method to place it in calendar
#Then debug this to let me know that event has been created

def create(start, end, summary, description, zone):
  event = {
      "summary": summary,
      "description": description,
      "start": {
          "dateTime": start,
          "timeZone": "UTC" # will change to make it variable later, for now assume in UTC
        },

      "end": {
          "dateTime": end,
          "timeZone": "UTC" # will change to make it variable later, for now assume in UTC

        },
      'recurrence': [
  'RRULE:FREQ=DAILY;COUNT=1'
        ]
    }
  
  quickstart.main()
  event = quickstart.service.events().insert(calendarId='primary', body=event).execute()
  print ('Event created: %s' % (event.get('htmlLink')))

  
start = datetime.datetime.now()
end = start + timedelta(hours= 1)
#ISO format converts the datetime format and converst to ISO8601 format
start = start.isoformat()
end = end.isoformat()

#test to give start and end time of event before creating it in calendar
print(start)
print(end)
create(start, end,  summary = "hello world,", description= "This is a test", zone = None)