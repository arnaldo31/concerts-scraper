import requests
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import logging
from datetime import datetime
import traceback

today = datetime.today()
date_save = today.strftime("%Y-%m-%d")
logging.basicConfig(filename='scraper.log',level=logging.INFO,
                    encoding='utf-8',
                    format='%(asctime)s : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

save = []


month_mapping = {
        "Jan": "01", "Feb": "02", "Mar": "03",
        "Apr": "04", "May": "05", "Jun": "06",
        "Jul": "07", "Aug": "08", "Sep": "09",
        "Oct": "10", "Nov": "11", "Dec": "12"
    }

mons = []
def parse(item:dict,category:str):
    dic = {}
    dic['title'] = item['title']
    date_str = item['date'].strip()
    parts = date_str.split()

    try:
        day = parts[0]
        if len(day) == 1:
            day = '0'+day
        month = month_mapping[parts[1]]
        year = parts[2]
    except:
        return None
    date_str = f"{day} {month} {year}"

    try:
        date_obj = datetime.strptime(date_str, "%d %B %Y")
        iso_date_time = date_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        iso_date_time = f'{year}-{month}-{day}T00:00:00.000000Z'

    dic['monthlySchedule'] = {
        "startDate": iso_date_time, 
        "endDate": iso_date_time
    }
    dic['postType'] = 'MUSIC'
    dic['genre'] = item.get('genre','')
    if dic['genre'] == None:
        dic['genre'] = ''
    photos = [{'provider':item.get('image','')}]
    dic['photos'] = photos
    dic['channel'] = '@public'
    
    if category == 'pumpehuset':
        dic['address'] = 'PUMPEHUSET'
        dic['locationLatitude'] = 55.67746
        dic['locationLongitude'] =  12.56490
        
    if category == 'byhaven':
        dic['address'] = 'BYHAVN'
        dic['locationLatitude'] = 55.67708
        dic['locationLongitude'] =  12.56510
    dic['parent'] = 'ROOT'
    link = item.get('link','')
    ticket = item.get('ticket_link','')
    if ticket == '':
        ticket = link
    dic['url'] = ticket
    dic = scraper_obj.crawl(url=link,dic=dic)
    title = dic['title']
    text = 'www.pumpehuset.com | ' + title
    print(text)
    title = ' completed - ' + dic['title']
    logging.info(title)
    save.append(dic)

class scraper:

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'origin': 'https://pumpehuset.dk',
        'priority': 'u=1, i',
        'referer': 'https://pumpehuset.dk/en/program/?genre=all',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    }
    
    def __init__(self) -> None:
        pass
    
    def crawl(self,url:str,dic:dict):
    
        while True:
            try:
                res = requests.get(url,headers=self.headers,timeout=5)
                break
            except requests.exceptions.Timeout:
                continue
            except requests.exceptions.ConnectionError:
                continue
        
        
        res.encoding = 'utf-8'
        
        soup = BeautifulSoup(res.text,'lxml')
        description = soup.find(class_='text__content text__content--large')
        if description != None:
            dic['body'] = description.parent.get_text('\n',strip=True)
        
        try:
            hours_open = soup.find("div", class_="text__button u-text-grey grid uppercase", string=lambda text: "Doors open" in text).find_next('div').text.strip()
        except:
            hours_open = '10.00'
        dic['openingHours'] = hours_open.replace('.',':')
        return dic

    def run(self,category:str):
        
        for i in range(1,99):
            i = str(i)
            data = {
                'action': 'fetch_concerts',
                'searchString': '',
                'searchMonth': 'false',
                'sort': 'concert_date',
                'pageNumber': i,
                'pageAmount': '9',
                'locations': category,
                'genres': 'all',
            }

            while True:
                try:
                    response = requests.post('https://pumpehuset.dk/wp-admin/admin-ajax.php', headers=self.headers, data=data,timeout=5)
                    data = response.json()
                    break
                except requests.exceptions.ConnectionError:
                    continue
                except requests.exceptions.Timeout:
                    continue
                except requests.exceptions.JSONDecodeError:
                    continue
            
            if data == []:
                break
            
            links2 = []
            x = 3
            for i in range(0,len(data),x):
                links2.append(data[i:i+x])
            
            for links3 in links2:
                for item in links3:
                    #start_time = time.time()    
                    threads = []
                    for item in data:
                        th = threading.Thread(target=parse, args=(item,category,))   
                        th.start()
                        threads.append(th) 

                    for th in threads:
                        th.join() # Main thread wait for threads finish
                    #print("multiple threads took ", (time.time() - start_time), " seconds")

scraper_obj = scraper()
category = ['pumpehuset','byhaven']

def run():

    filename = __file__.split('\\')[-1]
    logging.info("-" * 113)
    logging.info(f" Starting  - ({filename}) scraper")

    try:
        for cat in category:
            scraper_obj.run(category=cat)
        logging.info(f" completed - total: {len(save)}")
    except Exception as e:
        error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        logging.info("-" * 113)
        logging.error(f"An error occurred: (scrapers\\{filename})\n%s", error_message)
        logging.error("-" * 113)

    return save

