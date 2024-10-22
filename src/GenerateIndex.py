import json, glob
from DataManager import get_current_all

def item_to_str(item) -> str:
	return f'{item["name"]}, {item["price"]} CZK, {item["store"]}'

def item_to_path(item) -> str:
	return f'{item["store"]}/{item["id"]}.csv'

def generate_index():
	c = get_current_all()
	d = {}
	d["items"] = {item_to_path(i): {"name": item_to_str(i), "store": i["store"]} for i in c}
	d["stores"] = [i.split("/")[1] for i in glob.glob("out/*/")]
	d["stores"].remove("error")
	with open("out/index.json", "w") as f:
		f.write(json.dumps(d))

if __name__ == "__main__":
	generate_index()