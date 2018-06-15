
# 大数据爬虫——创造101

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badge/) [![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)      

最近创造101异常火爆，看到国内女团的正在崛起，向阳而生。

正好符合需要识别的人脸数据，索性用scrapy下载了一些数据用于大数据分析。

##  特性

- [x] **下载图片**
- [x] **用户信息**
- [x] **阶段排名**
- [x] **文件存储**
- [x] **中文名转英文**

##  原理

- 使用xpath分析网页，并下载数据
- 存储网页图片

## 使用教程

- Python版本：3.6及以上
- Scrapy版本：1.5.0及以上
- 相关软件工具安装和使用步骤请参考 [wechat_jump_game](https://github.com/wangshub/wechat_jump_game) 和 [Android 操作步骤](https://github.com/wangshub/wechat_jump_game/wiki/Android-%E5%92%8C-iOS-%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4)
1. 获取源码：`git clone https://github.com/firstaier/BD_Spider.git`
2. 进入源码目录： `cd BD_Spider`
3. 安装依赖： `pip install -r requirements.txt`
4. 运行程序：`scrapy crawl P101`

## 注意

部分网页做的不标准

## 下载图片

![](./screenshot/faces.png)

## LICENSE

MIT

欢迎 Star 和 Fork ~

如果你有什么问题请提 Issue，或者关注我的微信公众号留言，我都会一一解答


