# -*- coding: utf-8 -*-
import time
import os
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(BASE_DIR)
from jinja2 import Environment, FileSystemLoader
import os.path

from settings import DB_PARAM
from pymongo import MongoClient
from datetime import timedelta


path = '{}/templates/'.format(os.path.dirname(__file__))
# 创建一个加载器, jinja2 会从这个目录中加载模板
loader = FileSystemLoader(path)
# 用加载器创建一个环境, 有了它才能读取模板文件
env = Environment(loader=loader)


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def http_response(body, headers=None):
    """
    headers 是可选的字典格式的 HTTP 头
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v)
                            for k, v in headers.items()])
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def template(path, **kwargs):
    """
    本函数接受一个路径和一系列参数
    读取模板并渲染返回
    """
    t = env.get_template(path)
    return t.render(**kwargs)


def get_db():
    client = MongoClient(DB_PARAM['ip'], DB_PARAM['port'],
                          )

    db = client[DB_PARAM['database']]
    return db


def datetime_format(dt):
    dt = dt + timedelta(hours=8)
    return dt.strftime("%Y-%m-%d %H:%M")