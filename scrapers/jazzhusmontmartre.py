import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import traceback
import json
import html
import base64


today = datetime.today()
date_save = today.strftime("%Y-%m-%d")
logging.basicConfig(filename='scraper.log',level=logging.INFO,
                    encoding='utf-8',
                    format='%(asctime)s : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

save = []

def call_api(authorization,appid):
    current_datetime = datetime.utcnow()
    formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    json_data = {"dataCollectionId":"Koncerter","query":{"filter":{"date":{"$gte":{"$date":formatted_datetime}}},"sort":[{"fieldName":"date","order":"ASC"}],"paging":{"offset":0,"limit":110},"fields":[]},"options":{},"includeReferencedItems":[],"returnTotalCount":True,"environment":"LIVE","appId":appid}
    json_string = json.dumps(json_data)
    encoded_param = base64.b64encode(json_string.encode('utf-8')).decode('utf-8')
    headers = {
        'authorization': authorization,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'Accept': 'application/json, text/plain, */*',
    }
    params = {
        '.r': encoded_param,
    }
    response = requests.get('https://www.jazzhusmontmartre.dk/_api/cloud-data/v2/items/query', params=params, headers=headers)
    return response.json()

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

    response = requests.get('https://www.jazzhusmontmartre.dk/en/koncerter', headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    div = soup.find('script',id='wix-viewer-model').string.strip()
    div = json.loads(div)
    headers = div['siteFeaturesConfigs']['dynamicPages']['prefixToRouterFetchData']['koncerter']['optionsData']['headers']
    Authorization = headers['Authorization']
    appId = headers['x-wix-grid-app-id']
    data_result = call_api(authorization=Authorization,appid=appId)
    
    for data in data_result['dataItems']:
        data = data['data']
        title = html.unescape(data['title']).replace('\n','')
        if 'kl' in title:
            title = title.split('kl')[0]
        dic = {}
        dic['title'] = title
        try:
            image = data['image']
            image = 'https://static.wixstatic.com/media/' + image.split('/v1/')[1].split('/')[0]
            
        except:
            continue
        dic['photos'] = [{'provider':image}]
        dic['body'] = data.get('beskrivelse','')

        startDate = data['date']['$date'].replace('Z','.00Z')
        endDate = startDate
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
            dic['url'] = 'https://www.jazzhusmontmartre.dk/en' + data['link-koncerter-2-title']
        except:
            dic['url'] = 'https://www.jazzhusmontmartre.dk/en'

        dic.update({
                'postType': 'Music',
                'channel': '@public',
                'parent': 'ROOT',
                'address': 'Jazz hus Montmartre',
                'locationLatitude': 55.682087076297876,
                'locationLongitude': 12.582442259194254
            })

        text = 'jazzhusmontmartre.dk | ' + dic['title']
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

