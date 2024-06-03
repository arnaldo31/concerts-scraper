import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import traceback


today = datetime.today()
date_save = today.strftime("%Y-%m-%d")
logging.basicConfig(filename='scraper.log',level=logging.INFO,
                    encoding='utf-8',
                    format='%(asctime)s : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

save = []


def crawl():
    
    month_mapping = {
        "Jan": "01", "Feb": "02", "Mar": "03",
        "Apr": "04", "May": "05", "Jun": "06",
        "Jul": "07", "Aug": "08", "Sep": "09",
        "Oct": "10", "Nov": "11", "Dec": "12"
    }
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    }
    response = requests.get('https://amagerbio.dk/', headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    divs = soup.find_all('div',attrs={'data-genres':True})
    
    for data in divs:
        url = data.div.a.get('href')
        dic = {}
        dic['title'] = data.h4.text.strip()
        day = data.find(class_='day').text.strip()
        if len(day) == 1:day = '0'+day
        try:month = month_mapping[data.find(class_='month').text.replace('k','c').strip().title()]
        except:continue
        year = '2024'
        if datetime.now().month > int(month):
            year = str(datetime.now().year + 1)
        
        try:doorOpen = soup.find(class_='time').text.strip()
        except:continue
        startDate = f'{year}-{month}-{day}T{doorOpen}:00.000Z'
        try:date = datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S.%fZ")
        except:continue
        dic['monthlySchedule'] = {
            "startDate": startDate, 
            "endDate": startDate
        }
        doorOpen = date.strftime("%H:%M")
        dic['openingHours'] = doorOpen
        dic['genre'] = data.get('data-genres').replace(' ','/').strip().lower()
        try:category = data.find(class_='venue-label venue-label-xs').text.strip()
        except:continue
        if 'Amager Bio' in category:
            dic.update({
                    'postType': 'Music',
                    'channel': '@public',
                    'parent': 'ROOT',
                    'address': 'Amager Bio',
                    'locationLatitude': 55.658093068230905,
                    'locationLongitude': 12.609159634086259
                })
        if 'Beta' in category:
            dic.update({
                    'postType': 'Music',
                    'channel': '@public',
                    'parent': 'ROOT',
                    'address': 'Beta',
                    'locationLatitude': 55.65803535902243,
                    'locationLongitude': 12.609471933373767
                })

        while True:
            try:
                response = requests.get(url,headers=headers,timeout=10)
                break
            except requests.exceptions.Timeout:
                continue
            except requests.exceptions.ConnectionError:
                continue
        soup = BeautifulSoup(response.text,'lxml')
        body = soup.find(class_='concert')
        if body != None:
            body = body.get_text('\n',strip=True)
            dic['body'] = body
        image = soup.find('div',attrs={'data-lazy-fullres':True})
        if image == None:
            continue
        dic['photos'] = [{'provider':image.get('data-lazy-fullres')}]
        try:
            dic['url'] = data.find(class_='ticket-row').a.get('href')
        except:
            dic['url'] = url
        text = 'amagerbio.dk | ' + dic['title']
        print(text)
        title = ' completed - ' + dic['title']
        logging.info(title)
        save.append(dic)

def run():
    
    filename = __file__.split('\\')[-1]
    logging.info("-" * 113)
    logging.info(f" Starting  - ({filename}) scraper")


    try:
        crawl()
        logging.info(f" completed - total: {len(save)}")
    except Exception as e:
        error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        logging.info("-" * 113)
        logging.error(f"An error occurred: (scrapers\\{filename})\n%s", error_message)
        logging.error("-" * 113)

    return save

