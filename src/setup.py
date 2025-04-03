import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import os
from database import NewsSource, NewsStory
from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    # Create database engine
    engine = db.create_engine(os.environ.get('SQL_DB_URI'), isolation_level='READ COMMITTED')
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    # Create tables if they don't exist
    session.execute('create schema if not exists news;')
    session.execute('''
        create table if not exists news.sources (
            id bigint auto_increment primary key,
            name varchar(255) not null,
            url text not null,
            index idx_sources_name (name)
        );
    ''')
    session.execute('''
        create table if not exists news.stories (
            id bigint auto_increment primary key,
            source_id bigint not null,
            headline text not null,
            url text not null,
            timestamp timestamp not null,
            description text,
            thumbnail text,
            foreign key (source_id) references news.sources(id),
            index idx_stories_source_id (source_id)
        );
    ''')
    session.commit()

    # Insert sources
    sources = [
        NewsSource(id=1, name='u.today', url='https://u.today/'),
        NewsSource(id=2, name='CoinDesk', url='https://www.coindesk.com/'),
        NewsSource(id=3, name='CoinTelegraph', url='https://cointelegraph.com/'),
        NewsSource(id=4, name='DailyCoin', url='https://dailycoin.com/'),
        NewsSource(id=5, name='TapTools', url='https://taptools.io/'),
        NewsSource(id=6, name='Cardano Spot', url='https://cardanospot.io/'),
        NewsSource(id=7, name='Bloomberg', url='https://www.bloomberg.com/'),
        NewsSource(id=8, name='Forbes', url='https://www.forbes.com/'),
        NewsSource(id=9, name='Watcher.Guru', url='https://watcher.guru/')
    ]

    for source in sources:
        # Check if source is already inserted
        if not session.query(NewsSource).filter_by(name=source.name).first():
            print(f'Inserting {source.name}')
            session.add(source)

        session.commit()