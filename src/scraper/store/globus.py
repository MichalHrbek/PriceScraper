from scraper.scraper import Scraper
from scraper.item import Item
import requests
from tqdm import tqdm
from math import ceil
from data_manager import append_record
from datetime import datetime
from typing import Optional
import logging

class ScraperGlobus(Scraper):
	def __init__(self):
		self.logger = logging.getLogger(__name__)
	
	def scrape(self) -> None:
		self.logger.info("Starting")

		
	
	def parse_item(self, item, timestamp:int=None) -> Optional[Item]:
		i = Item()
		i.timestamp = int(datetime.now().timestamp()) if timestamp == None else timestamp
		return i
