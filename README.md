# PriceScraper
- Made to scrape prices of big grocery stores in Czechia that have online catalogues (Albert, Billa, Tesco) 

## Usage
- `python3 main.py`
- The program should finish in about 8 minutes depending on your internet connection

## Output
- Output files are stored in the `out` folder in this format: `{time}.{store}.json.gz`
- All stores share these properties: name, price, category
- Different stores have different properties but they are mostly id/slug/url and unit price
- Std out shows the progress