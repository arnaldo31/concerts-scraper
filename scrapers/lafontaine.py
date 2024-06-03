import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import traceback
import json
import html

today = datetime.today()
date_save = today.strftime("%Y-%m-%d")
logging.basicConfig(filename='scraper.log',level=logging.INFO,
                    encoding='utf-8',
                    format='%(asctime)s : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

save = []

def crawl():
    
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

    response = requests.get('https://www.lafontaine.dk/koncerter/', headers=headers)
    response.encoding = 'utf-8'
    print(response.status_code)
    soup = BeautifulSoup(response.text,'lxml')
    div = soup.find('script',attrs={'type':'application/ld+json'}).string.strip()
    div = json.loads(div)
    dynamicResults = div
    h3 = soup.find_all('h3')
    for data in dynamicResults:
        dic = {}
        dic['title'] = html.unescape(data['name'])
        image = data['image']
        dic['photos'] = [{'provider':image}]
        desk = ''
        try:
            for h3_tag in h3:
                if dic['title'] in h3_tag.text:
                    body_div = h3_tag.parent.parent.find(class_='tribe-events-calendar-list__event-description tribe-common-b2 tribe-common-a11y-hidden').contents 
                    for b in body_div:
                        if b.name == 'p':
                            desk += b.get_text('\n',strip=True) + '\n'
                        if b.name == 'ul':
                            for li in b.find_all('li'):
                                desk += ' - ' + li.text.strip() + '\n'
        except:
            pass
                            
        dic['body'] = desk
        if dic['body'] == '':
            try:
                dic['body'] = BeautifulSoup(data['description'],'lxml').text
            except:
                dic['body'] = ''

        startDate = data['startDate'].split('+')[0] + '.000Z'
        endDate = data['endDate'].split('+')[0] + '.000Z'
        try:date = datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S.%fZ")
        except:continue
        dic['monthlySchedule'] = {
            "startDate": startDate, 
            "endDate": endDate
        }
        doorOpen = date.strftime("%H:%M")
        dic['openingHours'] = doorOpen
        dic['genre'] = 'jazz'

        try:
            ticket = data['offers']['url']
        except:
            ticket = ''
        if ticket == '' or ticket == None:
            ticket = 'https://www.lafontaine.dk/koncerter/' 
            
        dic['url'] = ticket
        dic.update({
                'postType': 'Music',
                'channel': '@public',
                'parent': 'ROOT',
                'address': 'La Fontaine Jazz',
                'locationLatitude': 55.67752926127099,
                'locationLongitude': 12.576135398084217
            })

        text = 'www.drkoncerthuset.dk | ' + dic['title']
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

