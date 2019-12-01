from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import uuid
import logging

from config import DevelopmentConfig
from modules.common.db.database import DBHelper, VNCSpecies, VNCSpeciesDetails, VNCSpeciesImage, DetailStatusEnum

logger = logging.getLogger(__name__)
DBHelper.connect_database(DevelopmentConfig())


def download_and_put_image_into_host(url):
    return None


def update_status(obj, status,  session):
    try:
        obj.detail_status = status
        session.commit()
        logger.info('Updated status of object id={}, from to {}'.format(obj.id, status))
    except (Exception,) as ex:
        logger.error('Update detail_status failed on id={}. Error: {}'.format(obj.id, ex))
        session.rollback()


def query_and_update_status(vnc_id, status):
    session = DBHelper.get_session()

    try:
        obj = VNCSpecies.get_item(session, **{'id': vnc_id, 'limit': 1})[0]
        obj.detail_status = status
        session.commit()
        logger.info('Updated status of object id={}, from to {}'.format(vnc_id, status))
    except (Exception,) as ex:
        logger.error('Update detail_status failed on id={}. Error: {}'.format(vnc_id, ex))
        session.rollback()

    finally:
        session.close()


def add_database(entry, vnc_id):


    session = DBHelper.get_session()

    VNCSpeciesDetails.create(session, **{
        'id': vnc_id,
        'details': entry.get('details', '')
    })

    # TODO: download image, upload into host and add database
    for image_url in entry['url']:
        VNCSpeciesImage.create(session, **{
            'uuid': str(uuid.uuid5(uuid.NAMESPACE_URL, image_url)),
            'vnc_id': vnc_id,
            'vnc_url': image_url
        })

    session.close()

    query_and_update_status(vnc_id, DetailStatusEnum.completed.value)


class VNCreatureImageSpider(CrawlSpider):
    name = 'vncreature-detail'
    web_uri = 'http://www.vncreatures.net'

    def start_requests(self):
        # df = pd.read_csv('/home/tien/Works/DH/final/project/reports/plantclef_vncreature_join_list.csv')

        while True:
            session = DBHelper.get_session()
            objs = VNCSpecies.get_item(session, **{
                'detail_status': DetailStatusEnum.pending.value,
                'limit': 100
            })

            for obj in objs:
                update_status(obj, DetailStatusEnum.waiting.value, session)
                url = self.web_uri + obj.url.strip('.')
                vnc_id = obj.id

                request = Request(url)
                request.meta['vnc_id'] = vnc_id
                yield request

            session.close()

            if not objs:
                break

    def parse(self, response):
        vnc_id = response.meta['vnc_id']
        images = response.xpath('//img[contains(@src,"picture")]')

        data = {'url': []}

        for image in images:
            image_url = image.xpath('./@src').extract_first()
            data['url'].append(self.web_uri + image_url.strip('.'))

        detail_texts = response.xpath('//table[@class="Body00"]//table[@class="Body00"]//title/following-sibling::p')
        text = []
        for p in detail_texts:
            text.append(''.join(t.replace('\r\n', '') for t in p.xpath('.//text()').extract()))

        data['details'] = '\n'.join([t for t in text if t != ''])

        add_database(data, vnc_id)
        d = 1


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(VNCreatureImageSpider)
    process.start()
