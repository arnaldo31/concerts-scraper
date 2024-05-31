import requests
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import time
from settings import logging_config

log_error,log_info = logging_config.configure_logging(__file__)

save = []

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
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
}

def translate(word):
    
    while True:
        params = {
            'q':word,
            'key':'AIzaSyBbAo3SShaeAiBAzYUdHEMc_-Oc_uL-wAg',
            'target':'da'
        }
        url = 'https://translation.googleapis.com/language/translate/v2'

        res = requests.post(url,params=params)
        
        data = res.json()
        error = data.get('error')
        if error != None:
            print('errorrrr')
            continue
        else:
            return data['data']['translations'][0]['translatedText']

def parse(url:str,dic:dict):
    #url = 'https://www.hotelcecil.dk/datoer/martinnorgaard'
    #url = 'https://www.hotelcecil.dk/datoer/tomas-hoffding-2'
    #url = 'https://www.hotelcecil.dk/datoer/crack-cloud-can'
    #url = 'https://www.hotelcecil.dk/datoer/claus-hempler-8'
    while True:
        try:
            res = requests.get(url,headers=headers,timeout=5)
            break
        except requests.exceptions.ConnectionError:
            continue
        except requests.exceptions.Timeout:
            continue
        
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')
    
    desk = soup.find(class_='event-page-description')
    dic['body'] = ''
    if desk != None:
        desk = desk.get_text('\n',strip=True)
        dic['body'] = desk
    
    ticket_bottom = soup.find(class_='ticket-info-buttom')
    time = '19:00'
    try:
        if ticket_bottom != None:
            ticket_lines = ticket_bottom.find_all(class_='h3-alternative lines')
            for tic in ticket_lines:
                if 'Koncert' in tic.text or 'DÃ¸rene' in tic.text:
                    concert_info = translate(word=tic.text).lower()
                    #print(concert_info)
                    if 'doors open at' in concert_info:
                        half = concert_info.split('doors open at')[1]
                        if 'p.m.' in half:
                            time = half.replace('p.m.','PM')
                        elif 'a.m.' in half:
                            time = half.replace('a.m.','PM')
                        else:
                            time = half.split('.')[0]
                            time = time + ':00'
                    if 'doors at' in concert_info:
                        half = concert_info.split('doors at')[1]
                        if 'p.m.' in concert_info:
                            time = half.replace('p.m.','PM')
                        elif 'a.m.' in concert_info:
                            time = half.replace('a.m.','PM')
                        else:
                            time = half.split('.')[0]
                            time = time + ':00'
    except:
        time = '19:00'

    time = time.replace('.00.',':00').strip()
    dic['openingHours'] = time
    event_tag = soup.find(class_='ticket-info-top')
    genre = ''
    if event_tag != None:
        try:
            genre = event_tag.find_all(class_='event-tag no-padding')[-1].text
        except:
            pass
    
    dic['genre'] = genre
    
    if 'JAZZ' in genre:
        genre = 'jazz'
        dic['genre'] = genre
    if 'CECIL' in genre:
        genre = 'electronic'
        dic['genre'] = genre
    if 'Koncert' in genre:
        genre = 'rock/pop'
        dic['genre'] = genre
    
    return dic

def parse1(card:dict):
    dic = {}
    title = card.find(class_='h2').text.strip()
    dic['title'] = title
    date = card.find(class_='event-tag-dato').text 
    parts = date.split('.')
    day = parts[0]
    if len(day) == 1:
        day = '0'+day
    month = parts[1]
    if len(month) == 1:
        month = '0'+month
    year = parts[2]
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
    try:
        image = card.find(class_='image-event-2').get('src')
        photos = [{'provider':image}]
        dic['photos'] = photos
    except:
        return None

    link = 'https://www.hotelcecil.dk' + card.find(class_='h2').get('href')
    ticket = card.find(class_='button-secondary small').a.get('href')
    if 'www' not in ticket:
        dic['url'] = link
    else:
        dic['url'] = ticket
    
    dic = parse(url=link,dic=dic)
    dic['postType'] = 'MUSIC'
    dic['address'] = 'Hotel Cecil'
    dic['locationLatitude'] = 55.679460185700734
    dic['locationLongitude'] =  12.57759959176165
    dic['parent'] = 'ROOT'
    dic['channel'] = '@public'
    if dic['genre'] == '':
        return None
    text = 'www.hotelcecil.dk | ' + dic['title']
    print(text)
    save.append(dic)
        
def scraper():
        
    response = requests.get('https://www.hotelcecil.dk/',headers=headers)
    soup = BeautifulSoup(response.text,'lxml')
    
    cards = soup.find_all(class_='forside-kalender-item w-dyn-item')
    links2 = []
    x = 5
    for i in range(0,len(cards),x):
        links2.append(cards[i:i+x])
        
    for links3 in links2:
        start_time = time.time()    
        threads = []
        for item in links3:
            th = threading.Thread(target=parse1, args=(item,))   
            th.start()
            threads.append(th) 

        for th in threads:
            th.join() # Main thread wait for threads finish

def run():
    try:
        scraper()
        log_info()
    except Exception as e:
        log_error(e)
    return save