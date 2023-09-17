from ScraperBase import ScraperBase
from ItemBilla import ItemBilla
import requests
from tqdm import tqdm
from math import ceil

class ScraperBilla(ScraperBase): # Scan takes 30s
	def scrape() -> list[ItemBilla]:
		total = ceil(requests.get("https://shop.billa.cz/api/products?pageSize=0").json()["total"]/500)
		out_list = []

		try:
			for i in tqdm(range(total)):
				resp = requests.get("https://shop.billa.cz/api/products?pageSize=500&page=" + str(i)).json()

				for j in resp["results"]:
					out_list.append(ItemBilla(j))
		except KeyboardInterrupt:
			pass

		return out_list
