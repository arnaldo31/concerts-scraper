# Concerts Scraper

This script scrapes concert information from different websites and saves the results as JSON data.

## Technologies Used
- Python
- JSON

## Libraries Used
- `beautifulsoup4`
- `lxml`
- `requests`

## Installation

1. **Install Python**
   - You will need to have [Python](https://www.python.org/downloads/) installed.
   - When installing Python, ensure you check the `Add to PATH` checkbox.

2. **Install Required Packages**
   - Open your command prompt (cmd) and type the following commands to install the necessary packages:
     ```
     pip install requests
     pip install beautifulsoup4
     pip install lxml
     ```

3. **Download the Repository**
   - Download this repository's code from [GitHub](https://github.com/arnaldo31/concerts-scraper/archive/refs/heads/main.zip).

4. **Unzip the File**
   - Unzip the downloaded file. If you do not have an unzip application, you can download one [here](https://www.7-zip.org/a/7z2406-x64.exe).

## How to Use

1. Open the folder where this project is saved on your local machine.
2. Run the `main.py` script:
3. Wait for the script to finish.
4. Check the scraped data in the `savefiles` folder.
5. Check the `scraper.log` if there is any error happen during the scraping.

## Files and Directory Structure

- `scrapers/` - Contains individual scripts for scraping each website.
- `scraper.log` - Contains logs of all scrape concert with time, including error messages.
- `main.py` - The main script that executes all code in the `scrapers` folder.
- `savefiles/` - Where all the scraped data is saved.

## Filename Format for Saved Data (JSON)
- `save_YYMMDD.json` (e.g., `save_240531.json` for data saved on May 31, 2024).
