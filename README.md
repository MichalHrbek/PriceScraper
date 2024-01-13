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
### GUI with mass plotting and search [[Search]](http://158.101.162.168:8081/graph/static/search.html) [[Example]](http://158.101.162.168:8081/graph?graph&ids[]=/shop/Pekarna-a-cukrarna/Slane-pecivo-volne/Rohliky/Rohlik-mlynarsky-zitny/p/27344064&ids[]=/shop/Pekarna-a-cukrarna/Slane-pecivo-volne/Rohliky/Ceska-chut-Rohlik-klasik-ruzne-druhy/p/26109718&ids[]=/shop/Pekarna-a-cukrarna/Slane-pecivo-volne/Rohliky/Rohlik-anglicky/p/22459466&ids[]=/shop/Pekarna-a-cukrarna/Slane-pecivo-volne/Rohliky/Rohlik/p/20480905&ids[]=turisticky-rohlik-82315094&ids[]=rohlik-82316363&ids[]=zitny-rohlik-s-posypem-82322229&ids[]=2001000151875&ids[]=2001130294293&ids[]=2001130294254&ids[]=2001130898559&ids[]=2001130905057&ids[]=2001130905073&ids[]=2001130907487&ids[]=2001130905063&ids[]=/shop/Pekarna-a-cukrarna/Slane-pecivo-volne/Rohliky/Rohlik-sedmizrnny/p/21976056&ids[]=2001019141652&ids[]=2001130909583)
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