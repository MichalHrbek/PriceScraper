from scraper.scraper import Scraper
from scraper.item import Item
import requests
from tqdm import tqdm
from math import ceil
from data_manager import append_record
import traceback
from datetime import datetime
import urllib.parse
from typing import Any, Tuple, Optional
import json
import logging

PRODUCT_SEARCH_QUERY = 'query GetCategoryProductSearch($lang: String, $searchQuery: String, $pageSize: Int, $pageNumber: Int, $category: String, $sort: String, $filterFlag: Boolean, $plainChildCategories: Boolean, $facetsOnly: Boolean, $fields: String) {\n  categoryProductSearch: categoryProductSearchV2(\n    lang: $lang\n    searchQuery: $searchQuery\n    pageSize: $pageSize\n    pageNumber: $pageNumber\n    category: $category\n    sort: $sort\n    filterFlag: $filterFlag\n    plainChildCategories: $plainChildCategories\n    facetsOnly: $facetsOnly\n    fields: $fields\n  ) {\n    products {\n      ...ProductBlockDetails\n      __typename\n    }\n    breadcrumbs {\n      ...Breadcrumbs\n      __typename\n    }\n    categoryBreadcrumbs {\n      ...CategoryBreadcrumbs\n      __typename\n    }\n    facets {\n      ...Facets\n      __typename\n    }\n    sorts {\n      name\n      selected\n      code\n      __typename\n    }\n    pagination {\n      ...Pagination\n      __typename\n    }\n    currentQuery {\n      query {\n        value\n        __typename\n      }\n      url\n      __typename\n    }\n    categorySearchTree {\n      categoryDataList {\n        categoryCode\n        categoryData {\n          facetData {\n            count\n            name\n            nameNonLocalized\n            query {\n              query {\n                value\n                __typename\n              }\n              url\n              __typename\n            }\n            selected\n            thumbnailUrl\n            __typename\n          }\n          subCategories\n          __typename\n        }\n        __typename\n      }\n      level\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProductBlockDetails on Product {\n  available\n  averageRating\n  numberOfReviews\n  manufacturerName\n  manufacturerSubBrandName\n  code\n  country\n  countryFlagUrl\n  badges {\n    ...ProductBadge\n    __typename\n  }\n  badgeBrand {\n    ...ProductBadge\n    __typename\n  }\n  promoBadges {\n    ...ProductBadge\n    __typename\n  }\n  delivered\n  littleLion\n  firstLevelCategory {\n    code\n    name\n    nameNonLocalized\n    url\n    __typename\n  }\n  freshnessDuration\n  freshnessDurationTipFormatted\n  frozen\n  recyclable\n  images {\n    format\n    imageType\n    url\n    __typename\n  }\n  isBundle\n  isProductWithOnlineExclusivePromo\n  isWine\n  maxOrderQuantity\n  limitedAssortment\n  mobileFees {\n    ...MobileFee\n    __typename\n  }\n  name\n  newProduct\n  onlineExclusive\n  potentialPromotions {\n    ...ProductPromotionFragment\n    __typename\n  }\n  potentialActivatablePromotions {\n    ...ProductPromotionFragment\n    __typename\n  }\n  price {\n    approximatePriceSymbol\n    currencySymbol\n    formattedValue\n    priceType\n    supplementaryPriceLabel1\n    supplementaryPriceLabel2\n    showStrikethroughPrice\n    discountedPriceFormatted\n    discountedUnitPriceFormatted\n    unit\n    unitPriceFormatted\n    unitCode\n    unitPrice\n    value\n    wasPrice\n    __typename\n  }\n  purchasable\n  productPackagingQuantity\n  productProposedPackaging\n  productProposedPackaging2\n  promotionThemes\n  stock {\n    inStock\n    inStockBeforeMaxAdvanceOrderingDate\n    partiallyInStock\n    availableFromDate\n    __typename\n  }\n  url\n  previouslyBought\n  nutriScoreLetter\n  isLowPriceGuarantee\n  isHouseholdBasket\n  isPermanentPriceReduction\n  freeGift\n  plasticFee\n  score\n  bestSellerScore\n  __typename\n}\n\nfragment ProductBadge on ProductBadge {\n  code\n  image {\n    ...Image\n    __typename\n  }\n  tooltipMessage\n  name\n  __typename\n}\n\nfragment Image on Image {\n  altText\n  format\n  galleryIndex\n  imageType\n  url\n  __typename\n}\n\nfragment MobileFee on MobileFee {\n  feeName\n  feeValue\n  __typename\n}\n\nfragment ProductPromotionFragment on Promotion {\n  isMassFlashOffer\n  endDate\n  alternativePromotionMessage\n  alternativePromotionBadge\n  code\n  priceToBurn\n  promotionType\n  pickAndMix\n  qualifyingCount\n  freeCount\n  range\n  redemptionLevel\n  toDisplay\n  description\n  title\n  promoBooster\n  simplePromotionMessage\n  offerType\n  restrictionType\n  priority\n  percentageDiscount\n  onlineOnly\n  promotionTypeCode\n  points\n  __typename\n}\n\nfragment CategoryBreadcrumbs on CategoryBreadcrumb {\n  name\n  url\n  __typename\n}\n\nfragment Breadcrumbs on SearchBreadcrumb {\n  facetCode\n  facetName\n  facetValueName\n  facetValueCode\n  removeQuery {\n    query {\n      value\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Facets on Facet {\n  code\n  name\n  category\n  facetUiType\n  values {\n    code\n    count\n    name\n    query {\n      query {\n        value\n        __typename\n      }\n      __typename\n    }\n    selected\n    __typename\n  }\n  __typename\n}\n\nfragment Pagination on Pagination {\n  currentPage\n  totalResults\n  totalPages\n  sort\n  __typename\n}'
HEADERS = {
	"content-type": "application/json"
}

