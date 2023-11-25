class ItemBase:
	name: str
	category: str
	price: float
	store: str
	id: int
	timestamp: int
	unit_price: float
	unit_type: str
	url: str

	def __init__(self, data):
		self.name = data["Name"]
		self.category = data["Category"]
		self.price = data["Price"]
		self.store = data["Shop"]
		self.id = data["Id"]
		self.timestamp = data["RecordTimeStamp"]
		self.unit_price = data["UnitPrice"]
		self.unit_type = data["UnitType"]
		self.url = data["Url"]
	
	def toDict(self):
		data = {}
		data["Name"] = self.name
		data["Category"] = self.category
		data["Price"] = self.price
		data["Shop"] = self.store
		data["Id"] = self.id
		data["RecordTimeStamp"] = self.timestamp
		data["UnitPrice"] = self.unit_price
		data["UnitType"] = self.unit_type
		data["Url"] = self.url
		return data