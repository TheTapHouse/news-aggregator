import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class NewsStory(base):
    __table_args__ = {'schema': 'news'}
    __tablename__ = 'stories'

    id = db.Column(db.BigInteger, primary_key=True)
    source_id = db.Column(db.BigInteger, db.ForeignKey('news.sources.id'), nullable=False)
    headline = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    thumbnail = db.Column(db.Text, nullable=True)

class NewsSource(base):
    __table_args__ = {'schema': 'news'}
    __tablename__ = 'sources'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    url = db.Column(db.String(255), nullable=False)