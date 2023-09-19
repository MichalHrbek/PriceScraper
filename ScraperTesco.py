from ScraperBase import ScraperBase
from ItemTesco import ItemTesco
import requests
from tqdm import tqdm

HEADERS = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
	"Accept": "application/json",
	"content-type": "application/json",
	"x-csrf-token": "fFRGjayy-pQy7h1GjMF2251JkHqF1mOzPr-g",
	"Cookie": "_csrf=DsK3LGi5-4EDpI9Tj9YslMxs;"
}

class ScraperTesco(ScraperBase): # Scan takes 300s
	def scrape() -> list[ItemTesco]:
		out_list = []

		try:
			taxonomy = requests.get("https://nakup.itesco.cz/groceries/cs-CZ/taxonomy", headers=HEADERS).json()
			categories = [i["url"][1:] for i in taxonomy]
			for i in tqdm(categories):
				j = 1

				while True:
					body = {
						"resources": [
							{
								"type": "productsByCategory",
								"params": {
									"query": {
										"include-children": "true",
										"page": str(j),
										"count": str(48)
									},
									"superdepartment": i
								}
							}
						]
					}
					resp =  requests.post("https://nakup.itesco.cz/groceries/cs-CZ/resources", headers=HEADERS, json=body)
					
					if resp.ok:
						item_list = resp.json()["productsByCategory"]["data"]["results"]["productItems"]
						for k in item_list:
							out_list.append(ItemTesco(k["product"]))
					else:
						if resp.text.strip() == "{}":
							break
						else:
							print("error")
						
					
					j += 1
		except KeyboardInterrupt:
			pass

		return out_list