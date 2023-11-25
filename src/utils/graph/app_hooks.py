import json, glob, datetime, data, os, gzip

def item_to_str(item) -> str:
	return f'{item["Name"]}, {item["Price"]} CZK, {item["Shop"]}'

def on_server_loaded(server_context):
	print("Loading")
	data.start()
	items = data.getAllItems()
	os.makedirs("src/utils/graph/static", exist_ok=True)
	with open("src/utils/graph/static/items.json", "w+") as f:
		f.write(json.dumps({i["Id"]: item_to_str(i) for i in items}))
	print("Done")

def on_server_unloaded(server_context):
    data.end()