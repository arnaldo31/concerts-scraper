import requests
from bs4 import BeautifulSoup
from settings import logging_config
import json
log_error,log_info = logging_config.configure_logging(__file__)

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

save = []
def crwal():
    
    response = requests.get('https://www.stengade.dk/',headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    
    events = soup.find(class_='eventlist eventlist--upcoming').find_all('article')

    for item in events:
        url = 'https://www.stengade.dk' + item.a.get('href')
        while True:
            try:
                response = requests.get(url,headers=headers,timeout=10)
                response.encoding = 'utf-8'
                break
            except requests.exceptions.Timeout:
                continue
            except requests.exceptions.ConnectionError:
                continue
        soup = BeautifulSoup(response.text,'lxml')
        dic = {}
        dic['title'] = soup.title.text
        for script in soup.find_all('script',attrs={'type':'application/ld+json'}):
            try:
                string = script.text
            except:
                continue
            if 'startDate' in string:
                json_str = json.loads(string)
                startDate = json_str['startDate'].replace('+','.')
                endDate = json_str['endDate'].replace('+','.')
            
        dic['monthlySchedule'] = {
            'startDate':startDate,
            'endDate':endDate
        }
        dic['openingHours'] = startDate.split('T')[1][:5]
        image = soup.find(attrs={'itemprop':'image'}).get('content')
        dic['photos'] = [
            {'provider':image}
        ]
        try:
            body = soup.find(class_='eventitem-column-content').find(class_='sqs-html-content').get_text('\n',strip=True)
        except:
            body = ''
        dic['body'] = body
        tags = soup.find(class_='eventitem-meta-item eventitem-meta-tags event-meta-item')
        if tags == None:
            continue
        genre = tags.a.text.lower().replace(' ','/')
        dic['genre'] = genre
        buttons = soup.find_all(attrs={'data-button-size':True})
        ticket = url
        if buttons != []:
            for button in buttons:
                if 'buy tickets' in button.text:
                    ticket = button.a.get('href')

        dic['url'] = ticket

        #--------------------------------
        dic['postType'] = 'Music'
        dic['channel'] = '@public'
        dic['parent'] = 'ROOT'
        dic['address'] = ''
        dic['locationLatitude'] = '55.68819'
        dic['locationLongitude'] = '12.55569509999998'
        
        print('www.stengade.dk | ',dic['title'])
        save.append(dic)

def run():
    try:
        crwal()
        log_info()
    except Exception as e:
        log_error(e)


    return save

