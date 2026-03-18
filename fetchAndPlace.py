import json
import math
import allocateTime
import eventCreator
import quickstart

from collections import deque
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class FeedbackQueue:

    def __init__(self, revisionSpread):
        #revisionSpread is an array containing the amount
        #of hours per subject of the student i.e. revisionSpread[0]
        #is the number of hours going towareds subject 1
        #which is their highest priority subject
        self.revisionSpread = revisionSpread

        #cleaner way of creating queues (in this case 3 in 1)
        self.queues = [deque() for _ in range(3)]
    
    #inner class
    #each of these Slots should have public access
    #lower priority index is a high priority
    class Slot:
        def __init__(self, name, subjectIndex, priority):
            self.name = name
            self.minutesCompleted = 0
            self.subjectIndex = subjectIndex
            self.priority = priority
    
    #put a slot into the feedback queue
    def addSlot(self, slot):
        self.queues[slot.priority].append(slot)
        
    #get the slot that is coming next
    def getNextSlot(self):
        for level in range(3):
            #only return the next slot if it exists
            if self.queues[level]:
                return self.queues[level].popleft()
        #else return null
        return None

##main program

def mapSubjectToIndex(subjectName):
    return subjectMap.get(subjectName, 0)

subjectMap = {
    "Math": 0,
    "FM": 1,
    "Computer Science": 2,
    "Economics": 3
}

#in main program ask from the user and store it
revisionSpread = [5,6,7,5]

#get API services
service = quickstart.service
courses = service.courses.list().execute.get("courses", [])

#init feedback queue
feedbackQueue = FeedbackQueue(revisionSpread)

assignmentsData = []
#geta ll the assignments that are due
for course in courses:
    courseWorkList = service.courses().courseWork().list(courseID = course["id"]).execute().get("courseWork", [])
    
    for work in courseWorkList:
        if "dueDate" not in work:
            continue
    due = work["dueDate"]

    dueDate = datetime(year=due["year"], month =due["month"],day=due["day"])
    
    assignmentsData.append(
        {
            "assignmentName": work["title"],
            "subjectName": course["name"],
            "dueDate": dueDate
        }
    )

#determine the priority by checking the due day
today = datetime.now()
twoDaysFromNow = today + timedelta(days=2)
#shorten the current datetime to just the date
todayTruncated = datetime.date(today.year, today.month, today.day)
#find week beginning by subtracting a number
#of days depending on which weekday it is
weekStart = todayTruncated - timedelta(days = todayTruncated.weekday)
#create a buddy
allocateTime.Buddy(64)

for item in assignmentsData:
    #set high priority level if due in less than 2 days
    if item["dueData"] <= twoDaysFromNow:
        priorityLevel = 0
    else:
        #set to medium priority if not
        priorityLevel = 1
    #create a slot using the information about the current assignment
    slot = feedbackQueue.Slot(
        name=item["assignmentName"],
        subjectIndex=mapSubjectToIndex(item["subjectName"]),
        priority=priorityLevel
    )

    feedbackQueue.addSlot(slot)

#turns anythin in buddy units into aa datetime in iso format
def unitsToDateTime(startUnit, blockUnit, baseDate):

    startMinutes = startUnit * 15
    endMinutes = (startUnit+blockUnit) * 15

    startDateTime = baseDate + timedelta(minutes=startMinutes)
    endDateTime = baseDate + timedelta(minutes=endMinutes)

    return startDateTime.isoformat(), endDateTime.isoformat()

#main loop ofr this file
while True:
    slot = feedbackQueue.getNextSlot()

    if slot is None:
        break

    #Convert weekly hours to minutes
    weeklyMinutes = feedbackQueue.revisionSpread[slot.subjectIndex] * 60

    #Convert to something suitable for the buddy allocator
    requiredUnits = weeklyMinutes // 15

    #put into a buddy
    startUnit, blockUnit = allocateTime.allocate(requiredUnits)
    startTime, endTime = unitsToDateTime(startUnit, blockUnit, weekStart)
    eventCreator.createEvent(startTime, endTime, summary= slot.name, description= slot.subjectIndex)