from ItemBase import ItemBase
import datetime

class ItemBilla(ItemBase):
	def __init__(self, item, timestamp:int=None) -> None:
		self.name = item["name"]
		self.category = item["category"]
		self.price = item["price"]["regular"]["value"]/100.0
		self.store = "billa"
		self.id = int(item["slug"].split("-")[-1])
		self.url = "https://shop.billa.cz/produkt/" + item["slug"]
		self.timestamp = int(datetime.datetime.now().timestamp()) if timestamp == None else timestamp
		self.unit_price = item["price"]["regular"]["perStandardizedQuantity"]/100.0
		self.unit_type = item["price"]["baseUnitShort"]