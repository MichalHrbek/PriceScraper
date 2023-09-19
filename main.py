from ScraperTesco import ScraperTesco
from ScraperBilla import ScraperBilla
from ScraperAlbert import ScraperAlbert
import json, time, os, gzip

COMPRESS = False
SCRAPERS = [ScraperAlbert, ScraperTesco, ScraperBilla] # Takes about 8 minutes to complete on my system

if not os.path.exists("out"):
	os.makedirs("out")

for s in SCRAPERS:
	print(s.__name__)
	start_time = time.time()
	x = [i.__dict__ for i in s.scrape()]
	print(int(time.time() - start_time), "seconds")

	with (gzip.open(f"out/{int(start_time)}.{s.__name__}.json.gz", 'wb') if COMPRESS else open(f"out/{int(start_time)}.{s.__name__}.json", 'wb')) as f:
		f.write(json.dumps(x, ensure_ascii=False, indent="	").encode())