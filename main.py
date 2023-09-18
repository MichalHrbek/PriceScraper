from ScraperTesco import ScraperTesco
from ScraperBilla import ScraperBilla
from ScraperAlbert import ScraperAlbert
import json, time, os

if not os.path.exists("out"):
	os.makedirs("out")

scrapers = [ScraperAlbert, ScraperTesco, ScraperBilla] # Takes about 8 minutes to complete on my system

for s in scrapers:
	print(s.__name__)
	start_time = time.time()
	x = [i.__dict__ for i in s.scrape()]
	print(int(time.time() - start_time), "seconds")

	with open(f"out/{int(start_time)}.{s.__name__}.json", 'w') as f:
		f.write(json.dumps(x, ensure_ascii=False, indent="	"))