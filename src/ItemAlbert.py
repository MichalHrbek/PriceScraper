from ItemBase import ItemBase
import datetime

class ItemAlbert(ItemBase):
	def __init__(self, item, category, timestamp:int=None) -> None:
		self.name = item["name"]
		self.category = category
		# This seems to always get the correct price, even when there is no discount
		# Unfortuanetly it is only available in the formatted version, e.g. "1.099,00 Kč"
		try:
			self.price = float(item["price"]["discountedPriceFormatted"].split()[0].replace('.','').replace(',','.'))
		except:
			# print("Failed to parse the price. Falling back to price.value")
			self.price = item["price"]["value"] 
		self.store = "albert"
		self.id = int(item["url"].split("/")[-1])
		self.url = "https://www.albert.cz" + item["url"] # The url can also just be https://www.albert.cz/p/{id} without the slug
		self.timestamp = int(datetime.datetime.now().timestamp()) if timestamp == None else timestamp
		if item["price"]["supplementaryPriceLabel1"] != None:
			s = item["price"]["supplementaryPriceLabel1"].split()
			self.unit_price = float(s[3].replace(",", "."))
			self.unit_type = s[1]