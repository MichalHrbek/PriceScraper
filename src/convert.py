from data_manager import *
import sys, glob, json
import tqdm
import os
from collections import defaultdict

# Converts from the old format to .csv
if __name__ == "__main__":
	filepaths = []
	for i in sys.argv[1:]:
		for j in glob.glob(i):
			filepaths.append(j)

	db: dict[str,list[dict]] = defaultdict(list)
	for i in filepaths:
		for j in json.loads(open(i, encoding='utf-8').read()):
			if j["store"] == "albert":
				j["url"] = "https://www.albert.cz" + j["id"]
				j["id"] = int(j["id"].split(os.path.sep)[-1])
				if j["unit_label"] != None:
					s = j["unit_label"].split()
					j["unit_price"] = float(s[3].replace(",", "."))
					j["unit_type"] = s[1]
			elif j["store"] == "billa":
				j["url"] = "https://shop.billa.cz/produkt/" + j["id"]
				j["id"] = int(j["id"].split("-")[-1])
			elif j["store"] == "tesco":
				j["url"] = "https://nakup.itesco.cz/groceries/cs-CZ/products/" + j["id"]
				j["id"] = int(j["id"])
			for k in PROPS:
				if k not in j:
					j[k] = None
			db[j["id"]].append(j)

	for i in tqdm.tqdm(db):
		append_multiple_records([{a:o[a] for a in o if a in PROPS} for o in db[i]])