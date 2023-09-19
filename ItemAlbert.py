from ItemBase import ItemBase

class ItemAlbert(ItemBase):
	url: str # https://www.albert.cz{url}
	unit_label: str
	ammount: str
	net_content: str
	def __init__(self, item, category) -> None:
		self.name = item["name"]
		self.category = category
		self.price = item["price"]["value"]
		self.store = "albert"
		self.unit_label = item["price"]["supplementaryPriceLabel1"]
		self.ammount = item["price"]["supplementaryPriceLabel2"]
		self.url = item["url"]