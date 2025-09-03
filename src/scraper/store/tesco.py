from scraper.scraper import Scraper
from scraper.item import Item
import requests
from tqdm import tqdm
from data_manager import append_record
from datetime import datetime
import base64
import urllib.parse
import logging

HEADERS = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
	"Accept": "application/json",
	"content-type": "application/json",
	"region": "CZ",
	"language": "cs-CZ",
	"x-apikey": "TvOSZJHlEk0pjniDGQFAc9Q59WGAR4dA",
}

ENDPOINT = "https://xapi.tesco.com/"

TAXONOMY_QUERY = """query Taxonomy($storeId: ID, $includeInspirationEvents: Boolean = false) {
  taxonomy(
    storeId: $storeId
    includeInspirationEvents: $includeInspirationEvents
  ) {
    name
  }
}
"""

CATEGORY_PRODUCTS_QUERY = """query GetCategoryProducts(
  $page: Int = 1,
  $count: Int,
  $sortBy: String,
  $offset: Int,
  $facet: ID
) {
  category(
    page: $page
    count: $count
    sortBy: $sortBy
    offset: $offset
    facet: $facet
  ) {
    pageInformation: info {
      total
      count
      offset
    }
    results {
      node {
        ... on ProductInterface {
          id
          title
          departmentName
          sellers(type: TOP, limit: 1) {
            results {
              price {
                actual
                unitPrice
                unitOfMeasure
              }
            }
          }
        }
      }
    }
  }
}
"""

class ScraperTesco(Scraper): # Scan takes 300s
	def __init__(self):
		self.logger = logging.getLogger(__name__)

	def scrape(self):
		self.logger.info("Starting")
		taxonomy = requests.post(ENDPOINT, json={
			"operationName": "Taxonomy",
			"query": TAXONOMY_QUERY
		}, headers=HEADERS).json()
		categories = [i["name"] for i in taxonomy["data"]["taxonomy"] if i["name"] != "Výběr týdne"] # Skipping "Výběr týdne" for better performance since it only contains products already present in other categories
		recorded_ids: set[int] = set() # To avoid duplicates
		for i in tqdm(categories, desc=__name__):
			page = 1

			while True:
				resp = requests.post(ENDPOINT, json={
					"operationName": "GetCategoryProducts",
					"query": CATEGORY_PRODUCTS_QUERY,
					"variables": {
						"count": 48, # Can be higher
						"page": page,
						"facet": "b;" + base64.b64encode(urllib.parse.quote(i).encode()).decode(),
					}
				}, headers=HEADERS)
				data = resp.json()
				count = data["data"]["category"]["pageInformation"]["count"]
				offset = data["data"]["category"]["pageInformation"]["offset"]
				total = data["data"]["category"]["pageInformation"]["total"]
				# print(i, page, count, offset, total)
				if count == 0 or count + offset >= total:
					break
				if resp.ok:
					for node in data["data"]["category"]["results"]:
						if int(node["node"]["id"]) not in recorded_ids:
							append_record(ScraperTesco.parse_item(node["node"]).__dict__)
							recorded_ids.add(int(node["node"]["id"]))
				else:
					self.logger.error(f"Problem with request at [{resp.url}]:\n{resp.text}")
				
				page += 1
	
	def parse_item(item, timestamp:int=None) -> Item:
		i = Item()
		i.name = item["title"]
		i.category = item["departmentName"]
		i.price = item["sellers"]["results"][0]["price"]["actual"]
		i.store = "tesco"
		i.id = int(item["id"])
		i.url = "https://nakup.itesco.cz/groceries/cs-CZ/products/" + str(item["id"])
		i.timestamp = int(datetime.now().timestamp()) if timestamp == None else timestamp
		i.unit_price = item["sellers"]["results"][0]["price"]["unitPrice"]
		i.unit_type = item["sellers"]["results"][0]["price"]["unitOfMeasure"]
		return i