class ScraperAlbert(Scraper): # Scan takes 150s
	def __init__(self):
		self.logger = logging.getLogger(__name__)

	def build_url(params):
		encoded_params = {}
		for key, value in params.items():
			if isinstance(value, (dict, list)):
				value = json.dumps(value, separators=(',', ':'))
			encoded_params[key] = value
		
		return urllib.parse.urlencode(encoded_params)

	def send_persistent_query(data: dict) -> Tuple[bool, requests.Response, Any]:
		resp = requests.get("https://www.albert.cz/api/v1/?" + ScraperAlbert.build_url(data), headers=HEADERS)
		resp_json = resp.json()
		if "errors" in resp:
			for i in resp["errors"]:
				if i["message"] == "PersistedQueryNotFound":
					return False, resp
		return True, resp, resp_json
	
	def send_query(self, data: dict, query: str) -> Tuple[requests.Response, Any]:
		found, resp, resp_json = ScraperAlbert.send_persistent_query(data)
		if found:
			return resp, resp_json
		self.logger.info("Hash not found. Sending full query.")
		data["query"] = query
		resp = requests.post("https://www.albert.cz/api/v1/", json=data, headers=HEADERS)
		return resp, resp.json()
		
			
	def scrape(self):
		self.logger.info("Starting")
		_, categories_json = self.send_query({
			"operationName": "LeftHandNavigationBar",
			"variables": {
				"rootCategoryCode":"",
				"cutOffLevel":"1",
				"lang":"cs",
			},
			"extensions": {
				"persistedQuery": {
					"version":1,
					"sha256Hash":"29a05b50daa7ab7686d28bf2340457e2a31e1a9e4d79db611fcee435536ee01c"
				}
			}
		}, "query LeftHandNavigationBar($rootCategoryCode: String, $cutOffLevel: String, $lang: String, $topLevelCategoriesToHideIfEmpty: String, $anonymousCartCookie: String) {\n  leftHandNavigationBar(\n    rootCategoryCode: $rootCategoryCode\n    cutOffLevel: $cutOffLevel\n    lang: $lang\n    topLevelCategoriesToHideIfEmpty: $topLevelCategoriesToHideIfEmpty\n    anonymousCartCookie: $anonymousCartCookie\n  ) {\n    categoryTreeList {\n      categoriesInfo {\n        categoryCode\n        levelInfo {\n          ...CategoryFields\n          __typename\n        }\n        __typename\n      }\n      level\n      __typename\n    }\n    levelInfo {\n      ...CategoryFields\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CategoryFields on CategoryLevelInfo {\n  name\n  productCount\n  url\n  code\n  __typename\n}")
		categories = categories_json["data"]["leftHandNavigationBar"]["levelInfo"]
		for i in tqdm(categories, desc=__name__):
			category_name = i["name"]
			category_url = i["url"].split('/')[2]
			for j in range(ceil(i["productCount"]/50)): # TODO: Use the pagination info in the response
				data = {
					"operationName": "GetCategoryProductSearch",
					"variables": {
						"lang": "cs",
						"searchQuery": "",
						"category": i["code"],
						"pageNumber": j,
						"pageSize": 50,
						"filterFlag": True,
						"fields": "PRODUCT_TILE",
						"plainChildCategories": True
					},
					"extensions": {
						"persistedQuery": {
							"version": 1,
							"sha256Hash": "c5bf48545cb429dfbcbdd337dc33dc4c3b82565ec95d29a88113cdb308ea560a"
						}
				}}
				resp, resp_json = self.send_query(data, PRODUCT_SEARCH_QUERY)
				try:
					for k in resp_json["data"]["categoryProductSearch"]["products"]:
						if category_url == k["url"].split('/')[2]: # This is to exclude duplicates. Let me know if you know of a better way to do this
							item = self.parse_item(k, category_name)
							if item:
								append_record(item.__dict__)
				except:
					self.logger.error(f"Invalid response at [{resp.url}]:\n{resp.text}", exc_info=True)
	
	def parse_item(self, item, category, timestamp:int=None) -> Optional[Item]:
		i = Item()
		i.name = item["name"]
		i.category = category
		# This seems to always get the correct price, even when there is no discount
		# Unfortuanetly it is only available in the formatted version, e.g. "1.099,00 Kč"
		try:
			try:
				i.price = float(item["price"]["discountedPriceFormatted"].split()[0].replace('.','').replace(',','.'))
			except:
				i.price = item["price"]["value"] 
				self.logger.info("Failed to parse the price. Falling back to price.value", item["price"])
		except:
			self.logger.info("Price not available. Skipping", item["price"] if "price" in item else "Price not specified")
			return None
		i.store = "albert"
		i.id = int(item["url"].split("/")[-1])
		i.url = "https://www.albert.cz" + item["url"] # The url can also just be https://www.albert.cz/p/{id} without the slug
		i.timestamp = int(datetime.now().timestamp()) if timestamp == None else timestamp
		if item["price"]["supplementaryPriceLabel1"] != None:
			s = item["price"]["supplementaryPriceLabel1"].split()
			i.unit_price = float(s[3].replace(",", "."))
			i.unit_type = s[1]
		
		return i