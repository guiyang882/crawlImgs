# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import urllib
import hashlib
from scrapy.utils.python import to_bytes
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        url = item['image_urls'][0]
        request = scrapy.Request(url)
        request.meta['word'] = item['image_label']
        yield request

    def item_completed(self, results, item, info):
        for ok, x in results:
            if ok:
                image_path = x['path']
                item['image_paths'] = image_path

                with open("image_infos.csv", 'a') as handle:
                    handle.write(item['image_label'] + "," + item['image_paths'] + "," + item['image_urls'][0] + "\n")

                return item

    def file_path(self, request, response=None, info=None):
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url
        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        word = str(request.meta['word']).split('word=')[-1]
        word = urllib.unquote(word).decode('utf-8')
        print(word+"/%s.jpg" % image_guid)
        return word + '/%s.jpg' % (image_guid)