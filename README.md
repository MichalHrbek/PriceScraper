# PriceScraper
- Made to scrape prices of big grocery stores in Czechia that have online catalogues (Albert, Billa, Tesco) 

## Usage
- `python3 main.py`
- The program should finish in about 8 minutes depending on your internet connection

## Output
- Output files are stored in the `out` folder in this format: `{time}.{store}.json.gz`
- All stores share these properties: name, price, category, id, timestamp
- Different stores have different properties but they are mostly the unit price and ammount/weight
- Std out shows the progress

## Working with the data
### GUI with mass plotting and search
- `python3 utils/vis.py path`
- Use a unix style path ex. `out/*Albert.json`
- Requires `bokeh`
### A diff tool
- `python3 utils/diff.py file1 file2`
- Requires `deepdiff`

<img src="https://michalhrbek.github.io/images/pricescraper/list.png" width=920>
<img src="https://michalhrbek.github.io/images/pricescraper/graph.png" width=920>
<img src="https://michalhrbek.github.io/images/pricescraper/info.png" width=920>