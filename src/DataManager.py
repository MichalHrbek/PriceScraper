import csv, os, glob

PROPS = [
	"timestamp",
	"store",
	"id",
	"name",
	"url",
	"category",
	"price",
	"unit_price",
	"unit_type",
]

CONV = {
	"id": int,
	"price": float,
	"timestamp": int,
	"unit_price": float,
}

CSV_CONF = {
	"quoting": csv.QUOTE_MINIMAL,
	"delimiter": ",",
	"dialect": "unix",
}

def check_existence(record):
	os.makedirs(get_foldername(record["store"]), exist_ok=True)
	if not os.path.exists(get_filename(record["store"],record["id"])):
		with open(get_filename(record["store"],record["id"]), "x", newline='') as f:
			f.write(CSV_CONF["delimiter"].join(PROPS) + "\n")

def make_record(record):
	return get_diff(record, get_last_state(record["store"],record["id"]))

def get_filename(id, store):
	if os.path.commonprefix((os.path.realpath(f"out/{id}/{store}.csv"),os.path.realpath(f"out/"))) != os.path.realpath(f"out/"):
		raise Exception("Illegal path")
	return f"out/{id}/{store}.csv"

def get_foldername(store):
	return f"out/{store}"

def get_diff(a,b):
	o = {i:None for i in PROPS}

	for i in PROPS:
		if (i not in a) or (i not in b) or (b[i] == a[i]):
			o[i] = None
		else:
			o[i] = a[i]
	
	return o

def type_parse(record):
	o = record.copy()
	for i in CONV:
		if type(o[i]) == str:
			o[i] = CONV[i](o[i])
	return o

def get_last_state(store, id):
	with open(get_filename(store,id), "r", newline='') as f:
		reader = csv.DictReader(f, **CSV_CONF)
		o = {i:None for i in PROPS}

		for row in reader:
			for i in PROPS:
				if row[i] != "":
					o[i] = row[i]

		return type_parse(o)

def append_record(record):
	check_existence(record)
	with open(get_filename(record["store"],record["id"]), "a", newline='') as f:
		writer = csv.DictWriter(f, fieldnames=PROPS, **CSV_CONF)
		d = make_record(record)
		writer.writerow(d)

def append_multiple_records(records):
	check_existence(records[0])
	with open(get_filename(records[0]["store"],records[0]["id"]), "a", newline='') as f:
		writer = csv.DictWriter(f, fieldnames=PROPS, **CSV_CONF)
		last = {i:None for i in PROPS}
		for record in sorted(records, key=lambda x: x["timestamp"]):
			o = get_diff(record,last)
			last = record
			writer.writerow(o)

def get_timeline(store, id):
	records = []
	with open(get_filename(store,id), "r", newline='') as f:
		reader = csv.DictReader(f, **CSV_CONF)
		o = {i:None for i in PROPS}

		for row in reader:
			for i in PROPS:
				if row[i] != "":
					o[i] = row[i]
			records.append(type_parse(o))
	return records

def get_current_all():
	files = glob.glob("out/*/*.csv")
	items = []
	for i in files:
		id = int(i.split("/")[-1][:-4])
		store = i.split("/")[-2]
		items.append(get_last_state(store, id))
	return items

def get_start_all():
	files = glob.glob("out/*/*.csv")
	items = []
	for i in files:
		with open(i, "r", newline='') as f:
			reader = csv.DictReader(f, **CSV_CONF)
			items.append(next(reader))
	return items

def get_timeline_all():
	files = glob.glob("out/*/*.csv")
	items = {}
	for i in files:
		id = int(i.split("/")[-1][:-4])
		store = i.split("/")[-2]
		items[str(id)] = get_timeline(store, id)
	return items