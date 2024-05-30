# Concerts Scraper

 This script will going to scrape different concerts from diffirent websites and save results as JSON data.

## Technologies Used
- Python
- JSON

## Installation
1. You will need to have [Python](https://www.python.org/downloads/)
   when installing python check the `add to path` check box.
   
2. You will need to install the following packages with `pip`
   go to `cmd` and type each of this line.
   
    - Windows commands:
      ```
      pip install requests
      pip install beautifulsoup4
      pip install lxml
      
      ```
3. download this repository code - https://github.com/arnaldo31/concerts-scraper/archive/refs/heads/main.zip
4. unzip the file if you dont have unzip app download it - https://www.7-zip.org/a/7z2406-x64.exe

## How to Use
1. Open folder where this project is saved on your local machine.
2. Run the `main.py`
3. Wait the script to finish.
4. check the scrape data from `savefiles` folder.

## Files Definitions

- `scrapers`  - All the scripts for each website is located here.
- `logfile.log` - All the logs will be input here including the errors.
- `main.py` - This is the main script that need to run function of this is to run all the code inside `scrapers` folders.
- `savefiles` - All the scraped data will be save here.

## Filename Format is (JSON)
- save_{yy/mm/dd}.json
