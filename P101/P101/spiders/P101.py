# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from P101.items import DokiSlimItem
from P101.items import DokiItem
import json
from xpinyin import Pinyin
import urllib


class P101Spider(Spider):
    name = 'P101'
    allowed_domains = ['v.qq.com']
    start_urls = ['http://v.qq.com/biu/101_star_web']
    p101_url = 'http://v.qq.com/biu/101_star_web'
    # allowed_domains = ['127.0.0.1:8080']
    # p101_url = 'http://127.0.0.1:8080/rank.html'

    single_url = 'http://v.qq.com/doki/star?id={starid}'

    def start_requests(self):  # 将战队ID号取出，构建完整的战队详情页的URL，并使用parse_team函数解析
        yield Request(self.p101_url, self.parse_p101)

    def parse_p101(self, response):

        p = Pinyin()
        # sel.xpath('//div[@class="list_item"]//a[contains(@href, "javascript:;")]/text()')
        for divs in response.xpath('//div[@class="list_item"]'):
            item1 = DokiSlimItem()
            for name in divs.xpath('.//a[contains(@href, "javascript:;")]/text()'):
                print(name.extract())
                cnname = name.extract()
                engname = p.get_pinyin(cnname, '')
                item1['name'] = cnname
                item1['engname'] = engname
            for starid in divs.xpath('.//a[@class="pic"][contains(@href, "javascript:;")]/@data-starid'):
                print(starid.extract())
                item1['starid'] = starid.extract()
            for pic in divs.xpath('.//a[@class="pic"][contains(@href, "javascript:;")]/img/@src'):
                print(pic.extract())
                item1['pic'] = pic.extract()
                item1['images'] = engname + ".png"
                # strurl = urllib.parse.quote(pic.extract().replace('.', ''))
                # strurl = "http://127.0.0.1:8080"+strurl
                strurl = pic.extract()
                strurl = "http:"+strurl
                item1['image_urls'] = [strurl]
                yield item1

                # 构造队员信息URL，回调函数为parse_idol
                yield Request(self.single_url.format(starid=item1['starid']), self.parse_idol)

    def parse_idol(self, response):  # 将队员的信息存入Item
        p = Pinyin()
        item2 = DokiItem()
        starid = str(response.url).strip().split("id=")[-1]
        epsdata = response.xpath('//div[@id="101"]/@data-round').extract()
        item2["epsdata"] = epsdata[0]

        properties = response.xpath('//div[@class="wiki_info_1"]//div[@class="line"]')
        name = properties[0].xpath('.//span[@class="content"]/text()').extract()
        # item2["name"] = name[0]
        cnname = name[0]
        engname = p.get_pinyin(cnname, '')
        item2['name'] = cnname
        item2['engname'] = engname
        item2['starid'] = starid

        height = properties[5].xpath('.//span[@class="content"]/text()').extract()
        item2["height"] = height[0]
        weight = properties[6].xpath('.//span[@class="content"]/text()').extract()
        item2["weight"] = weight[0]
        hometown = properties[7].xpath('.//span[@class="content"]/text()').extract()
        item2["hometown"] = hometown[0]
        yield item2
