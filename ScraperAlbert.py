from ScraperBase import ScraperBase
from ItemAlbert import ItemAlbert
import requests
from tqdm import tqdm
from math import ceil

class ScraperAlbert(ScraperBase): # Scan takes 150s
	def scrape() -> list[ItemAlbert]:
		out_list = []
		try:
			categories = requests.get('https://www.albert.cz/api/v1/?operationName=LeftHandNavigationBar&variables={"rootCategoryCode":"","cutOffLevel":"1","lang":"cs"}&extensions={"persistedQuery":{"version":1,"sha256Hash":"29a05b50daa7ab7686d28bf2340457e2a31e1a9e4d79db611fcee435536ee01c"}}').json()["data"]["leftHandNavigationBar"]["levelInfo"]
			for i in tqdm(categories):
				category_name = i["url"].split('/')[2]
				for j in range(ceil(i["productCount"]/50)):
					# I have no idea how persistedQuery works. Some hash is required but you can still change the search parameters. There's no query param to hash so idk where to get the hash
					resp = requests.get('https://www.albert.cz/api/v1/?operationName=GetCategoryProductSearch&variables={"lang":"cs","category":"' + i["code"] + '","pageNumber":' + str(j) + ',"pageSize":20,"filterFlag":true,"plainChildCategories":true}&extensions={"persistedQuery":{"version":1,"sha256Hash":"25fdff69c2396b20f500d39cc3e5967a066ee90eb8678e1e264575dfb9433060"}}').json()
					for k in resp["data"]["categoryProductSearch"]["products"]:
						if category_name == k["url"].split('/')[2]: # This is to exclude duplicates (may not work)
							out_list.append(ItemAlbert(k, category_name))
						
		except KeyboardInterrupt:
			pass

		return out_list
