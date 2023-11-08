import json, glob, datetime, data

db = {}

def on_server_loaded(server_context):
	for i in glob.glob("out/*json"):
		for j in json.loads(open(i).read()):
			j["timestamp"] = datetime.datetime.fromtimestamp(j["timestamp"])
			if j["id"] in db:
				db[j["id"]].append(j)
			else:
				db[j["id"]] = [j]
	data.set(db)
