from scraper.scraper import Scraper
from scraper.item import Item
import requests
from tqdm import tqdm
from math import ceil
from data_manager import append_record
from datetime import datetime
from typing import Optional
import logging
from base64 import b64encode

SEARCH_QUERY = """query SearchProductsQuery(
	$search: String!,
	$pageSize: Int,
	$endCursor: String!,
	$userIdentifier: Uuid!
) {
	productsSearch(
		first: $pageSize
		after: $endCursor
		searchInput: {
			search: $search, 
			userIdentifier: $userIdentifier
		}
	
	) {
		totalCount
		pageInfo {
			hasNextPage
		}

		edges {
			node {
				id
				catalogNumber
				name
				fullName
				slug
				
				categories {
					name
				}
				
				# Prices are strings with 6 decimal places.
				price {
					priceWithVat
					baseComparisonPrice
					baseComparisonSaleUnitSizeText
				}
			}
		}
	}
}"""

# This is used to get the totalCount for pagination.
INIT_QUERY = """query SearchProductsQuery(
	$search: String!,
	$pageSize: Int,
	$userIdentifier: Uuid!
) {
	productsSearch(
		first: $pageSize
		searchInput: {
			search: $search, 
			userIdentifier: $userIdentifier
		}
	
	) {
		totalCount
		pageInfo {
			hasNextPage
		}
	}
}"""

class ScraperGlobus(Scraper):
	def __init__(self):
		self.logger = logging.getLogger(__name__)
	
	def scrape(self) -> None: # FIXME: This method hits a 10k products limit. The L1 category sweep might be neccesary instead of this.
		self.logger.info("Starting")

		query_data = {
			"operationName": "SearchProductsQuery",
			"query": INIT_QUERY,
			"variables": {
				"endCursor": "", # b64e(b'arrayconnection:{100*i-1}')
				"pageSize": 100, # This is max allowed
				"search": "",
				"userIdentifier": "00000000-0000-0000-0000-000000000000"
			}
		}

		r = requests.post("https://globusonline.cz/graphql/SearchProductsQuery", json=query_data)
		init_data = r.json()
		total = init_data["data"]["productsSearch"]["totalCount"]

		query_data["query"] = SEARCH_QUERY

		for i in tqdm(range(ceil(total/100))):
			r = requests.post("https://globusonline.cz/graphql/SearchProductsQuery", json=query_data)
			data = r.json()
			
			for j in data["data"]["productsSearch"]["edges"]:
				parsed = ScraperGlobus.parse_item(j["node"])
				if parsed:
					append_record(parsed.__dict__)
				
			query_data["variables"]["endCursor"] = b64encode(f"arrayconnection:{(i+1)*100-1}".encode()).decode()
			if not data["data"]["productsSearch"]["pageInfo"]["hasNextPage"]:
				break

	def parse_item(item: dict, timestamp:int=None) -> Optional[Item]:
		i = Item()
		i.name = item["fullName"]
		i.category = item["categories"][0]["name"] # TODO: Nejak z toho vybrat nejvic high level kategorii? Mozna to uz je serazeny
		i.price = float(item["price"]["priceWithVat"])
		i.store = "globus"
		i.id = int(item["catalogNumber"])
		i.timestamp = int(datetime.now().timestamp()) if timestamp == None else timestamp
		# Some items don't have a unit price. Could be left null, or manually set as 1pc-{normal price}.
		if item["price"]["baseComparisonPrice"] != None:
			i.unit_price = float(item["price"]["baseComparisonPrice"])
		if item["price"]["baseComparisonSaleUnitSizeText"] != None:
			i.unit_type = item["price"]["baseComparisonSaleUnitSizeText"]
		i.url = "https://globusonline.cz" + item["slug"]
		return i
