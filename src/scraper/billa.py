from scraper import Scraper, Item
import requests
from tqdm import tqdm
from math import ceil
from data_manager import append_record
from datetime import datetime
from typing import Optional

class ScraperBilla(Scraper): # Scan takes 30s
	def scrape():
		total = ceil(requests.get("https://shop.billa.cz/api/products?pageSize=0").json()["total"]/500)
		for i in tqdm(range(total)):
			resp = requests.get("https://shop.billa.cz/api/products?pageSize=500&page=" + str(i)).json()
			
			if "results" not in resp:
				raise Exception(f"Invalid response at [{resp.url}]:\n{resp.text}")
			
			for j in resp["results"]:
				try:
					record = ScraperBilla.parse_item(j)
				except:
					raise Exception(f"Invalid item:\n{j}")
				if record:
					append_record(record.__dict__)
	
	def parse_item(item, timestamp:int=None) -> Optional[Item]:
		if "price" not in item:
			print("Price not available. Skipping")
			return None
		i = Item()
		i.name = item["name"]
		i.category = item["category"]
		i.price = item["price"]["regular"]["value"]/100.0
		i.store = "billa"
		i.id = int(item["slug"].split("-")[-1])
		i.url = "https://shop.billa.cz/produkt/" + item["slug"]
		i.timestamp = int(datetime.now().timestamp()) if timestamp == None else timestamp
		i.unit_price = item["price"]["regular"]["perStandardizedQuantity"]/100.0
		i.unit_type = item["price"]["baseUnitShort"]
		return i