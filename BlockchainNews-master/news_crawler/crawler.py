# --*-- coding: utf-8 --*--
import os
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(BASE_DIR)

import datetime
import requests
import time
import platform
from pymongo import MongoClient
from bs4 import BeautifulSoup
from news_crawler.check import check_future, check_blacklist
from settings import DB_PARAM


# from pyquery import PyQuery as pq

client = MongoClient(DB_PARAM['ip'], DB_PARAM['port'],
                     )


db = client[DB_PARAM['database']]


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
}


def get_driver():
    current_platform = platform.system()
    driver = None
    if current_platform == 'Darwin':
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome('/Users/rong/Documents/chromedriver', chrome_options=chrome_options)
        driver.set_page_load_timeout(60)
        time.sleep(0.5)
    if current_platform == 'Linux':
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.set_page_load_timeout(60)
        time.sleep(0.5)
    return driver


def get_image(driver, url):
    s = requests.Session()
    try:
        r = s.get(url, headers=headers)
        html_content = r.content
    except:
        time.sleep(6)
        driver.implicitly_wait(30)
        html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'lxml')
    imgs= soup.findAll('img')
    if not imgs:
        return
    if len(imgs) >= 2:
        cover_img = imgs[1]
    else:
        cover_img = imgs[0]
    candidate_images = []
    for img in imgs:
        try:
            weight = int(img.get("wight").strip('px')) if img.get("wight") else 0
            height = int(img.get("height").strip('px')) if img.get("height") else 0
            if weight > 600 and height > 600:
                cover_img = img
                break
            if weight > 500 and height > 500:
                cover_img = img
                break
            if weight > 500 or height > 500:
                candidate_images.append(img)
        except:
            pass
    if candidate_images:
        cover_img =  candidate_images[0]
    if not cover_img:
        return
    cover_img_url = cover_img.get("src", None)
    return cover_img_url





def crawl(url, source, category):
    driver = get_driver()
    try:
        driver.get(url)
        time.sleep(6)
        driver.implicitly_wait(30)
        # driver.set_page_load_timeout(30)
        # driver.set_script_timeout(30)

        js_down = "var q=document.documentElement.scrollTop=100000"
        js_up = "var q=document.documentElement.scrollTop=0"
        for i in range(3):
            driver.execute_script(js_down)
            time.sleep(2)
            driver.execute_script(js_up)
            time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        # title = soup.select("div.hd > h1")
        # print(title[0].get_text())
        # ctime = soup.select("div.a_Info > span.a_time")
        # print(time[0].string)
        # author = soup.select("div.qq_articleFt > div.qq_toolWrap > div.qq_editor")
        # print(author[0].get_text())
        # paras = soup.select("div.Cnt-Main-Article-QQ > p.text")
        # for para in paras:
        #     if len(para) > 0:
        #         print(para.get_text())
        #         print()
        #     # 写入文件
        #     fo = open("text.txt", "w+")
        #     fo.writelines(title[0].get_text() + "\n")
        #     fo.writelines(ctime[0].get_text() + "\n")
        #     for para in paras:
        #         if len(para) > 0:
        #             fo.writelines(para.get_text() + "\n\n")
        #     fo.writelines(author[0].get_text() + '\n')
        #     fo.close()
        items = soup.find_all('a')
        for i in items:
            title = i.string
            if title:
                title = title.strip()
            else:
                continue
            news_url = i.get('href')

            if title and check_future(title) and check_blacklist(title):
                print(title)
                # print(news_url)
                img_url = get_image(driver, news_url)

                data = {
                    'title': title,
                     'url': news_url,
                    # 'content': content,
                    # 'time': ctime[0].get_text(),
                    # 'Paragraph': paras,
                    # 'Author': author[0].get_text(),
                    'source': source,
                    'category': category,
                    'img_url': img_url,
                    'crawled_at': datetime.datetime.utcnow(),
                }
                print(data)
                is_exist = db.news.find_one({'title': title})
                if not is_exist:
                    db.news.insert(data)

    except Exception as e:
        print(str(e))
    driver.quit()

