# PriceScraper
- Made to scrape prices of big grocery stores in Czechia that have online catalogues (Albert, Billa, Tesco) 

## Usage
### Scraping
- `python3 src/main.py`
- scraping takes few minutes (~ 5)

### Web UI
- Generate index of items: `python3 src/generate_index.py`
- Run web server: 
	- (_recommended_) `python3 web/serve.py`
	- `cd web && python3 -m http.server`
- You can download over a year of data scraped everyday at midnight [here](https://prices.kasos.cz/out.tar.gz) or inspect the files [here](https://prices.kasos.cz/data/)

## Output
- Output files: `out/{store}/{id}.csv`, `out/logs/`, `out/error/`
- Fields that haven't changed since the last entry are null, to save space + all changes are easily visible when you inspect the files in a text editor
- All stores share these fields: `name`, `category`, `price`, `store`, `id`, `timestamp`, `unit_price`, `unit_type`, `url`
- Shows the progress while scraping with [tqdm](https://pypi.org/project/tqdm/)

## Web UI [[Search]](https://prices.kasos.cz/) [[Example]](https://prices.kasos.cz/graph.html?ids[]=tesco%2F2001019141652.csv&ids[]=tesco%2F2001130909583.csv&ids[]=tesco%2F2001000151875.csv&ids[]=tesco%2F2001130898559.csv&ids[]=tesco%2F2001130294293.csv&ids[]=tesco%2F2001130907487.csv&ids[]=tesco%2F2001130294254.csv&ids[]=tesco%2F2001130905057.csv&ids[]=tesco%2F2001130905063.csv&ids[]=tesco%2F2001130905073.csv&ids[]=albert%2F20480905.csv&ids[]=albert%2F22459466.csv&ids[]=albert%2F27344064.csv&ids[]=albert%2F26109718.csv&ids[]=albert%2F21976056.csv&ids[]=billa%2F82322229.csv&ids[]=billa%2F82316363.csv&ids[]=billa%2F82315094.csv)

<img src="https://michalhrbek.github.io/images/pricescraper/chartjs_plot.png" width=920>
<img src="https://michalhrbek.github.io/images/pricescraper/search.png" width=920>

## TODO
### Search
- [x] Filter by store
- [x] Button to download selected item as normal csv
### Scraper
- [x] Automatically update albert query hashes
- [x] Improve error logging
- [ ] Scrape the Tesco clubcard price (this is needed to make comparisions make sense, since it is the Tesco equivalent of a discount)
### Data analysis
- [ ] Show interesting statistic (biggest discounts, new items, etc.)
### UI
- [ ] Page for each item
- [ ] Page for each category
