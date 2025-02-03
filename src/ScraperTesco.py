from Scraper import Scraper
from Item import Item
import requests
from tqdm import tqdm
from DataManager import append_record
from datetime import datetime

HEADERS = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
	"Accept": "application/json",
	"content-type": "application/json",
	"x-csrf-token": "fFRGjayy-pQy7h1GjMF2251JkHqF1mOzPr-g",
	"Cookie": "_csrf=DsK3LGi5-4EDpI9Tj9YslMxs;"
}

class ScraperTesco(Scraper): # Scan takes 300s
	def scrape():
		taxonomy = requests.get("https://nakup.itesco.cz/groceries/cs-CZ/taxonomy", headers=HEADERS).json()
		categories = [i["url"][1:] for i in taxonomy if i["url"] != "/vyber-tydne"] # Skipping "vyber-tydne" for better performance since it only contains products already present in other categories
		recorded_ids: set[int] = set() # To avoid duplicates
		for i in tqdm(categories):
			j = 1

			while True:
				body = {
					"resources": [
						{
							"type": "productsByCategory",
							"params": {
								"query": {
									"include-children": "true",
									"page": str(j),
									"count": str(48)
								},
								"superdepartment": i
							}
						}
					]
				}
				resp =  requests.post("https://nakup.itesco.cz/groceries/cs-CZ/resources", headers=HEADERS, json=body)
				
				if resp.ok:
					item_list = resp.json()["productsByCategory"]["data"]["results"]["productItems"]
					for k in item_list:
						if int(k["product"]["id"]) not in recorded_ids:
							append_record(ScraperTesco.parse_item(k["product"]).__dict__)
							recorded_ids.add(int(k["product"]["id"]))
				else:
					if resp.text.strip() == "{}":
						break
					else:
						raise Exception(f"Problem with request at [{resp.url}]:\n{resp.text}")


				j += 1
	
	def parse_item(item, timestamp:int=None) -> Item:
		i = Item()
		i.name = item["title"]
		i.category = item["departmentName"]
		i.price = item["price"]
		i.store = "tesco"
		i.id = int(item["id"])
		i.url = "https://nakup.itesco.cz/groceries/cs-CZ/products/" + str(item["id"])
		i.timestamp = int(datetime.now().timestamp()) if timestamp == None else timestamp
		i.unit_price = item["unitPrice"]
		i.unit_type = item["unitOfMeasure"]
		return i