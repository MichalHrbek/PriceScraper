from ScraperBase import ScraperBase
from ItemAlbert import ItemAlbert
import requests
from tqdm import tqdm
from math import ceil

class ScraperAlbert(ScraperBase): # Scan takes 150s
	def scrape() -> list[ItemAlbert]:
		categories = requests.get('https://www.albertdomuzdarma.cz/api/v1/?operationName=LeftHandNavigationBar&variables={"rootCategoryCode":"","cutOffLevel":"1","lang":"cs"}&extensions={"persistedQuery":{"version":1,"sha256Hash":"29a05b50daa7ab7686d28bf2340457e2a31e1a9e4d79db611fcee435536ee01c"}}').json()["data"]["leftHandNavigationBar"]["levelInfo"]
		out_list = []
		try:
			for i in tqdm(categories):
				for j in range(ceil(i["productCount"]/50)):
					resp = requests.get('https://www.albertdomuzdarma.cz/api/v1/?operationName=GetCategoryProductSearch&variables={"lang":"cs","category":"' + i["code"] + '","pageNumber":' + str(j) + ',"pageSize":20,"filterFlag":true,"plainChildCategories":true}&extensions={"persistedQuery":{"version":1,"sha256Hash":"65b0b1aacb2caeea6468873e8f7fde0ef82ffb0c4f9c93583c41070fa1f13c82"}}').json()
					for k in resp["data"]["categoryProductSearch"]["products"]:
						out_list.append(ItemAlbert(k, i["name"]))
		except KeyboardInterrupt:
			pass

		return out_list
