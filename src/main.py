import os
import importlib
from datetime import datetime, timezone
from utils import make_db_connection, upload_file, make_request, slugify, get_source_ids
from dotenv import load_dotenv
load_dotenv()

from config import ENABLE_DB, DISABLE_SOURCES, COPY_IMAGES
from database import NewsStory

if __name__ == '__main__':
    # Create database engine
    if ENABLE_DB:
        db = make_db_connection(conn=os.environ.get('SQL_DB_URI'))
        source_ids = get_source_ids(session=db)

    # Get all sources from directory
    sources = os.listdir(os.path.join(os.getcwd(), 'src', 'sources'))
    for source in sources:
        if source in ['__init__.py', '__pycache__']:
            continue

        module_name = source.replace('.py', '')
        if module_name in DISABLE_SOURCES:
            print(f'{module_name} is disabled')
            continue
        
        print(f'Running {module_name}')

        module = importlib.import_module(f'sources.{module_name}')
        if hasattr(module, 'fetch') and callable(module.fetch):
            response = module.fetch()
            print(f'[{module_name}] Found {len(response)} news stories')

            # Insert into db
            for n in response:
                if ENABLE_DB:
                    # Make sure source is present in database
                    try:
                        source_ids[module_name]
                    except KeyError:
                        print(f'Source {module_name} not found in database, skipping...')
                        break
                    
                    # Check if headline already exists
                    # If not, insert
                    if not db.query(NewsStory).filter_by(source_id=source_ids[module_name], headline=n['headline']).first():
                        print(f'[{n["time"].strftime("%Y-%m-%d")}] {n["headline"]} -- {n.get("description")} -- {n.get("thumbnail")} ({n["source"]})')

                        if COPY_IMAGES and n['thumbnail']:
                            # Copy image to our S3 if available
                            img = make_request(n['thumbnail'])
                            if img.status_code == 200:
                                img_url = upload_file(image_data=img.content, filename=f'{os.environ.get("S3_NEWS_FOLDER")}/{module_name}-{slugify(n["headline"])}.png', bucket=os.environ.get('S3_BUCKET'))
                                n['thumbnail'] = img_url
                            else:
                                print(f'Error fetching image: {n["thumbnail"]}')
                                n['thumbnail'] = None

                        story = NewsStory(
                            source_id=source_ids[module_name],
                            headline=n['headline'],
                            url=n['url'],
                            timestamp=n['time'],
                            description=n['description'],
                            thumbnail=n['thumbnail']
                        )
                        db.add(story)
                        db.commit()
                else:
                    # Just print the news stories for debugging
                    print(f'[{n["time"].strftime("%Y-%m-%d")}] {n["headline"]} -- {n.get("description")} -- {n.get("thumbnail")} ({n["source"]})')


