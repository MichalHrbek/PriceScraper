from ScraperTesco import ScraperTesco
from ScraperBilla import ScraperBilla
from ScraperAlbert import ScraperAlbert
import json, time, os, datetime

def mkdir(path):
	if not os.path.exists(path):
		os.makedirs(path)

date = datetime.datetime.now()
folder = f"out/{date.day}.{date.month}.{date.year}/"

mkdir("out")
mkdir(folder)

scrapers = [ScraperAlbert, ScraperTesco, ScraperBilla] # Takes about 8 minutes to complete on my system

for s in scrapers:
	print(s.__name__)
	start_time = time.time()
	x = [i.__dict__ for i in s.scrape()]
	print(int(time.time() - start_time), "seconds")

	with open(folder + s.__name__ + ".json", 'w') as f:
		f.write(json.dumps(x, ensure_ascii=False, indent="	"))