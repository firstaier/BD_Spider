# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from .items import DokiSlimItem
from scrapy import Request
from scrapy import log
import requests
import re
import logging
import json


def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path


class P101Pipeline(object):
    def process_item(self, item, spider):
        return item


class P101ImgDownloadPipeline(ImagesPipeline):
    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
#         'referer': 'http://puui.qpic.cn/media_img/0/',
        'referer': 'http://127.0.0.1:8080/',
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
        print('abc:')
        item = request.meta['item']
        folder = item
        print('folder:', folder)
        folder_strip = strip(folder)
        filename = u'{0}'.format(folder_strip)
        return filename

    def get_media_requests(self, item, info):
        if isinstance(item, DokiSlimItem):
            logging.debug("get_media_requests:"+item['image_urls'][0])
            print('item:', item)
            for image_url in item['image_urls']:
                self.default_headers['referer'] = image_url
#                 yield Request(image_url, headers=self.default_headers)
                logging.debug("get_media_requests url:"+image_url)
    #             referer = item['UserIcon']
                print('url:', image_url)
                yield Request(image_url, meta={'item': item['images']})

#         for image_url in item['image_urls']:
#             self.default_headers['referer'] = image_url
#             print('xxxx:'+image_url)
#             yield Request(image_url, headers=self.default_headers)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


class JsonPipeline(object):

    def open_spider(self, spider):
        self.file = open('data.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
