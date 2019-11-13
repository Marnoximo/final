# from scrapy import Request
from scrapy_splash import SplashRequest
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd
import json
import random

data = []


class GoogleImageSpider(CrawlSpider):
    name = 'google-image'

    search_url = 'https://google.com/search?q={q}&tbm=isch'

    custom_settings = {
        # 'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        # 'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
        'SPLASH_URL': 'http://localhost:8050',
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'SPLASH_COOKIES_DEBUG': False,
        'DOWNLOAD_DELAY': 0.5,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
        },
        'RETRY_ENABLED': True,
        'USER_AGENTS': [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13', #
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1', #
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2', #
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3', #
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.4 (KHTML like Gecko) Chrome/22.0.1229.79 Safari/537.4',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.31 (KHTML like Gecko) Chrome/26.0.1410.63 Safari/537.31',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 1083) AppleWebKit/537.36 (KHTML like Gecko) Chrome/28.0.1469.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36', #
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36', #
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2859.0 Safari/537.36', #
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', #
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.49 Safari/537.36' #
        ]
    }

    def start_requests(self):
        df = pd.read_csv('/home/tien/Works/DH/final/project/reports/plantclef_vncreature_join_list.csv')
        # rs_df = pd.read_csv('google_image_list.csv')
        # list_class = rs_df['ClassId'].unique().tolist()

        for idx, row in df.iterrows():
            species = row['Species']
            class_id = row['ClassId']
            # if class_id in list_class:
            #     continue

            url = self.search_url.format(q=species)

            ua = random.choice(self.custom_settings['USER_AGENTS'])
            request = SplashRequest(url=url, callback=self.parse, endpoint='render.html', dont_filter=True, args={
                'images': 0,
                'wait': 10,
                'headers': {
                    'User-Agent': ua
                }
            })
            request.meta['ClassId'] = class_id
            request.meta['ua'] = ua
            yield request

    def parse(self, response):
        class_id = response.meta['ClassId']
        time = response.meta.get('time', 0)

        # images = response.xpath('//table[@class="images_table"]//td//img/@src').extract()
        images = response.xpath('//div[@class="rg_meta notranslate"]/text()').extract()
        fetched = []
        debug = 1
        for idx, image in enumerate(images):
            try:
                image_url = json.loads(image)['ou']
            except (Exception, ) as ex:
                print(str(ex))
                print('Error at Class_id=%d, idx=%d, json=%s'%(class_id, idx, image))
                continue

            entry = {'ClassId': class_id, 'image_url': image_url}
            fetched.append(entry)

        if len(fetched) <= 20 and time < 10:
            print("Class_id:%d recrawl, time: %d" % (class_id, time))
            url = response.url
            ua = random.choice(self.custom_settings['USER_AGENTS'])
            request = SplashRequest(url=url, callback=self.parse, endpoint='render.html', dont_filter=True, args={
                'images': 0,
                'wait': 10,
                'headers': {
                    'User-Agent': ua
                }
            })
            request.meta['ClassId'] = class_id
            request.meta['ua'] = ua
            request.meta['time'] = time + 1
            yield request

        else:
            print("Class_id:%d get %d images" % (class_id, len(fetched)))
            data.extend(fetched)


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(GoogleImageSpider)
    process.start()

    from modules.crawler.convert_to_plantclef_train_web import *
    df = pd.DataFrame(data)
    df = convert_to_plantclef(df, 'google')
    df.to_csv('google_image_list.csv', index=False)
