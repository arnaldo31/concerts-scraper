from scrapers  import pumpehuset,hotelcecil,culturebox,loppen,rust,stengade ## this is the 1st barch 5 website 
from datetime import datetime
import json
import codecs

savefile = []

def save():
    current_date = datetime.now().strftime('%Y%m%d')
    with codecs.open(f'.\\savefiles\\save_{current_date}.json', 'w', encoding='utf-8') as f:
        json.dump({'posts': savefile}, f, ensure_ascii=False, indent=4)
        
def crawler():
    
    # data = rust.run()
    # savefile.extend(data)
    
    # data = hotelcecil.run()
    # savefile.extend(data)
    
    # data = culturebox.run()
    # savefile.extend(data)
    
    # data = loppen.run()
    # savefile.extend(data)
    
    # data = pumpehuset.run()
    # savefile.extend(data)
    
    data = stengade.run()
    savefile.extend(data)

if __name__ == '__main__':
    crawler()
    save()