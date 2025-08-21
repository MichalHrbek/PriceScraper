from scraper.store.tesco import ScraperTesco
from scraper.store.billa import ScraperBilla
from scraper.store.albert import ScraperAlbert
import time, os, logging

SCRAPERS = [ScraperAlbert, ScraperTesco, ScraperBilla] # Takes about 8 minutes to complete on my system

def setup_logger():
	log_id = str(int(time.time()))

	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	info_handler = logging.FileHandler(f"out/logs/{log_id}.log", encoding="utf-8")
	info_handler.setLevel(logging.INFO)

	error_handler = logging.FileHandler(f"out/errors/{log_id}.log", encoding="utf-8", delay=True)
	error_handler.setLevel(logging.ERROR)

	debug_handler = logging.StreamHandler()
	debug_handler.setLevel(logging.INFO)

	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	info_handler.setFormatter(formatter)
	error_handler.setFormatter(formatter)
	debug_handler.setFormatter(formatter)

	logger.addHandler(info_handler)
	logger.addHandler(error_handler)
	logger.addHandler(debug_handler)

def main():
	os.makedirs("out", exist_ok=True)
	os.makedirs("out/error", exist_ok=True)
	os.makedirs("out/logs", exist_ok=True)

	setup_logger()

	for i in SCRAPERS:
		start_time = time.time()

		scraper = i()
		try:
			scraper.scrape()
			scraper.logger.info(f"Finnished after {int(time.time() - start_time)} seconds")
		
		except KeyboardInterrupt:
			scraper.logger.info(f"Skipped after {int(time.time() - start_time)} seconds")

		except Exception as e:
			scraper.logger.error(f"Stopped - unhandled exception", exc_info=True)

if __name__ == "__main__":
	main()