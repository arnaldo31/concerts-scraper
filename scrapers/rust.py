import requests
from bs4 import BeautifulSoup
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

headers1 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.upwork.com/',
    'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
}

def scrape():
    
    res = requests.get('https://rust.dk/',headers=headers1)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')

    articles = soup.find(id='events').find_all('article')

    for article in articles:
        title = article.find(class_='event-title').text.strip()
        dic = {}
        startdate = article.find(attrs={'itemprop':'startDate'}).get('content')
        if ' ' in startdate:
            startdate = startdate.split(' ')[0].strip()
        doorTime = article.find(attrs={'itemprop':'doorTime'}).get('content')
        if '00:00' in doorTime:
            if ':' in article.find(attrs={'itemprop':'startDate'}).get('content'):
                doorTime = article.find(attrs={'itemprop':'startDate'}).get('content').split(' ')[1].strip()
            else:
                continue
        description = article.find(attrs={'itemprop':'description'}).get_text('\n',strip=True)
        try:
            img = article.img.get('src')
        except:
            continue
        

        dic['title'] = title
        dic['openingHours'] = doorTime
        dic['url'] = 'https://rust.dk'
        dic['body'] = description
        dic['photos'] = []
        dic['photos'].append({'provider':img})
        dic['genre'] = ''
        
        try:
            ticket_link = article.find(class_='event-ticket-link mvm').get('href')
            dic['url'] = ticket_link
        except:
            ticket_link = ''

        if 'billetto' in ticket_link:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
            }
        
            res = requests.get(ticket_link.replace('/select',''),headers=headers)
            soup = BeautifulSoup(res.text,'lxml')
            category = soup.find_all(class_='text-white focus:ring')
            dic['genre'] = category[-1].text

        if 'ticketmaster' in ticket_link:
            url = "https://app.ticketmaster.com/discovery/v2/events"

            # Parameters to be sent in the query string
            params = {
                "apikey": "2A4kyZtGfV9gHvZuPth8AINThJFG6zyU",
                "keyword": title,
                "locale": "*"
            }

            # Make the GET request
            response = requests.get(url, params=params)
            try:
                event = response.json()['_embedded']['events'][0]
                classifications = event.get('classifications')[0]
                dic['genre'] = classifications.get('genre')['name']
            except Exception as e:
                dic['genre'] = ''

        
        formatted_date = f"{startdate[:4]}-{startdate[4:6]}-{startdate[6:]}"
        doorTime = doorTime.strip()
        dic['startDate'] = f'{formatted_date}T{doorTime}:00.000Z'
        dic['endDate'] = dic['startDate']
        dic['monthlySchedule'] = {
            'startDate':dic.get('startDate',''),
            'endDate':dic.get('endDate','')
        }
        dic['postType'] = 'Music'
        dic['parent'] = 'ROOT'
        dic['channel'] = '@public'
        dic['locationLatitude'] = 55.69121
        dic['locationLongitude'] = 12.55929
        dic['address'] = 'RUST'
        
        try:
            del dic['startDate']
        except:
            pass
        try:
            del dic['endDate']
        except:
            pass

        print('www.rust.dk | ',dic['title'])
        if dic['genre'] == '':
            continue
        
        dic['genre'] = dic['genre'].lower().replace(' ','')
        title = ' completed - ' + dic['title']
        logging.info(title)
        save.append(dic)

def run():
    
    filename = __file__.split('\\')[-1]
    logging.info("-" * 113)
    logging.info(f" Starting  - ({filename}) scraper")

    try:
        scrape()
        logging.info(f" completed - total: {len(save)}")
    except Exception as e:
        error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        logging.info("-" * 113)
        logging.error(f"An error occurred: (scrapers\\{filename})\n%s", error_message)
        logging.error("-" * 113)

    return save

