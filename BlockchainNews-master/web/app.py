# -*- coding: utf-8 -*-

import os
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(BASE_DIR)

from flask import flash
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for



from flask import request
from flask import Flask, jsonify
from web.utils import get_db
from web.utils import datetime_format

# from news_crawler.main import start
# from settings import CRAWL_INTERVAL
# import time
from web.utils import (
    log,
    datetime_format,
    template,
    http_response,
)



app = Flask(__name__)

app.config.from_object('settings')
db = get_db()



@app.route('/api/v1/news')
def get_news():
    page = int(request.args.get('page', 0))
    limit = int(request.args.get('limit', 10))

    news = db.news.find().sort("crawled_at", -1).skip(page * limit).limit(limit)

    # import json
    # from bson import json_util
    # docs_list = list(news)
    # return json.dumps(docs_list, default=json_util.default)

    data = []
    for n in news:
        item = {
            'id': str(n['_id']),
            'title': n['title'],
            'url': n['url'],
            # 'Paragraph': n['Paragraph'],
            'image': n['img_url'],
            'category': n['category'],
            'source': n['source'],
            'created_at': datetime_format(n['crawled_at']),
        }

        data.append(item)
    return jsonify(data)



@app.route('/')
def index():
    # page = int(request.args.get('page', 0))
    # limit = int(request.args.get('limit', 100))
    #
    # news = db.news.find().sort("crawled_at", -1).skip(page * limit).limit(limit)

    # import json
    # from bson import json_util
    # docs_list = list(news)
    # return json.dumps(docs_list, default=json_util.default)

    # entries = []
    # for n in news:
    #     item = {
    #         'id': str(n['_id']),
    #         'title': n['title'],
    #         'url': n['url'],
    #         # 'Paragraph': n['Paragraph'],
    #         'image': n['img_url'],
    #         'category': n['category'],
    #         'source': n['source'],
    #         'created_at': datetime_format(n['crawled_at']),
    #     }
    #
    #     entries.append(item)
    #     # random.shuffle(entries)

     return render_template('show_entries.html')








if __name__ == '__main__':
    # start()
    # time.sleep(60 * CRAWL_INTERVAL)
    app.run(host='0.0.0.0', port=3009, debug=True)


