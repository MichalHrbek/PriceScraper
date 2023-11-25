import sqlite3
from collections import defaultdict
from contextlib import closing

opened: bool = False
connection: sqlite3.Connection = None

def start():
	global opened, connection
	if not opened:
		print("Opening")
		connection = sqlite3.connect("db/Items.db")
		connection.row_factory = sqlite3.Row
		opened = True

def end():
	global opened, connection
	if opened:
		print("Closing")
		connection.close()
		opened = False

def create():
	start()
	with open("db/Items.sql") as f:
		with closing(connection.cursor()) as cur:
			cur.execute(f.read())
	end()
		

def getConnection() -> sqlite3.Connection:
	if opened:
		return connection
	return None

PROPS = ["Id","RecordTimeStamp","Price","Name","Shop","Category","UnitPrice","UnitType","Url"]

def getItemRecords(id: int):
	with closing(connection.cursor()) as cur:
		cur.execute("""
					SELECT * from Items
					WHERE Id=(?)
					ORDER BY RecordTimeStamp ASC;
					""", (id,))
		return cur.fetchall()

def getItemList(id: int):
	l = []
	with closing(connection.cursor()) as cur:
		rec = getItemRecords(id)
		o = {}
		for i in rec:
			for j in range(len(PROPS)):
				if i[j] != None:
					o[PROPS[j]] = i[j]
			l.append(o.copy())
	return l

def getItemLast(id: int):
	return getItemList(id)[-1]

def addItem(item):
	with closing(connection.cursor()) as cur:
		last = getItemLast()
		o = defaultdict(lambda: None)
		o["Id"] = item["Id"]
		for i in item:
			if (item[i] != last[i]):
				o[i] = item[i]
		cur.execute("""
					INSERT INTO Items (Id,RecordTimeStamp,Price,Name,Shop,Category,UnitPrice,UnitType,Url)
					VALUES (:Id,:RecordTimeStamp,:Price,:Name,:Shop,:Category,:UnitPrice,:UnitType,:Url);
					""", item)
		connection.commit()

def addMultiple(items):
	with closing(connection.cursor()) as cur:
		items.sort(key=lambda i: i["RecordTimeStamp"])
		last = getItemLast(items[0]["Id"])
		for i in items:
			o = defaultdict(lambda: None)
			o["Id"] = i["Id"]
			for a in i:
				if (i[a] != last[a]):
					o[a] = i[a]
					last[a] = i[a]
			cur.execute("""
				INSERT INTO Items (Id,RecordTimeStamp,Price,Name,Shop,Category,UnitPrice,UnitType,Url)
				VALUES (:Id,:RecordTimeStamp,:Price,:Name,:Shop,:Category,:UnitPrice,:UnitType,:Url);
				""", o)
		connection.commit()

def getAllItems():
	with closing(connection.cursor()) as cur:
		cur.execute("SELECT Id, Name, Price, Shop, MIN(RecordTimeStamp) FROM Items GROUP BY Id;")
		items = cur.fetchall()
		return items