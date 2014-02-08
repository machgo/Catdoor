import datetime
import logging
import requests
import json


class catdoorDB:
    def __init__(self):
        self.lastDoorState = False


    def getDoorLockState(self):
        headers = {'content-type': 'application/json'}

        try:
            r = requests.get("http://echo.home.balou.in:9321/DoorService/Door", timeout=2.0, headers=headers)
            obj = r.json()
            self.lastDoorState = obj['Unlocked']

            return obj['Unlocked']

        except requests.exceptions.RequestException as e:
            return self.lastDoorState


    def writeLog(self, message, eventNumber=0):
        payload = {"Title": "core","Message": message, "EventNumber": eventNumber}
        headers = {'content-type': 'application/json'}

        print payload

        try:
            r = requests.post("http://echo.home.balou.in:9321/DoorService/LogEntries", timeout=2.0, data=json.dumps(payload), headers=headers)
        except requests.exceptions.RequestException as e:
            print e
