from pytz import timezone


# MongoDB
DB_PARAM = {
    'database': 'blockchain_news',
    'ip': '127.0.0.1',
    'port': 27017,

}


# 新闻抓取频率(分钟)
CRAWL_INTERVAL = 10


# TimeZone
UTC = timezone('UTC')
TIMEOUT = 60