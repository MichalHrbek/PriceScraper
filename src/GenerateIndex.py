import json, glob, linecache
from DataManager import get_current_all, PROPS

def item_to_str(item) -> str:
	return f'{item["name"]}, {item["price"]} CZK, {item["store"]}'

def item_to_path(item) -> str:
	return f'{item["store"]}/{item["id"]}.csv'

def generate_index_json():
	c = get_current_all()
	d = {}
	d["items"] = {item_to_path(i): {"name": item_to_str(i), "store": i["store"]} for i in c}
	d["stores"] = [i.split("/")[1] for i in glob.glob("out/*/")]
	d["stores"].remove("error")
	with open("out/index.json", "w") as f:
		f.write(json.dumps(d))

def generate_index_csv():
	stores = glob.glob("out/*/")
	stores.remove("out/error/")
	with open("out/index.csv", "w") as f:
		f.write(','.join(PROPS) + "\n")
		for i in stores:
			for j in glob.glob(i + "*"):
				f.write(linecache.getline(j, 2))

if __name__ == "__main__":
	generate_index_json()