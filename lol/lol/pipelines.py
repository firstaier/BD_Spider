# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymongo


# class MongoPipeline(object):
#
#     collection_name = 'lpl'
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGODB_URI'),
#             mongo_db=crawler.settings.get('MONGODB_DB')
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert(dict(item))
#         return item


from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from .items import ActivePlayersItem
import re
import json
import logging
import requests


def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path


class MongoImagePipeline(ImagesPipeline):

    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cookie': 'bid=yQdC/AzTaCw',
        'referer': 'http://lpl.qq.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def file_path(self, request, response=None, info=None):
        """
        :param request: 每一个图片下载管道请求
        :param response:
        :param info:
        :param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
        :return: 每套图的分类目录
        """
        item = request.meta['item']
        folder = item
        print('folder:', folder)
        folder_strip = strip(folder)
        image_guid = request.url.split('/')[-2]
        filename = u'full/{0}/{1}.png'.format(folder_strip, image_guid)
        return filename

    def get_media_requests(self, item, info):
        """
        :param item: spider.py中返回的item
        :param info:
        :return:
        """
        if isinstance(item, ActivePlayersItem):
            logging.debug("get_media_requests:"+item['UserIcon'])
            print('item:', item)
            img_url = item['UserIcon']
            # img_url = "http://img.crawler.qq.com/lolwebvideo/20180223171542/67ba1766a6c4d27f26cbab28e18613ea/0.png"
            logging.debug("get_media_requests url:"+img_url)
#             referer = item['UserIcon']
            print('url:', img_url)
            yield Request(img_url, meta={'item': item['NickName']})

            # fixed scrapy download image error
#             filename = item['NickName']+"_00.png"
#             ir = requests.get(img_url)
#             if ir.status_code == 200:
#                 open('images/' + filename, 'wb').write(ir.content)

#             self.default_headers['referer'] = img_url
#             yield Request(img_url, headers=self.default_headers, meta={'item': item})

#         for img_url in item['UserIcon']:
#             referer = item['UserIcon']
#             yield Request(img_url, meta={'item': item,
#                                          'referer': referer})
#             logging.debug("get_media_requests url:"+img_url)
#             self.default_headers['referer'] = img_url
#             yield Request(img_url, headers=self.default_headers)

    def item_completed(self, results, item, info):
        if isinstance(item, ActivePlayersItem):
            logging.debug("item_completed:"+item['UserIcon'])
            image_paths = [x['path'] for ok, x in results if ok] # ok判断是否下载成功
            print(results)
            if not image_paths:
                raise DropItem("Item contains no images")
        return item

#     def open_spider(self, spider):
#         self.file = open('items.jl', 'w')
# 
#     def close_spider(self, spider):
#         self.file.close()
# 
#     def process_item(self, item, spider):
#         if isinstance(item, ActivePlayersItem):
#             logging.debug("process_item:"+item['UserIcon'])
# 
#         line = json.dumps(dict(item)) + "\n"
#         self.file.write(line)
#         return item


import json


class MongoPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
