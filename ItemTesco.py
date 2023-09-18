from ItemBase import ItemBase

class ItemTesco(ItemBase):
	id: int # https://nakup.itesco.cz/groceries/cs-CZ/products/{id}
	unit_price: float
	unit_type: str
	weight: float
	def __init__(self, item) -> None:
		self.name = item["title"]
		self.category = item["departmentName"]
		self.price = item["price"]
		self.store = "tesco"
		self.id = item["id"]
		self.unit_price = item["unitPrice"]
		self.unit_type = item["unitOfMeasure"]
		self.weight = item["averageWeight"]