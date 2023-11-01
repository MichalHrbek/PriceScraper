from ItemBase import ItemBase
import datetime

class ItemAlbert(ItemBase):
	unit_label: str
	ammount: str
	net_content: str
	def __init__(self, item, category, timestamp:int=None) -> None:
		self.name = item["name"]
		self.category = category
		self.price = item["price"]["value"]
		self.store = "albert"
		self.id = item["url"] # https://www.albert.cz{id}
		self.timestamp = int(datetime.datetime.now().timestamp()) if timestamp == None else timestamp
		self.unit_label = item["price"]["supplementaryPriceLabel1"]
		self.ammount = item["price"]["supplementaryPriceLabel2"]