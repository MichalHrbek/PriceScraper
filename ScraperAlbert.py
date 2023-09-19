from ScraperBase import ScraperBase
from ItemAlbert import ItemAlbert
import requests
from tqdm import tqdm
from math import ceil

class ScraperAlbert(ScraperBase): # Scan takes 150s
	def scrape() -> list[ItemAlbert]:
		out_list = []
		# I have no idea how persistedQuery works. Some hash is required but you can still change the search parameters. There's no query param to hash so idk where to get the hash
		gen_url = lambda page_num, page_size: 'https://www.albert.cz/api/v1/?operationName=GetProductSearch&variables={"lang":"cs","searchQuery":"","pageNumber":' + str(page_num) + ',"pageSize":' + str(page_size) + '}&extensions={"persistedQuery":{"version":1,"sha256Hash":"eb2c35d17a491cfbbffd34a91ed26d79a27cbc808fd4849c6edbefe679983718"}}'
		
		try:
			pages = ceil(requests.get(gen_url(0, 1)).json()["data"]["productSearch"]["pagination"]["totalResults"]/50)
			for i in tqdm(range(pages)):
				for j in requests.get(gen_url(i, 50)).json()["data"]["productSearch"]["products"]:
					out_list.append(ItemAlbert(j))
		except KeyboardInterrupt:
			pass

		return out_list
