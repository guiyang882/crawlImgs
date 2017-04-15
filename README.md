# crawlImgs
这个是一个分布式爬虫。
抓取的关键词列表是通过json格式提交，具体的提交格式在 ./template/ 文件夹中。
其中，每个json都是一个例子，用户需要按照制定格式提交任务。

## 程序运行逻辑
- 代码从 ./fetchwords/中读取指定的文件，获得对应的列表词汇
- 通过解析出来的内容，进行爬虫的爬取

### Documents
[Documents Images Pipeline](http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/images.html)
