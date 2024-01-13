from ScraperBase import ScraperBase
from ItemBilla import ItemBilla
import requests
from tqdm import tqdm
from math import ceil
from DataManager import append_record

class ScraperBilla(ScraperBase): # Scan takes 30s
	def scrape():
		try:
			total = ceil(requests.get("https://shop.billa.cz/api/products?pageSize=0").json()["total"]/500)
			for i in tqdm(range(total)):
				resp = requests.get("https://shop.billa.cz/api/products?pageSize=500&page=" + str(i)).json()

				if "results" not in resp:
					raise Exception(f"Error on URL https://shop.billa.cz/api/products?pageSize=500&page={i}\n{resp}")

				for j in resp["results"]:
					append_record(ItemBilla(j).__dict__)
		except KeyboardInterrupt:
			pass
