import json, glob, datetime, data, os

def item_to_str(item: list[dict]) -> str:
	return f'{item[-1]["name"]}, {item[-1]["price"]} CZK, {item[-1]["store"]}, {len(item)}' + ('' if all([i["price"] == item[0]["price"] for i in item]) else ', X')

def on_server_loaded(server_context):
	db = {}
	print("Loading...")
	for i in glob.glob("out/*json"):
		for j in json.loads(open(i).read()):
			j["timestamp"] = datetime.datetime.fromtimestamp(j["timestamp"])
			if j["id"] in db:
				db[j["id"]].append(j)
			else:
				db[j["id"]] = [j]
	data.set(db)
	os.makedirs("utils/graph/static", exist_ok=True)
	with open("utils/graph/static/items.json", "w+") as f:
		f.write(json.dumps({i: item_to_str(db[i]) for i in db}))
	print("Done")
