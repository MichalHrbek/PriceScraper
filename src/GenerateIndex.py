import json
from DataManager import get_current_all

def item_to_str(item) -> str:
	return f'{item["name"]}, {item["price"]} CZK, {item["store"]}'

def item_to_path(item) -> str:
	return f'{item["store"]}/{item["id"]}.csv'

def generate_index():
	c = get_current_all()
	with open("out/index.json", "w") as f:
		f.write(json.dumps({item_to_path(i): item_to_str(i) for i in c}))

if __name__ == "__main__":
	generate_index()