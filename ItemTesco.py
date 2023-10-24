from ItemBase import ItemBase
import datetime

class ItemTesco(ItemBase):
	unit_price: float
	unit_type: str
	weight: float
	def __init__(self, item, timestamp:int=None) -> None:
		self.name = item["title"]
		self.category = item["departmentName"]
		self.price = item["price"]
		self.store = "tesco"
		self.id = str(item["id"]) # https://nakup.itesco.cz/groceries/cs-CZ/products/{id}
		self.timestamp = int(datetime.datetime.now().timestamp()) if timestamp == None else timestamp
		self.unit_price = item["unitPrice"]
		self.unit_type = item["unitOfMeasure"]
		self.weight = item["averageWeight"]