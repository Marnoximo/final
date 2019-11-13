from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd
import os

data = []


class VNCreatureImageSpider(CrawlSpider):
    name = 'vncreature-image'
    web_uri = 'http://www.vncreatures.net'

    def start_requests(self):
        df = pd.read_csv('/home/tien/Works/DH/final/project/reports/plantclef_vncreature_join_list.csv')

        for idx, row in df.iterrows():
            url = self.web_uri + row['vnc_url'].strip('.')
            class_id = row['ClassId']

            request = Request(url)
            request.meta['ClassId'] = class_id
            yield request

    def parse(self, response):
        class_id = response.meta['ClassId']
        images = response.xpath('//img[contains(@src,"picture")]')

        for image in images:
            image_url = image.xpath('./@src').extract_first()
            data.append({'ClassId': class_id, 'image_url': self.web_uri + image_url.strip('.')})


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(VNCreatureImageSpider)
    process.start()

    from modules.crawler.convert_to_plantclef_train_web import *
    df = pd.DataFrame(data)
    df = convert_to_plantclef(df, 'vncreature')
    df.to_csv('vncreature_image_list.csv', index=False)
