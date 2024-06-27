from ScraperBase import ScraperBase
from ItemAlbert import ItemAlbert
import requests
from tqdm import tqdm
from math import ceil
from DataManager import append_record

class ScraperAlbert(ScraperBase): # Scan takes 150s
	def scrape():
		categories = requests.get('https://www.albert.cz/api/v1/?operationName=LeftHandNavigationBar&variables={"rootCategoryCode":"","cutOffLevel":"1","lang":"cs"}&extensions={"persistedQuery":{"version":1,"sha256Hash":"29a05b50daa7ab7686d28bf2340457e2a31e1a9e4d79db611fcee435536ee01c"}}').json()["data"]["leftHandNavigationBar"]["levelInfo"]
		for i in tqdm(categories):
			category_name = i["name"]
			category_url = i["url"].split('/')[2]
			for j in range(ceil(i["productCount"]/50)):
				# I have no idea how persistedQuery works. Some hash is required but you can still change the search parameters. There's no query param to hash so idk where to get the hash
				resp = requests.get('https://www.albert.cz/api/v1/?operationName=GetCategoryProductSearch&variables={"lang":"cs",' + f'"category":"{i["code"]}","pageNumber":{j},' + '"includeSponsoredProducts":false,"pageSize":20,"filterFlag":true,"plainChildCategories":true}&extensions={"persistedQuery":{"version":1,"sha256Hash":"161b8b6137d82243a0dbfeed8477edec6469b84e16b0d00490c1133c57e3f234"}}')
				if not resp.ok:
					raise Exception("Problem with request: " + resp.text)
				resp = resp.json()
				if "data" not in resp:
					raise Exception("Invalid response: " + str(resp))
				for k in resp["data"]["categoryProductSearch"]["products"]:
					if category_url == k["url"].split('/')[2]: # This is to exclude duplicates. Tell me if you know of a better way to do this
						append_record(ItemAlbert(k, category_name).__dict__)