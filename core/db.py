import datetime
import logging
import requests
import json


class catdoorDB:
    def __init__(self):
        self.lastDoorState = False
        self.serverurl = "http://rancherapp.home.balou.in:3203/api/"

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

