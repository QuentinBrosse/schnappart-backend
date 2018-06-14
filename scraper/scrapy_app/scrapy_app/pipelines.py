# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from scrapy.exceptions import DropItem
from api.models import SearchResult


class PersistencePipeline(object):
    """
    Save items in Django database.
    """

    logger = logging.getLogger('scrapy.pipeline.persistence')

    def process_item(self, item, spider):
        print('Spider Name %s' % spider.name)

        try:
            search_result = SearchResult(
                search_id=item['search'],
                url=item['url'],
                original_id=item['original_id'],
                title=item['title'],
                description=item['description'],
                price=item['price'],
                charges_included=item['charges_included'],
                publication_date=item['publication_date'],
                real_estate_type=item['real_estate_type'],
                rooms=item['rooms'],
                furnished=item['furnished'],
                surface=item['surface'],
                images=item['images'],
                zipcode=item['zipcode'],
                city=item['city'],
                ges=item['ges'],
                energy_rate=item['energy_rate'],
            )
            search_result.save()
        except Exception as exc:
            self.logger.info(
                'Validation error: "%s" on %s',
                exc, search_result.url)
            raise DropItem()

        return item
