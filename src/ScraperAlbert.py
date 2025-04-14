from Scraper import Scraper
from Item import Item
import requests
from tqdm import tqdm
from math import ceil
from DataManager import append_record
import traceback
from datetime import datetime

class ScraperAlbert(Scraper): # Scan takes 150s
	def scrape():
		categories = requests.get('https://www.albert.cz/api/v1/?operationName=LeftHandNavigationBar&variables={"rootCategoryCode":"","cutOffLevel":"1","lang":"cs"}&extensions={"persistedQuery":{"version":1,"sha256Hash":"29a05b50daa7ab7686d28bf2340457e2a31e1a9e4d79db611fcee435536ee01c"}}').json()["data"]["leftHandNavigationBar"]["levelInfo"]
		for i in tqdm(categories):
			category_name = i["name"]
			category_url = i["url"].split('/')[2]
			for j in range(ceil(i["productCount"]/50)):
				# I have no idea how persistedQuery works. Some hash is required but you can still change the search parameters. There's no query param to hash so idk where to get the hash
				resp = requests.get('https://www.albert.cz/api/v1/?operationName=GetCategoryProductSearch&variables={"lang":"cs",' + f'"category":"{i["code"]}","pageNumber":{j},' + '"includeSponsoredProducts":false,"pageSize":20,"filterFlag":true,"plainChildCategories":true}&extensions={"persistedQuery":{"version":1,"sha256Hash":"73df954a408a1d92f799c2b1b9dc0e40ae4bcbb74e363138503343bfc7951768"}}')
				if not resp.ok:
					raise Exception(f"Problem with request at [{resp.url}]:\n{resp.text}")
				try:
					json = resp.json()
					for k in json["data"]["categoryProductSearch"]["products"]:
						if category_url == k["url"].split('/')[2]: # This is to exclude duplicates. Tell me if you know of a better way to do this
							append_record(ScraperAlbert.parse_item(k, category_name).__dict__)
				except Exception as e:
					raise Exception(f"Invalid response at [{resp.url}]:\n{resp.text}\nException:\n{traceback.format_exc()}")
	
	def parse_item(item, category, timestamp:int=None) -> Item:
		i = Item()
		i.name = item["name"]
		i.category = category
		# This seems to always get the correct price, even when there is no discount
		# Unfortuanetly it is only available in the formatted version, e.g. "1.099,00 Kč"
		try:
			i.price = float(item["price"]["discountedPriceFormatted"].split()[0].replace('.','').replace(',','.'))
		except:
			# print("Failed to parse the price. Falling back to price.value")
			i.price = item["price"]["value"] 
		i.store = "albert"
		i.id = int(item["url"].split("/")[-1])
		i.url = "https://www.albert.cz" + item["url"] # The url can also just be https://www.albert.cz/p/{id} without the slug
		i.timestamp = int(datetime.now().timestamp()) if timestamp == None else timestamp
		if item["price"]["supplementaryPriceLabel1"] != None:
			s = item["price"]["supplementaryPriceLabel1"].split()
			i.unit_price = float(s[3].replace(",", "."))
			i.unit_type = s[1]
		
		return i