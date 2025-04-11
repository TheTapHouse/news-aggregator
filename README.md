# News Feed
This repository contains a news aggregator that pulls multiple news sources and inserts into database. The database engine that is used is MySQL, but with `SQLAlchemy` this should be fairly straight forward to get working on other database engines.

### Table of Contents
1. [Live Usage](#live-usage)
2. [Platform & Versions](#platform-&-versions)
3. [Setup](#setup)
4. [Structure](#structure)
5. [System Diagram](#system-diagram)
6. [Fetcher Response Format](#fetcher-response-format)
7. [Handling Images](#handling-images)
8. [Configuration & Adding New Sources](#configuration-&-adding-new-sources)
9. [Plan to Evolve into an Optimized Resource Dedicated to Cardano](#plan-to-evolve-into-an-optimized-resource-dedicated-to-cardano)
10. [Database Schema](#database-schema)
11. [Supported News Outlets](#supported-news-outlets)

### Live Usage
This repository is currently feeding the [TapTools News Aggregator](https://www.taptools.io/news), a live production system being used by real users.

This repository is Version 2 of our prior news aggregator feed. Version 1 was not very extendable and lacked clear and concise documentation, so it was difficult to expand on it. This version was a complete rewrite and addressed all of Version 1's problems.

### Platform & Versions
The news aggregator feed was built using `Python 3.9.6`, and is deployed on a machine running `Amazon Linux 2`, although most Linux distributions should run this code just fine.

### Setup
1. Create virtual environment with `python3 -m venv venv`
2. Install required dependencies with `pip3 install -r requirements.txt`
3. Create required database tables and records with `python3 src/setup.py`
4. Pull latest news with `python3 src/main.py`

Can automate new data pulls by defining schedule in `crontab`.

### Structure
All news sources have their own `fetch` method that makes a request to a specific news outlet's RSS feed, parses into consistent formatting, and returns list of formatted news stories.

### System Diagram
![news-diagram](https://github.com/user-attachments/assets/22275257-8a61-49ce-8ebe-f6586893eb52)

### Fetcher Response Format
```
[
    source: str,      # news source name
    headline: str,    # headline of article
    url: str,         # url to news article
    thumbnail: str,   # image url to be used as thumbnail
    description: str, # description of news article
    time: int         # unix timestamp when article was published
]
```

### Handling Images
Most RSS feeds include a thumbnail image to use, but instead of using this link directly, we copy the image contents to our own S3 bucket to be served to frontend. This prevents external news outlets from rate limiting and having to serve images to our users.

To use this feature, you must create an AWS S3 bucket with a folder inside to hold the images. You can define this folder name with the `S3_NEWS_FOLDER` environment variable. You will then need to create an IAM user with requisite permissions to upload files. Populate your IAM credentials in `.env`.

To disable this feature, set `COPY_IMAGES` in config to `False`

### Configuration & Adding New Sources
All RSS URLs are defined in `config.py`, as well as some other configuration options.

To add new sources:
1. Define RSS URL in `config.py`
2. Create a file in the `sources` directory that contains a `fetch` method. This method should return a list of news stories with the exact format found above.
3. Update `setup.py` to insert this news source into the database (or insert manually). If not inserted manually, run the `setup.py` file.
4. This will automatically get picked up when `main.py` is ran.

### Plan to Evolve into an Optimized Resource Dedicated to Cardano
Following the steps above to add new sources, we plan to continually add news outlets that cover Cardano so that users have an easily accessible one-stop-shop for all of the latest Cardano news.

If you have a news outlet you would recommend to be added, you can either: 
- Create an issue in this repository with a link to the news outlet (preferably the RSS URL). The TapTools team will work to add this news source to the repository.
- Create a pull request with a working `fetch` method and appropriate response format

### Database Schema
The database schema to store the aggregated news consists of just two tables:
- `news.sources`: Defines individual news sources
- `news.stories`: Holds all individual news stories

You can find the table definitions in `database.py`. We use SQLAlchemy as the database ORM.

### Supported News Outlets
- [u.today](https://u.today)
- [CoinDesk](https://www.coindesk.com)
- [CoinTelegraph](https://cointelegraph.com)
- [Cardano Spot](https://cardanospot.io)
- [TapTools](https://taptools.io)
- [Forbes](https://forbes.com)
- [Bloomberg](https://bloomberg.com)
- [Watcher.Guru](https://watcher.guru)
