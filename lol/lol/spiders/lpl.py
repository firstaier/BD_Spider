# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from lol.items import ActivePlayersItem, TeamBaseInfoItem, BaseInfoItem, PlayerAwardsItem, FavoriteHerosItem
import json


class LplSpider(Spider):
    name = 'lpl'
    allowed_domains = ['lpl.qq.com']
    start_urls = ['http://lpl.qq.com/']

    # 这是战队详情页的url格式
    team_url = 'http://lpl.qq.com/web201612/data/LOL_MATCH2_TEAM_TEAM{TeamId}_INFO.js'
    # 这是队员详情页的url格式
    member_url = 'http://lpl.qq.com/web201612/data/LOL_MATCH2_TEAM_MEMBER{MemberId}_INFO.js'

    TeamIDs = {  # 这是战队的ID号
        'BLG': 57, 'EDG': 1, 'FPX': 7,
        'IG': 2, 'JDG': 29, 'LGD': 4,
        'OMG': 6, 'RNG': 8, 'RW': 422,
        'SNG': 41, 'Snake': 9, 'TOP': 42,
        'VG': 11, 'WE': 12
    }

    def start_requests(self):  # 将战队ID号取出，构建完整的战队详情页的URL，并使用parse_team函数解析
        for k, TeamID in self.TeamIDs.items():
            yield Request(self.team_url.format(TeamId=TeamID), self.parse_team)

    def parse_team(self, response):  # 将战队的信息解析并存入Item
        datas = json.loads(response.text)
        item1 = ActivePlayersItem()
        item2 = TeamBaseInfoItem()

        if 'msg' in datas.keys():
            data2 = datas['msg']['baseInfo']
            item2['TeamDesc'] = data2.get('TeamDesc')
            item2['TeamEnName'] = data2.get('TeamEnName')
            item2['TeamId'] = data2.get('TeamId')
            item2['TeamLogo'] = data2.get('TeamLogo')
            item2['TeamName'] = data2.get('TeamName')
            yield item2

            for data1 in datas['msg']['activePlayers']:
                item1['GameName'] = data1.get('GameName')
                item1['MemberId'] = data1.get('MemberId')
                item1['NickName'] = data1.get('NickName')
                item1['Place'] = data1.get('Place')
                item1['RealName'] = data1.get('RealName')
                item1['UserIcon'] = data1.get('UserIcon')
#                 item1['image_urls'] = data1.get('UserIcon')
#                 item1['images'] = data1.get('NickName')
                yield item1
                # 构造队员信息URL，回调函数为parse_member
                yield Request(self.member_url.format(MemberId=data1.get('MemberId')), self.parse_member)

    def parse_member(self, response):  # 将队员的信息存入Item
        results = json.loads(response.text)
        item3 = BaseInfoItem()
        item4 = FavoriteHerosItem()
        item5 = PlayerAwardsItem()
        if 'msg' in results.keys():
            data3 = results['msg']['baseInfo']
            item3['EnName'] = data3.get('EnName')
            item3['GameDate'] = data3.get('GameDate')
            item3['GameHero'] = data3.get('GameHero')
            item3['GameName'] = data3.get('GameName')
            item3['GamePlace'] = data3.get('GamePlace')
            item3['MemberDesc'] = data3.get('MemberDesc')
            item3['MemberId'] = data3.get('MemberId')
            item3['NickName'] = data3.get('NickName')
            item3['RealName'] = data3.get('RealName')
            item3['TeamId'] = data3.get('TeamId')
            item3['TeamName'] = data3.get('TeamName')
            item3['UserIcon'] = data3.get('UserIcon')
            yield item3

            for data4 in results['msg']['favoriteHeros']:
                item4['HeroId'] = data4.get('HeroId')
                item4['UseNum'] = data4.get('UseNum')
                item4['WinNum'] = data4.get('WinNum')
                item4['sUpdated'] = data4.get('sUpdated')
                yield item4

            try:  # 这里是队员以往荣誉，但是有些队员是新人，可能没有这方面的信息。
                for data5 in results['msg']['playerAwards']:
                    item5['AwardDesc'] = data5.get('AwardDesc')
                    item5['RankName'] = data5.get('RankName')
                    item5['sGameName'] = data5.get('sGameName')
                    yield item5
            except TypeError:
                return
