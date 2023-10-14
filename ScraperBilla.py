from ScraperBase import ScraperBase
from ItemBilla import ItemBilla
import requests
from tqdm import tqdm
from math import ceil

class ScraperBilla(ScraperBase): # Scan takes 30s
	def scrape() -> list[ItemBilla]:
		out_list = []

		try:
			total = ceil(requests.get("https://shop.billa.cz/api/products?pageSize=0").json()["total"]/500)
			for i in tqdm(range(total)):
				resp = requests.get("https://shop.billa.cz/api/products?pageSize=500&page=" + str(i)).json()

				if "results" not in resp:
					raise Exception(f"Error on URL https://shop.billa.cz/api/products?pageSize=500&page={i}\n{resp}")

				for j in resp["results"]:
					out_list.append(ItemBilla(j))
		except KeyboardInterrupt:
			pass

		return out_list
