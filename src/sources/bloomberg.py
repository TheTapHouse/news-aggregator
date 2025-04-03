from utils import make_request, make_json, make_soup
from config import URLS
from datetime import datetime

def fetch() -> list:
    r = make_request(URLS['bloomberg'])
    data = make_soup(r.text, parser='xml')
    items = data.find_all('item')

    response = []
    for item in items:
        try:
            headline = item.find('title').text
            url = item.find('link').text
            thumbnail = item.find('media:content')['url']
            desc = item.find('description').text
            time_str = item.find('pubDate').text.replace('GMT', '+0000')
            t = datetime.strptime(time_str, '%a, %d %b %Y %H:%M:%S %z')
        except Exception as e:
            print(f'[BLOOMBERG] Error: {e}')
            continue
            
        response.append({
            'source': 'Bloomberg',
            'headline': headline,
            'url': url,
            'thumbnail': thumbnail,
            'description': desc,
            'time': t,
        })

    return response