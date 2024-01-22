# PriceScraper
- Made to scrape prices of big grocery stores in Czechia that have online catalogues (Albert, Billa, Tesco) 

## Usage
- `python3 main.py`
- The program should finish in about 8 minutes depending on your internet connection

## Output
- Output files are stored in this format: `out/{store}/{id}.csv`
- Fields that haven't changed from the last datapoint are empty to save space
- All stores share these fields: `name`, `category`, `price`, `store`, `id`, `timestamp`, `unit_price`, `unit_type`, `url`
- Shows the progress while scraping with `tqdm`

## Working with the data
### GUI with mass plotting and search [[Search]](http://158.101.162.168:8081/graph/static/search.html) [[Example]](http://158.101.162.168:8081/graph?graph&ids[]=tesco%3B2001019141652&ids[]=tesco%3B2001130909583&ids[]=tesco%3B2001000151875&ids[]=tesco%3B2001130898559&ids[]=tesco%3B2001130294293&ids[]=tesco%3B2001130907487&ids[]=tesco%3B2001130294254&ids[]=tesco%3B2001130905057&ids[]=tesco%3B2001130905063&ids[]=tesco%3B2001130905073&ids[]=albert%3B20480905&ids[]=albert%3B22459466&ids[]=albert%3B27344064&ids[]=albert%3B26109718&ids[]=albert%3B21976056&ids[]=billa%3B82322229&ids[]=billa%3B82316363&ids[]=billa%3B82315094)
- `python3 utils/vis.py path`
- Use wildcards ex. `out/albert/*.csv`
- Requires `bokeh`

<img src="https://michalhrbek.github.io/images/pricescraper/list.png" width=920>
<img src="https://michalhrbek.github.io/images/pricescraper/bokeh_plot.png" width=920>
<img src="https://michalhrbek.github.io/images/pricescraper/info.png" width=920>

## TODO
### Graph
- Fix legend entries with the same name merging
- Handle overlapping lines better
- Highlight data points
