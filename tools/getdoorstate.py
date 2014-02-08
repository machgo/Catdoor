import requests
import json

headers = {'content-type': 'application/json'}

try:
	r = requests.get("http://marcows.home.balou.in:9321/DoorService/Door", timeout=1.0, headers=headers)
	obj = r.json()
	if obj['Unlocked']:
		print "is unlocked"

except requests.exceptions.RequestException as e:
	print e

