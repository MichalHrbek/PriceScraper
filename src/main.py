from ScraperTesco import ScraperTesco
from ScraperBilla import ScraperBilla
from ScraperAlbert import ScraperAlbert
import json, time, os, gzip, traceback
from utils.graph.data import start, end, commit, addItem, addMultipleItems, addMultipleRecords

SCRAPERS = [ScraperBilla] # Takes about 8 minutes to complete on my system

if not os.path.exists("out"):
	os.makedirs("out")

start()

for s in SCRAPERS:
	start_time = time.time()
	file_name = f"out/{int(start_time)}.{s.__name__}"

	try:
		print(s.__name__)
		x = [i.toDict() for i in s.scrape()]
		print("a")
		print(int(time.time() - start_time), "seconds")
		print("b")
		addMultipleItems(x)
		print("c")
		commit()
		print("d")	

	except Exception as e:
		print(traceback.format_exc())
		with open(file_name + ".error", 'w') as f:
			f.write(traceback.format_exc())

end()