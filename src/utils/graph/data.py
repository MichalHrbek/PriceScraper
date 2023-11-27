import sqlite3
from collections import defaultdict
from contextlib import closing

opened: bool = False
connection: sqlite3.Connection = None

def start():
	global opened, connection
	if not opened:
		print("Opening")
		connection = sqlite3.connect("db/prices.sqlite")
		connection.row_factory = sqlite3.Row
		opened = True

def end():
	global opened, connection
	if opened:
		print("Closing")
		commit()
		connection.close()
		opened = False

def create():
	start()
	
	with closing(connection.cursor()) as cur:
		cur.execute(open("db/Items.sql").read())
		cur.execute(open("db/Records.sql").read())
	end()

def commit():
	if opened:
		connection.commit()

def getConnection() -> sqlite3.Connection:
	if opened:
		return connection
	return None

# PROPS = ["Id","RecordTimeStamp","Price","Name","Shop","Category","UnitPrice","UnitType","Url"]
PROPS = ["Price","Name","Shop","Category","UnitPrice","UnitType","Url"]

def getItemList(id: int):
	raise Exception("Not implemented")
	with closing(connection.cursor()) as cur:
		cur.execute("""
				SELECT * from Items
				WHERE Id=(?)
				ORDER BY RecordTimeStamp DESC;
				""", (id,))
		return cur.fetchall()

# Gets the items state on the last change -> Current info but wrong timestamp
def getItemLastChange(id: int):
	with closing(connection.cursor()) as cur:
		cur.execute("""
				SELECT * FROM Records
				WHERE Id=(?)
				ORDER BY RecordTimeStamp DESC
			  	LIMIT 1;
				""", (id,))
		return cur.fetchone()

# Gets current state and the last timestamp
def getItemLast(id: int):
	with closing(connection.cursor()) as cur:
		cur.execute("""
					SELECT Id, RecordTimeStamp FROM Items
					WHERE Id=(?)
					ORDER BY RecordTimeStamp DESC
					LIMIT 1;""", (id,))
		time = cur.fetchone()["RecordTimeStamp"]
		last = getItemLastChange(id)
		last["RecordTimeStamp"] = time
		return last

def addItem(item):
	with closing(connection.cursor()) as cur:
		item = defaultdict(lambda: None, item)
		last_change = getItemLastChange(item["Id"])
		last = defaultdict(lambda: None) if last_change == None else defaultdict(lambda: None, last_change)
		change = False
		for i in PROPS:
			if last[i] != item[i]:
				change = True
				break
		cur.execute("""
					INSERT INTO Items (Id,RecordTimeStamp,Changed)
					VALUES (?,?,?);
					""", (item["Id"], item["RecordTimeStamp"], change))
		if change:
			cur.execute("""
					INSERT INTO Records (Id,RecordTimeStamp,Price,Name,Shop,Category,UnitPrice,UnitType,Url)
					VALUES (:Id,:RecordTimeStamp,:Price,:Name,:Shop,:Category,:UnitPrice,:UnitType,:Url);
					""", item)

def addMultipleRecords(items):
	with closing(connection.cursor()) as cur:
		items.sort(key=lambda i: i["RecordTimeStamp"])
		last = defaultdict(lambda: None)
		for item in items:
			change = False
			item= defaultdict(lambda: None, item)
			for i in PROPS:
				if last[i] != item[i]:
					change = True
					break
			cur.execute("""
						INSERT INTO Items (Id,RecordTimeStamp,Changed)
						VALUES (?,?,?);
						""", (item["Id"], item["RecordTimeStamp"], change))
			if change:
				cur.execute("""
						INSERT INTO Records (Id,RecordTimeStamp,Price,Name,Shop,Category,UnitPrice,UnitType,Url)
						VALUES (:Id,:RecordTimeStamp,:Price,:Name,:Shop,:Category,:UnitPrice,:UnitType,:Url);
						""", item)
			last = item