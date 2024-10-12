import json,os,sys

sys.path.append(os.getcwd() + "/src")
from DataManager import get_current_all


def item_to_str(item) -> str:
	return f'{item["name"]}, {item["price"]} CZK, {item["store"]}'

def item_to_id(item) -> str:
	return f'{item["store"]};{item["id"]}'

def item_to_path(item) -> str:
	return f'{item["store"]}/{item["id"]}.csv'

def on_server_loaded(server_context):
	print("Loading...")
	os.makedirs("src/utils/graph/static/", exist_ok=True)
	c = get_current_all()
	with open("src/utils/graph/static/items.json", "w") as f:
		f.write(json.dumps({item_to_id(i): item_to_str(i) for i in c}))
	with open("out/index.json", "w") as f:
		f.write(json.dumps({item_to_path(i): item_to_str(i) for i in c}))
	print("Done")

if __name__ == "__main__":
	on_server_loaded(None)