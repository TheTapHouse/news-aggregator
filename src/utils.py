import requests
from bs4 import BeautifulSoup
import json
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import boto3
from botocore.exceptions import ClientError
import os
import io
import re
import unicodedata
from database import NewsSource

def make_db_connection(conn: str) -> db.orm.session.Session:
    '''
    Create a database connection
    '''
    engine = db.create_engine(os.environ.get('SQL_DB_URI'), isolation_level='READ COMMITTED')
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

def make_soup(content: str, parser: str = 'html.parser') -> BeautifulSoup:
    '''
    Parse HTML content
    '''
    return BeautifulSoup(content, parser)

def make_request(url: str, headers: dict = {}) -> requests.Response:
    '''
    Make HTTP GET request
    '''
    return requests.get(url, headers=headers)

def make_json(content: str) -> dict:
    '''
    Parse JSON content
    '''
    return json.loads(content)

def upload_file(image_data: bytes, filename: str, bucket: str) -> str:
    '''
    Update image data to S3 as a file
    '''
    s3_client = boto3.client(
        's3',
        region_name=os.environ.get('S3_REGION'),
        aws_access_key_id=os.environ.get('S3_AWS_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('S3_AWS_SECRET_KEY')
    )
    try:
        response = s3_client.upload_fileobj(
            Fileobj=io.BytesIO(image_data),
            Bucket=bucket,
            Key=filename
        )
    except ClientError as e:
        print(f'[UPLOAD FILE] Error: {e}')
        return ''

    return f'{os.environ.get("S3_CLOUDFRONT_LINK")}/{filename}'

def slugify(text: str) -> str:
    '''
    Make text URL safe
    '''
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text.lower())     # remove special chars
    text = re.sub(r'[\s_-]+', '-', text).strip('-')  # normalize spaces/dashes
    return text

def get_source_ids(session: db.orm.session.Session) -> dict:
    '''
    Get internal database source IDs to be able to map from source name to source ID
    '''
    sources = session.query(NewsSource).all()
    source_ids = {}
    for source in sources:
        source_ids[str(source.name).replace('.', '').lower()] = source.id
    return source_ids