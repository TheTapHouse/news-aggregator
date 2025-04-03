from utils import make_request, make_json, make_soup
from config import URLS
from datetime import datetime

def fetch() -> list:
    r = make_request(URLS['watcherguru'])
    data = make_soup(r.text, parser='xml')
    items = data.find_all('item')

    response = []
    for item in items:
        try:
            headline = item.find('title').text
            url = item.find('link').text

            try:
                thumbnail = make_soup(item.find('content:encoded').text).find('figure').find('img')['src']
            except:
                continue
            
            desc = item.find_all('description')[0].text
            time_str = item.find('pubDate').text
            t = datetime.strptime(time_str, '%a, %d %b %Y %H:%M:%S %z')
        except Exception as e:
            print(f'[WATCHER.GURU] Error: {e}')
            continue

        response.append({
            'source': 'Watcher.Guru',
            'headline': headline,
            'url': url,
            'thumbnail': thumbnail,
            'description': desc,
            'time': t,
        })

    return response
