# -*- coding: utf-8 -*-


# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field


class ActivePlayersItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    GameName = Field()
    GamePlace = Field()
    MemberId = Field()
    NickName = Field()
    Place = Field()
    RealName = Field()
    UserIcon = Field()


class TeamBaseInfoItem(Item):
    TeamDesc = Field()
    TeamEnName = Field()
    TeamId = Field()
    TeamLogo = Field()
    TeamName = Field()


class BaseInfoItem(Item):
    EnName = Field()
    GameDate = Field()
    GameHero = Field()
    GameName = Field()
    GamePlace = Field()
    MemberDesc = Field()
    MemberId = Field()
    NickName = Field()
    RealName = Field()
    TeamId = Field()
    TeamName = Field()
    UserIcon = Field()


class FavoriteHerosItem(Item):
    HeroId = Field()
    UseNum = Field()
    WinNum = Field()
    sUpdated = Field()


class PlayerAwardsItem(Item):
    AwardDesc = Field()
    RankName = Field()
    sGameName = Field()
