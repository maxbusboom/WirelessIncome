# wireless-income


Comparison of median income to wireless data speeds. 

## Development

Getting started: 

- If on a Mac, run `.devcontainer/setup-mac.sh` to install brew and important features like aws cli and `uv`
- run `.devcontainer/setup-uv-env.sh` to setup the virtual env

### Manual

```
uv venv
uv sync
```

Then in VSCode command bar, select `Python: Select Interpreter` to select the
interpreter in your project .venv dir. 


## Census Data

Use  https://censusreporter.org to find tables, then Google for:

```
census api <table> 
```

To get more information about the Census API for that table. 

## More tract level data

* Neighborhood level data: https://nanda.isr.umich.edu/data/
* Social Vulnerability Index: https://svi.cdc.gov/dataDownloads/data-download.html
* Rural / Urban Codes: https://www.ers.usda.gov/data-products/rural-urban-commuting-area-codes


Internet Access, Social Risk Factors, and Web-Based Social Support Seeking Behavior: Assessing Correlates of the “Digital Divide” Across Neighborhoods in The State of Maryland

https://pmc.ncbi.nlm.nih.gov/articles/PMC8449832/


https://www.fcc.gov/form-477-census-tract-data-internet-access-services
Includes data on residential fixed internet access connections per 1,000 households by census tract for both service over 200 kbps and higher speed tiers.


The data file `src/tract_map_dec_2023.csv` is the FCC form 477 report of the number of providers per tract, to assess internet acess availability. See their [web page for more details](https://www.fcc.gov/form-477-census-tract-data-internet-access-services). 