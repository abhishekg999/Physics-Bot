import json
import os
import sys

os.system("wget https://www.reddit.com/r/"+ sys.argv[1] + "/top.json -N --output-document=f.json")
with open("f.json", "r") as f:
	file = f.read()
a = json.loads(file)
children = a["data"]["children"]

for child in children:
	if not child["data"]["over_18"]:
		print(child["data"]["title"])
		print(child["data"]["url"])
