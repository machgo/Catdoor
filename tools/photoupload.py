import requests
import json

# payload = {"EventNumber":123,"Message":"adasfsdasgf","Title":"sdfajsfajsdlfkskldf"}
# headers = {'content-type': 'application/json'}
# r = requests.post("http://localhost:9321/DoorService/LogEntries", data=json.dumps(payload), headers=headers)



def UploadImage (filePath):
	f = open (filePath, "rb")
	data = f.read();
	UU = data.encode("base64")
	
	payload = {"FileName": filePath,"Data": UU}

	headers = {'content-type': 'application/json'}

	try:
		r = requests.post("http://marcows.home.balou.in:9321/DoorService/Pictures", timeout=1.0, data=json.dumps(payload), headers=headers)
	except requests.exceptions.RequestException as e:
		print e



UploadImage ("/opt/catdoor/camera/old/58214a46-9021-11e3-8486-b827eba401c5.jpg")