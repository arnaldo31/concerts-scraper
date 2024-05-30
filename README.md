# Concerts scraper from different websites

This script will scrape concert info from different kinds of website and save results as json file.

## Technologies Used
- Python
- JSON

## Installation
1. You will need to have [Python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) installed (on Mac they are already installed)
2. You will need to install the following packages with `pip`:
   go to `cmd` and type each of this line
   
    - Windows commands:
      ```
      python -m pip install requests
      python -m pip install beautifulsoup4
      python -m pip install lxml
      ```
3. download the code - https://github.com/arnaldo31/kscdirect_scraper/archive/refs/heads/main.zip

## How to Use
1. Open folder where this project is saved on your local machine
   
2. Set up Code filter inside script.
   ```python
   UserName = 'VOOMSU'
   PassWord = 'Voomi1234$'
   crawler_speed = 10 # Default is 10 scrape per 5 seconds. change this to 10 + will increase scraping.
   max_page = 999999 # you can change on how many pages you like to scrape for each category Default is 999999.

4. Run the `kscdirect_scraper.py`
5. Wait the script to finish.

## Location of savefile
  - `save_product` folder with csv save complete product details
  - `save_with_price` folder csv save with price and id 

## Filename
kscdirect_products_category_{`category`}_{`date`}.csv
