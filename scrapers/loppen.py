import requests
from bs4 import BeautifulSoup
from settings import logging_config

log_error,log_info = logging_config.configure_logging(__file__)

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.loppen.dk/genre',
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

save = []

def crawl(link):

    while True:
        try:
            res = requests.get(link,headers=headers,timeout=7)
            break
        except requests.exceptions.Timeout:
            continue
        except requests.exceptions.ConnectionError:
            continue
    
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')
    title = soup.find(attrs={'property':'og:title'}).get('content')
    dic = {}
    dic['title'] = title
    date = soup.find(class_='date-display-single').get('content').replace('+',':')
    startDate = date
    endDate = date
    dic['monthlySchedule'] = {
        "startDate": startDate, 
        "endDate": endDate
    }
    try:
        dic['openingHours'] = date.split('T')[1][:5]
    except:
        dic['openingHours'] = '19:00'
    try:
        image = soup.find(class_='slideshow-item').img.get('src')
    except:
        image = ''
    photos = [{'provider':image}]
    dic['photos'] = photos
    desk = soup.find(class_='text')
    dic['body'] = ''
    if desk != None:
        desk = desk.get_text('\n',strip=True)
    dic['body'] = desk

    return dic
    
def scraper():
    
    res = requests.get('https://www.loppen.dk/',headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')

    cards = soup.find(id='content-area').contents
    
    for card in cards:
        tag = card.name 
        if tag != 'div':
            continue
        
        class_ = card.div.get('class')
        genre = class_[-3]
        if genre == 'Rock':
            genre = class_[-4]
        
        genre = genre.lower().replace('-','/')
        link = card.find(class_='event-link').get('href')
        try:
            dic = crawl(link)
        except:
            continue
        ticket = card.a.get('href')
        dic['url'] = ticket
        dic['genre'] = genre
        dic['address'] = 'Loppen'
        dic['locationLatitude'] = 55.67415971771049
        dic['locationLongitude'] = 12.59732532114244
        dic['parent'] = 'ROOT'
        dic['channel'] = '@public'
        dic['postType'] = 'MUSIC'
        text = 'www.loppen.dk | ' + dic['title']
        print(text)
        save.append(dic)
    
    
def run():
    
    try:
        scraper()
        log_info()
    except Exception as e:
        log_error(e)
        
    return save

