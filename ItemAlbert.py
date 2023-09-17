from ItemBase import ItemBase

class ItemAlbert(ItemBase):
	url: str # https://www.albertdomuzdarma.cz{url}
	price_label: str
	net_content: str
	def __init__(self, item, category: str) -> None:
		self.name = item["name"]
		self.category = category
		self.price = item["price"]["value"]
		self.price_label = item["price"]["supplementaryPriceLabel1"]
		self.store = "albert"
		self.url = item["url"]