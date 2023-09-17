from ItemBase import ItemBase

class ItemTesco(ItemBase):
	id: int
	unit_price: float
	unit_type: str
	weight: float
	def __init__(self, item) -> None:
		self.id = item["id"] # https://nakup.itesco.cz/groceries/cs-CZ/products/{id}
		self.name = item["title"]
		self.category = item["departmentName"]
		self.price = item["price"]
		self.unit_price = item["unitPrice"]
		self.unit_type = item["unitOfMeasure"]
		self.weight = item["averageWeight"]
		self.store = "tesco"