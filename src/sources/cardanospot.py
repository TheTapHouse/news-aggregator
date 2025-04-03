from utils import make_request, make_json
from datetime import datetime
import os
from config import URLS

def fetch() -> list: 
    if not os.environ.get("CSPOT_API_KEY"):
        print('[CARDANOSPOT] CSPOT_API_KEY not found in environment variables, skipping...')
        return []
    
    r = make_request(
        URLS['cardanospot'],
        headers={'x-api-key': f'Partner {os.environ.get("CSPOT_API_KEY")}'}
    )
    data = make_json(r.text)

    response = []
    for item in data['data']:
        try:
            response.append({
                'source': 'Cardano Spot',
                'headline': item['title'],
                'url': item['articleUrl'],
                'thumbnail': item['mainImage'],
                'description': None,
                'time': datetime.strptime(item['createdOn'], "%Y-%m-%dT%H:%M:%S.%fZ")
            })
        except Exception as e:
            print(f'[CARDANOSPOT] Error: {e}')
            continue

    return response