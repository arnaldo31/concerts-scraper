import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from datetime import datetime
import traceback
import pprint

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
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': 'PHPSESSID=6jhc3qfe4qnl7hiovt4n736982; __utma=129850129.1982742045.1723663506.1723663506.1723663506.1; __utmc=129850129; __utmz=129850129.1723663506.1.1.utmcsr=upwork.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=129850129.15.10.1723663506',
    'Referer': 'https://livejazz.dk/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
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
    global genres
    global venues
    
    params = {'url': 'cache/api/genres2.json',}
    response = requests.get('https://livejazz.dk/proxy.php', params=params,headers=headers)
    response.encoding = 'utf-8'
    genres = response.json()
    
    params = {'url': 'cache/api/concerts2.json',}
    response = requests.get('https://livejazz.dk/proxy.php', params=params,headers=headers)
    response.encoding = 'utf-8'
    concerts = response.json()
    
    params = {'url': 'cache/api/venues2.json',}
    response = requests.get('https://livejazz.dk/proxy.php', params=params,headers=headers)
    response.encoding = 'utf-8'
    venues = response.json()
    for item in concerts:
        parse_data(item=item)

def parse_data(item:dict):
    
    dic = {}
    dic['title'] = item['name']
    start = int(item['start'])
    final = int(item['finish'])
    startDate = datetime.utcfromtimestamp(start).strftime('%Y-%m-%dT%H:%M:%S.000000Z')
    start_time = datetime.utcfromtimestamp(start).strftime("%H:%M")
    endDate = datetime.utcfromtimestamp(final).strftime('%Y-%m-%dT%H:%M:%S.000000Z')

    dic['monthlySchedule'] = {
            "startDate": startDate, 
            "endDate": endDate
        }
    dic['openingHours'] = start_time
    
    # genre_list = []
    # for gen in item['genre']:
    #     gen = str(gen)
    #     for gen_item in genres:
    #         if gen == gen_item['id']:
    #             genre_list.append(gen_item['name'])
    
    # if genre_list != []:
    #     dic['genre'] = ','.join(genre_list)
    # else:
    #     dic['genre'] = 'Jazz'
    dic['genre'] = 'Jazz'
    try:
        dic['body'] = item['description']
    except:
        dic['body'] = ''
    
    image = item.get('image','')
    photos = [{'provider':image}]
    dic['photos'] = photos
    
    venueID = item.get('venueID')
    dic['address'] = ''
    for ven in venues:
        if ven['id'] == venueID:
            venue_name = ven.get('name')
            city = ven.get('city')
            #country = ven.get('country')
            addres = ven.get('street')
            full_address = f'{venue_name}, {addres}, {city}'
            dic['address'] = full_address

    ticket = item.get('ticket')
    if ticket == '':
        dic['url'] = 'https://livejazz.dk/concerts/' + item.get('id')
    else:
        dic['url'] = ticket
        
    lat = float(item.get('latitude'))
    dic['locationLatitude'] = lat
    
    long = float(item.get('longitude'))
    dic['locationLongitude'] = long
    dic['parent'] = 'ROOT'
    dic['channel'] = '@public'
    dic['postType'] = 'MUSIC'

    text = 'www.livejazz.dk | ' + dic['title']
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

