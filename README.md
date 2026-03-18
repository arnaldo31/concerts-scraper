# Concerts Scraper

This script scrapes concert information from multiple websites and saves the results as structured JSON data.

---

## 🚀 Technologies Used
- Python
- JSON

---

## 📦 Libraries Used
- `beautifulsoup4`
- `lxml`
- `requests`
- `aiohttp`

---

## ⚙️ Installation

### 1. Install Python
Make sure Python is installed on your system.

👉 Download: https://www.python.org/downloads/  
✔ أثناء التثبيت (during installation), check **"Add Python to PATH"**

---

### 2. Install Required Packages

Open your command prompt (CMD) and run:

```bash
pip install requests
pip install beautifulsoup4
pip install lxml
pip install aiohttp
```

---

### 3. Download the Repository

Download the project from GitHub:

```bash
git clone https://github.com/arnaldo31/concerts-scraper.git
```

Or download ZIP manually and extract it.

---

### 4. Navigate to Project Folder

```bash
cd concerts-scraper
```

---

## 🌐 Concert Websites Sources

The scraper collects concert/event data from the following websites:

- https://amagerbio.dk/
- https://culture-box.com/events/
- https://www.drkoncerthuset.dk
- https://www.hotelcecil.dk
- https://www.jazzhusmontmartre.dk/en/koncerter
- https://www.lafontaine.dk/koncerter/
- https://livejazz.dk/
- https://www.loppen.dk/
- https://pumpehuset.dk/
- https://rust.dk/

---

## ▶️ How to Use

1. Open terminal / command prompt  
2. Run the main script:

```bash
python main.py
```

3. Wait for scraping to complete  
4. Output will be saved automatically  

---

## 📁 Output

- All scraped data is stored in:

```
savefiles/
```

- File format:

```
save_YYMMDD.json
```

### Example:
```
save_240531.json
```

---

## 📂 Project Structure

```
concerts-scraper/
│
├── scrapers/               # Individual website scrapers
│   ├── amagerbio.py
│   ├── rust.py
│   └── ...
│
├── savefiles/              # Output JSON files
│
├── scraper.log             # Logs (errors + activity)
│
├── main.py                 # Main execution script
│
└── README.md               # Documentation
```

---

## 🧠 How It Works

1. `main.py` loads all scraper modules from the `scrapers/` folder  
2. Each scraper:
   - Sends HTTP requests  
   - Parses HTML using BeautifulSoup  
   - Extracts concert data  
3. Data is combined into a single JSON structure  
4. Saved into `savefiles/` directory  
5. Logs are written to `scraper.log`

---

## 📝 Logging

All scraping activity, including errors, is stored in:

```
scraper.log
```

Use this file to debug failed scrapers or site structure changes.

---

## ⚠️ Notes

- Some websites may:
  - Block scraping (Cloudflare / bot protection)
  - Require JavaScript rendering (Playwright may be needed)
- Proxies or headers may be required for stability
- Always respect website terms of service

---

## 🔧 Future Improvements

- Add Playwright support for JS-heavy sites  
- Add proxy rotation  
- Add scheduling (cron / cloud jobs)  
- Add database storage (MongoDB / PostgreSQL)  
- Add API layer for serving scraped data  

---

## 👨‍💻 Author

Built for scalable concert/event scraping using Python.

---

## ⭐ Support

If you find this useful, consider giving the repo a star ⭐
