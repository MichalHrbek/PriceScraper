from ItemBase import ItemBase
import datetime

class ItemTesco(ItemBase):
	def __init__(self, item, timestamp:int=None) -> None:
		self.name = item["title"]
		self.category = item["departmentName"]
		self.price = item["price"]
		self.store = "tesco"
		self.id = int(item["id"])
		self.url = "https://nakup.itesco.cz/groceries/cs-CZ/products/" + str(item["id"])
		self.timestamp = int(datetime.datetime.now().timestamp()) if timestamp == None else timestamp
		self.unit_price = item["unitPrice"]
		self.unit_type = item["unitOfMeasure"]