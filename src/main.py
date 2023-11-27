from ScraperTesco import ScraperTesco
from ScraperBilla import ScraperBilla
from ScraperAlbert import ScraperAlbert
import json, time, os, gzip, traceback, tqdm
from utils.graph.data import start, end, commit, addItem

SCRAPERS = [ScraperBilla]#, ScraperAlbert, ScraperTesco] # Takes about 8 minutes to complete on my system

if not os.path.exists("out"):
	os.makedirs("out")

start()

for s in SCRAPERS:
	start_time = time.time()
	file_name = f"out/{int(start_time)}.{s.__name__}"

	try:
		print(s.__name__)
		x = [i.toDict() for i in s.scrape()]
		print(int(time.time() - start_time), "seconds scraping")
		for i in tqdm.tqdm(x):
			addItem(i)
		commit()
		print(int(time.time() - start_time), "seconds total")

	except Exception as e:
		print(traceback.format_exc())
		with open(file_name + ".error", 'w') as f:
			f.write(traceback.format_exc())

end()