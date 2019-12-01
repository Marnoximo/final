from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import json

from config import DevelopmentConfig
from modules.common.db.database import DBHelper, VNCSpecies


data = []
DBHelper().connect_database(DevelopmentConfig())


def add_to_database(entry):
    session = DBHelper().get_session()

    obj = VNCSpecies.create(session, **{
        'id': entry.get('id', ''),
        'name': entry.get('name_vi'),
        'species': entry.get('species', ''),
        'classname': entry.get('class', ''),
        'familyname': entry.get('family', ''),
        'ordername': entry.get('order', ''),
        'url': entry.get('url' '')
    })

    session.close()


class VNCreatureSpider(CrawlSpider):
    name = 'vncreature'
    web_uri = 'http://www.vncreatures.net/kqtracuu.php'
    entry_url = 'http://www.vncreatures.net/kqtracuu.php?ID=0&tenloai=&Submit=Tra+c%E1%BB%A9u&type=ho&ch=&loai=2&radio=V'

    def start_requests(self):
        yield Request(self.entry_url)

    def parse(self, response):
        rows = response.xpath('//table[@bgcolor="#CCCCCC"]//td[@align]')

        for row in rows:
            row_data = {}

            cells = row.xpath('following-sibling::td')
            for idx, cell in enumerate(cells):
                if idx == 0:
                    row_data['name_vi'] = cell.xpath('.//text()').extract_first().strip('\n').strip()
                    row_data['url'] = cell.xpath('.//a/@href').extract_first().strip('\n').strip()
                    continue
                elif idx == 1:
                    row_data['species'] = cell.xpath('.//text()').extract_first().strip('\n').strip()
                    continue
                elif idx == 2:
                    row_data['family'] = cell.xpath('.//text()').extract_first().strip('\n').strip()
                    continue
                elif idx == 3:
                    row_data['order'] = cell.xpath('.//text()').extract_first().strip('\n').strip()
                    continue
                elif idx == 4:
                    row_data['class'] = cell.xpath('.//text()').extract_first().strip('\n').strip()
                    continue
                else:
                    break

            if row_data['url'] is not None and 'ID=' in row_data['url']:
                row_data['id'] = row_data['url'].split('ID=')[-1]
                add_to_database(row_data)

                print(row_data)
                data.append(row_data)

        next_page = response.xpath('//a[text()=">"]/@href').extract_first()

        if bool(next_page):
            url = self.web_uri + next_page
            yield Request(url)


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(VNCreatureSpider)
    process.start()

    import pandas as pd
    df = pd.DataFrame(data)
    df.to_csv('vncreature_list.csv')
