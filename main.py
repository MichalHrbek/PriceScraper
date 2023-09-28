from ScraperTesco import ScraperTesco
from ScraperBilla import ScraperBilla
from ScraperAlbert import ScraperAlbert
import json, time, os, gzip

COMPRESS = True
SCRAPERS = [ScraperAlbert, ScraperTesco, ScraperBilla] # Takes about 8 minutes to complete on my system

if not os.path.exists("out"):
	os.makedirs("out")

for s in SCRAPERS:
	start_time = time.time()
	file_name = f"out/{int(start_time)}.{s.__name__}"

	try:
		print(s.__name__)
		x = [i.__dict__ for i in s.scrape()]
		print(int(time.time() - start_time), "seconds")

		with (gzip.open(file_name + ".json.gz", 'wb') if COMPRESS else open(file_name + ".json", 'wb')) as f:
			f.write(json.dumps(x, ensure_ascii=False, indent="	").encode())

	except Exception as e:
		print(e)
		with open(file_name + ".error", 'w') as f:
			f.write(str(e))