import json
f = open('./enviro.json')
data = json.load(f)
print(data['BOT_TOKEN'])