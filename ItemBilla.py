from ItemBase import ItemBase

class ItemBilla(ItemBase):
	slug: str # https://shop.billa.cz/produkt/{slug}
	unit_price: float
	unit_type: str
	weight: float
	def __init__(self, item) -> None:
		self.slug = item["slug"]
		self.name = item["name"]
		self.category = item["category"]
		self.price = item["price"]["regular"]["value"]/100.0
		self.unit_price = item["price"]["regular"]["perStandardizedQuantity"]/100.0
		self.unit_type = item["price"]["baseUnitShort"]
		self.weight = item["weight"]
		self.store = "billa"