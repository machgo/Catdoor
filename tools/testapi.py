import datetime
import logging
import requests
import json

class testApi:
    def __init__(self):
        self.lastDoorState = False
        # self.serverurl = "http://rancherapp.home.balou.in/api/"
        self.serverurl = "http://localhost:8080/api/"

    def getDoorLockState(self):
        headers = {'content-type': 'application/json'}

        try:
            r = requests.get(self.serverurl+"door", timeout=2.0, headers=headers)
            obj = r.json()
            self.lastDoorState = obj['unlocked']

            return obj['unlocked']

        except requests.exceptions.RequestException as e:
            return self.lastDoorState


    def writeLog(self, message, eventNumber=0):
        payload = {"sender": "core","name": message}
        headers = {'content-type': 'application/json'}

        print(payload)

        try:
            r = requests.post(self.serverurl+"events", timeout=2.0, data=json.dumps(payload), headers=headers)
            obj = r.json()
            return obj['_id']
        except requests.exceptions.RequestException as e:
            print(e)

    def uploadImage(self, filePath):

        id = self.writeLog("New Picture") 
        print(id)

        with open(filePath, "rb") as f:
            byte = f.read()

        try:
            r = requests.post(self.serverurl+"uploads/"+id, timeout=2.0, data=byte, headers={'Content-Type': 'application/octet-stream'})
        except requests.exceptions.RequestException as e:
            print (e)

api = testApi()
ret = api.getDoorLockState()
print(ret)

# api.writeLog("testtt",23)

api.uploadImage("C:\\downloads\\animal.png")
