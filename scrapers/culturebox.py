import requests
from bs4 import BeautifulSoup
from datetime import datetime
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

def month_name_to_number(month_name):
    # Dictionary mapping month names to their numeric values
    month_mapping = {
        "JANUARY": "01", "FEBRUARY": "02", "MARCH": "03",
        "APRIL": "04", "MAY": "05", "JUNE": "06",
        "JULY": "07", "AUGUST": "08", "SEPTEMBER": "09",
        "OCTOBER": "10", "NOVEMBER": "11", "DECEMBER": "12"
    }
    
    # Convert the input month name to uppercase and return the corresponding value
    return month_mapping.get(month_name.upper(), "Invalid month name")

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.upwork.com/',
    'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
}


def parse(url:str):
    pass

    # dic = {}
    
    # test = 0
    # while True:
    #     #driver.open(url)
    #     if test == 7:
    #         break
    #     try:
    #         #page = driver.page_source
    #         #soup = BeautifulSoup(page,'lxml')
    #         script = soup.find(attrs={'type':'application/ld+json'}).string
    #         break
    #     except AttributeError:
    #         print('AttributeError')
    #         test += 1
    #         continue
    
    # if test == 7:
    #     return None

#     dic['genre'] = 'electronic'
#     script = json.loads(script)
#     title = script['name']
#     dic['title'] = title
#     dic['body'] = script.get('description','')
#     dic['monthlySchedule'] = {
#         "startDate": script.get('startDate','') + 'Z', 
#         "endDate": script.get('endDate','') + 'Z'
#     }
#     dic['url'] = url
#     timeStart = script.get('startDate').split("T")[1].split(".")[0]
#     dic['openingHours'] = timeStart
#     return dic

def crawl():
    
    res = requests.get('https://culture-box.com/events/',headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')
    
    cards = soup.find(class_='post-list').find_all('article')
    links = []
    
    for card in cards:
        links.append(card.a.get('href'))
    
    for url in links:
        res = requests.get(url,headers=headers)
        soup = BeautifulSoup(res.text,'lxml')
        
        Tickets = soup.find('span',string='Tickets')
        if Tickets == None:
            continue
        
        Tickets = Tickets.parent.get('href')
        if 'ra.co' not in Tickets:
            continue
        
        
        image = soup.find(attrs={'property':'og:image'}).get('content')
        h2 = soup.h2.text
        parts = h2.split(' ')
        day = parts[1]
        month = month_name_to_number(parts[2])
        if month == 'Invalid month name':
            continue
        year = parts[3]
        date_str = f"{day} {month} {year}"
        
        try:
            date_obj = datetime.strptime(date_str, "%d %B %Y")
            iso_date_time = date_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            iso_date_time = f'{year}-{month}-{day}T00:00:00.000000Z'
        
        dic = {}
        dic['monthlySchedule'] = {
            "startDate": iso_date_time, 
            "endDate": iso_date_time
        }
        dic['genre'] = 'electronic'
        dic['title'] = 'BLACK BOX - ' + h2
        try:
            dic['body'] = soup.find(class_='post-block__additional-text text-formatting').p.text.strip()
        except:
            dic['body'] = ''
        
        time = soup.find('h3',string='Open').parent.text.replace('Open','').split('–')[0].replace('\n','').strip()
        dic['openingHours'] = time
        dic['url'] = Tickets
        photos = [{'provider':image}]
        dic['photos'] = photos
        dic['address'] = 'Culture Box'
        dic['locationLatitude'] = 55.68662732622199
        dic['locationLongitude'] = 12.584014245701194
        dic['parent'] = 'ROOT'
        dic['channel'] = '@public'
        dic['postType'] = 'MUSIC'
        
        text = 'www.culture-box.com | ' + dic['title']
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
