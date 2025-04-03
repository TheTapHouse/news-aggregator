from utils import make_request, make_json, make_soup, upload_file
from datetime import datetime
import re
from config import URLS

def fetch() -> list:
    r = make_request(URLS['taptools'])
    data = make_json(r.text)

    response = []
    for item in data['items']:
        try:
            soup = make_soup(item['description'], 'html.parser')

            try:
                thumbnail = soup.find('img')['src']
            except:
                thumbnail = None
            
            response.append({
                'source': 'TapTools',
                'headline': item['title'],
                'url': item['link'],
                'thumbnail': thumbnail,
                'description': None,
                'time': datetime.strptime(item['pubDate'], '%Y-%m-%d %H:%M:%S')
            })

            # Parse description by removing HTML elements and getting first <p>
            descriptions = soup.find_all('p')
            for desc in descriptions:
                if len(desc.text) >= 50:
                    response[-1]['description'] = desc.text
                    break

        except Exception as e:
            print(f'[TAPTOOLS] Error: {e}')
            continue


    return response