from scraper.tesco import ScraperTesco
from scraper.billa import ScraperBilla
from scraper.albert import ScraperAlbert
import time, os, traceback

SCRAPERS = [ScraperAlbert, ScraperTesco, ScraperBilla] # Takes about 8 minutes to complete on my system

os.makedirs("out", exist_ok=True)
os.makedirs("out/error", exist_ok=True)	

for s in SCRAPERS:
	start_time = time.time()

	try:
		print(s.__name__)
		s.scrape()
		print(int(time.time() - start_time), "seconds")
	
	except KeyboardInterrupt:
		print("Skipped after", int(time.time() - start_time), "seconds")

	except Exception as e:
		print(traceback.format_exc())
		with open(f"out/error/{int(start_time)}.{s.__name__}.txt", 'w', encoding="utf-8") as f:
			f.write(traceback.format_exc())