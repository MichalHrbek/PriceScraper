from graph.data import *
import sys, glob, json
import tqdm

# Moves the data from json to the sql database

start()
filepaths = []
for i in sys.argv[1:]:
	for j in glob.glob(i):
		filepaths.append(j)

db: dict[str,list[dict]] = defaultdict(list)
for i in filepaths:
	for j in json.loads(open(i).read()):
		if j["store"] == "albert":
			j["url"] = "https://www.albert.cz" + j["id"]
			j["id"] = int(j["id"].split("/")[-1])
		elif j["store"] == "billa":
			j["url"] = "https://shop.billa.cz/produkt/" + j["id"]
			j["id"] = int(j["id"].split("-")[-1])
		elif j["store"] == "tesco":
			j["url"] = "https://nakup.itesco.cz/groceries/cs-CZ/products/" + j["id"]
			j["id"] = int(j["id"])
		db[j["id"]].append(j)

CONV = {
	"name":"Name",
	"category":"Category",
	"price":"Price",
	"store":"Shop",
	"id":"Id",
	"timestamp":"RecordTimeStamp",
	"unit_price":"UnitPrice",
	"unit_type":"UnitType",
	"url":"Url",
}

for i in tqdm.tqdm(db):
	addMultiple([{CONV[a]:o[a] for a in o if a in CONV} for o in db[i]])

end()