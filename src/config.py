# Enable database usage
# Disable if debugging parsing
ENABLE_DB = False

# Copy images to S3
COPY_IMAGES = True

# Disable sources for debugging
# Leave empty to enable all sources
DISABLE_SOURCES = [
    # 'taptools',
    # 'cardanospot',
    # 'utoday',
    # 'coindesk',
    # 'cointelegraph',
    # 'bloomberg',
    # 'forbes',
    # 'watcherguru'
]

# Map from source name to RSS feed URL
URLS = {
    'taptools': 'https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/tap-in-with-taptools',
    'cardanospot': 'https://api.cardanospot.io/news/external?language=64e79f7998a529d9aa827452',
    'coindesk': 'https://www.coindesk.com/arc/outboundfeeds/rss?outputType=xml',
    'utoday': 'https://u.today/cryptocompare.php',
    'cointelegraph': 'https://cointelegraph.com/rss',
    'bloomberg': 'https://feeds.bloomberg.com/crypto/news.rss?ageHours=10000000',
    'forbes': 'https://feeds.forbes.com/?feedId=65e751905f3da70f9b117908',
    'watcherguru': 'https://watcher.guru/news/feed',
}